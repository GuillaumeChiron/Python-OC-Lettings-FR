from django.urls import path

from profiles import views

app_name = "profiles"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:username>/", views.profile, name="profile"),
]
