"""Configuration de l'app Lettings"""

from django.apps import AppConfig


class LettingsConfig(AppConfig):
    """Utilise BigAutoField comme clé primaire par défaut pour les modèles de l'app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "lettings"
