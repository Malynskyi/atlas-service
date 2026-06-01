from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    company_name = models.CharField(_("company name"), max_length=255, blank=True)

    class Roles(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MANAGER = "manager", _("Manager")
        VIEWER = "viewer", _("Viewer")

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=Roles.choices,
        default=Roles.VIEWER,
    )

    def __str__(self):
        return self.username