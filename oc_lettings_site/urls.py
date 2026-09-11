"""Mise en place des routes d'accès du site"""

from django.contrib import admin
from django.urls import path, include

from oc_lettings_site import views

"""Les routes incluent les routes de lettings et profiles definie dans les apps respectives"""
urlpatterns = [
    path("", views.index, name="index"),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls),
]
