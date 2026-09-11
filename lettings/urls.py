"""Mise en place des routes d'accès pour les locations"""

from django.urls import path
from lettings import views

"""Nom de reférence pour les routes Lettings"""
app_name = "lettings"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:letting_id>/", views.letting, name="letting"),
]
