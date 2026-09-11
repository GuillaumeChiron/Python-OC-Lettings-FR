"""Tests de l'app profiles : modèles, vues, URLs et parcours utilisateur."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from profiles.models import Profile


class ProfileModelTests(TestCase):
    """Tests du modèle Profile : représentation et champ optionnel."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="jdoe@example.com",
        )
        self.profile = Profile.objects.create(
            user=self.user, favorite_city="Paris"
        )

    def test_str_returns_username(self):
        self.assertEqual(str(self.profile), "jdoe")

    def test_favorite_city_can_be_blank(self):
        other_user = User.objects.create_user(username="asmith")
        profile = Profile(user=other_user, favorite_city="")
        profile.full_clean()


class ProfilesViewsTests(TestCase):
    """Tests des vues index et profile : statut, template, contexte, 404."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="jdoe@example.com",
        )
        self.profile = Profile.objects.create(
            user=self.user, favorite_city="Paris"
        )

    def test_index_status_code_200(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertTemplateUsed(response, "profiles/index.html")

    def test_index_context_contains_profiles_list(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertIn("profiles_list", response.context)
        self.assertIn(self.profile, response.context["profiles_list"])

    def test_profile_detail_status_code_200(self):
        response = self.client.get(
            reverse("profiles:profile", args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_context_contains_profile(self):
        response = self.client.get(
            reverse("profiles:profile", args=[self.user.username])
        )
        self.assertEqual(response.context["profile"], self.profile)

    def test_profile_detail_404_if_not_found(self):
        response = self.client.get(
            reverse("profiles:profile", args=["unknown_user"])
        )
        self.assertEqual(response.status_code, 404)


class ProfilesUrlsTests(TestCase):
    """Tests de résolution des routes namespacées de l'app profiles."""

    def test_index_url_resolves(self):
        self.assertEqual(reverse("profiles:index"), "/profiles/")

    def test_profile_url_resolves(self):
        self.assertEqual(
            reverse("profiles:profile", args=["jdoe"]), "/profiles/jdoe/"
        )


class ProfilesIntegrationTests(TestCase):
    """Parcours utilisateur simple : liste des profils puis détail."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="jdoe@example.com",
        )
        self.profile = Profile.objects.create(
            user=self.user, favorite_city="Paris"
        )

    def test_user_journey_from_index_to_detail(self):
        response = self.client.get(reverse("profiles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        detail_url = reverse("profiles:profile", args=[self.user.username])
        self.assertContains(response, detail_url)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.profile.favorite_city)
