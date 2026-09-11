"""Initialisation des modèles Letting et Address dans admin"""

from django.contrib import admin
from lettings.models import Letting, Address

admin.site.register(Letting)
admin.site.register(Address)
