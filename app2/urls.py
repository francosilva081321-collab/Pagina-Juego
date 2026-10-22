from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.inicio, name="hola"),
    path('historia/', views.historia, name="historia"),
    path('personajes/', views.personajes, name="personajes"),
    path('descarga/', views.descarga, name="descarga"),
    path('login/', views.IniciarSesionView.as_view(), name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'recuperar-contrasena/',
        auth_views.PasswordResetView.as_view(
            template_name='app2/password_reset_form.html',
            email_template_name='app2/password_reset_email.html',
            subject_template_name='app2/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'recuperar-contrasena/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='app2/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'restablecer-contrasena/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='app2/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'restablecer-contrasena/completo/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='app2/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]