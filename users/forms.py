# users/forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

User = get_user_model()

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Nom d\'usuari només pot contenir lletres, números i @/./+/-/_.'
)

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contrasenya',
        widget=forms.PasswordInput,
        help_text='Introdueix una contrasenya segura.'
    )
    password2 = forms.CharField(
        label='Confirma contrasenya',
        widget=forms.PasswordInput,
        help_text='Torna a introduir la contrasenya.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('El nom d’usuari és obligatori.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Aquest nom d’usuari ja existeix.')

        if not username.isalnum():
            raise ValidationError('El nom d’usuari només pot contenir lletres i números.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Ja existeix un usuari amb aquest email.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Les contrasenyes no coincideixen.')
        if p1:
            try:
                validate_password(p1, user=None)
            except ValidationError as e:
                raise ValidationError({'password1': e.messages})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'display_name', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Una mica sobre tu...'}),
            'avatar': forms.FileInput(),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        # Exemple senzill de validació: mida màxima 2MB i tipus imatge
        if avatar:
            if hasattr(avatar, 'size') and avatar.size > 2 * 1024 * 1024:
                raise ValidationError('L\'avatar no pot superar els 2 MB.')
            # validar content_type si està disponible
            content_type = getattr(avatar, 'content_type', None)
            if content_type and not content_type.startswith('image/'):
                raise ValidationError('El fitxer ha de ser una imatge.')
        return avatar


class CustomAuthenticationForm(AuthenticationForm):
    """
    Permet login amb username o email.
    Llegeix el camp 'username' (pot ser email) i intenta autenticar.
    """
    username = forms.CharField(label='Usuari o Email')

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Intentar autenticar per username directe
            user = authenticate(self.request, username=username_or_email, password=password)
            if not user:
                # si no, buscar usuari amb email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    user = authenticate(self.request, username=user_obj.get_username(), password=password)
                except User.DoesNotExist:
                    user = None

            if user is None:
                raise forms.ValidationError('Credencials no vàlides. Revisa usuari/email i contrasenya.')

            # assignar l'usuari per a la resta del procés d'AuthenticationForm
            self.confirm_login_allowed(user)
            self.user_cache = user
            return self.cleaned_data
        return super().clean()
