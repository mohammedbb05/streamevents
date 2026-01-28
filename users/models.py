from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# Extendim AbstractUser per afegir camps extra requerits pel projecte:
# - display_name: nom públic opcional
# - bio: text breu
# - avatar: imatge d'usuari
class CustomUser(AbstractUser):
    # Validem username amb la mateixa regex que Django per coherència
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=_("El nom d'usuari només pot contenir lletres, números i @/./+/-/_")
    )

    display_name = models.CharField(
        _("Display name"),
        max_length=150,
        blank=True,
        help_text=_("Nom públic que es mostrarà al perfil")
    )
    bio = models.TextField(
        _("Bio"),
        blank=True,
        help_text=_("Una breu descripció sobre l'usuari"),
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to='avatars/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text=_("Imatge de perfil")
    )
    email = models.EmailField(unique=True)

    # Opcional: redefinir el __str__ per mostrar identificador clar
    def __str__(self):
        return self.display_name or self.get_username()
