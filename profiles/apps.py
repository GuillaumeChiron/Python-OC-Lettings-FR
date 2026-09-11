"""Configuration de l'app Profile"""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Utilise BigAutoField comme clé primaire par défaut pour les modèles de l'app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "profiles"
