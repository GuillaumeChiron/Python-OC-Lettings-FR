"""Mise en place des routes d'accès pour les profiles"""

from django.urls import path
from profiles import views

"""Nom de référence pour les routes profiles"""
app_name = "profiles"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:username>/", views.profile, name="profile"),
]
