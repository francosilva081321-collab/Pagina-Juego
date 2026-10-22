from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class InicioSesionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'placeholder': 'Tu usuario',
        })
        self.fields['password'].label = 'Contraseña'
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'placeholder': 'Tu contraseña',
        })


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'Tu correo electrónico',
        }),
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'placeholder': 'Elige un usuario',
        })
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': 'Crea una contraseña',
        })
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': 'Repite la contraseña',
        })
