from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import path, reverse

from lettings.models import Address, Letting
from oc_lettings_site.urls import urlpatterns as base_urlpatterns
from profiles.models import Profile


def erroring_view(request):
    """Raise unconditionally to trigger Django's 500 error handler."""
    raise Exception("Forced exception for 500 page test")


# URLconf used only by the 500 test: the real urlpatterns plus a view that
# deliberately raises. The real patterns are kept because base.html resolves
# named routes (``index``, ``profiles:index``, ``lettings:index``) that must
# still exist for the 500 page itself to render.
urlpatterns = base_urlpatterns + [
    path("boom/", erroring_view, name="boom"),
]


class ErrorPagesTest(TestCase):
    """Verify the custom 404 and 500 templates are actually rendered."""

    def test_404_page_renders_custom_template(self):
        """An unknown URL should return 404 and render templates/404.html."""
        client = Client()
        response = client.get("/this-url-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    @override_settings(ROOT_URLCONF=__name__, DEBUG=False)
    def test_500_page_renders_custom_template(self):
        """An unhandled exception should return 500 and render templates/500.html."""
        client = Client(raise_request_exception=False)
        response = client.get("/boom/")
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "500.html")


class SiteIntegrationTests(TestCase):
    """Parcours utilisateur global : accueil -> lettings -> profiles."""

    def setUp(self):
        self.client = Client()
        self.address = Address.objects.create(
            number=12,
            street="rue Example",
            city="New York",
            state="NY",
            zip_code=75000,
            country_iso_code="USA",
        )
        self.letting = Letting.objects.create(
            title="Cozy Apartment", address=self.address
        )
        self.user = User.objects.create_user(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="jdoe@example.com",
        )
        self.profile = Profile.objects.create(user=self.user, favorite_city="Paris")

    def test_full_site_user_journey(self):
        # Accueil : présente des liens vers lettings et profiles
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        lettings_index_url = reverse("lettings:index")
        profiles_index_url = reverse("profiles:index")
        self.assertContains(response, lettings_index_url)
        self.assertContains(response, profiles_index_url)

        # Accueil -> liste des lettings -> détail d'une location
        response = self.client.get(lettings_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.letting.title)

        letting_detail_url = reverse("lettings:letting", args=[self.letting.id])
        response = self.client.get(letting_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.address.street)

        # Accueil -> liste des profiles -> détail d'un profile
        response = self.client.get(profiles_index_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        profile_detail_url = reverse("profiles:profile", args=[self.user.username])
        response = self.client.get(profile_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.favorite_city)
