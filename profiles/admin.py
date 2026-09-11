"""Initialisation du modèle Profile dans admin"""

from django.contrib import admin
from profiles.models import Profile

admin.site.register(Profile)
