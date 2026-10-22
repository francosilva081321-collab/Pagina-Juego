import re

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AuthenticationTests(TestCase):
    def test_registration_creates_user_and_logs_them_in(self):
        response = self.client.post(reverse('registro'), {
            'username': 'commander_one',
            'email': 'commander@example.com',
            'password1': 'Long-unique-Password-8750!',
            'password2': 'Long-unique-Password-8750!',
        })

        self.assertRedirects(response, reverse('hola'))
        self.assertTrue(
            get_user_model().objects.filter(username='commander_one').exists()
        )
        self.assertEqual(
            get_user_model().objects.get(username='commander_one').email,
            'commander@example.com',
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_and_logout(self):
        user = get_user_model().objects.create_user(
            username='commander_two',
            password='Long-unique-Password-8751!',
        )

        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'Long-unique-Password-8751!',
        })

        self.assertRedirects(response, reverse('hola'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('hola'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_invalid_credentials_do_not_log_in(self):
        response = self.client.post(reverse('login'), {
            'username': 'unknown',
            'password': 'wrong-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_password_reset_changes_password_using_email_link(self):
        user = get_user_model().objects.create_user(
            username='commander_three',
            email='commander3@example.com',
            password='Long-unique-Password-8752!',
        )

        response = self.client.post(reverse('password_reset'), {
            'email': user.email,
        })

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])

        match = re.search(
            r'/restablecer-contrasena/([^/]+)/([^/\s]+)',
            mail.outbox[0].body,
        )
        self.assertIsNotNone(match)
        uidb64, token = match.groups()
        confirm_url = reverse(
            'password_reset_confirm',
            kwargs={'uidb64': uidb64, 'token': token},
        )
        response = self.client.get(confirm_url, follow=True)
        self.assertEqual(response.status_code, 200)
        confirm_form_url = response.redirect_chain[-1][0]

        response = self.client.post(confirm_form_url, {
            'new_password1': 'New-unique-Password-8753!',
            'new_password2': 'New-unique-Password-8753!',
        })

        self.assertRedirects(response, reverse('password_reset_complete'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('New-unique-Password-8753!'))

    def test_password_reset_does_not_reveal_unknown_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'unknown@example.com',
        })

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_logout_navigation_has_confirmation_prompt(self):
        user = get_user_model().objects.create_user(
            username='commander_four',
            password='Long-unique-Password-8754!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('hola'))

        self.assertContains(
            response,
            "confirm('¿Estás seguro de que quieres cerrar sesión?')",
        )
