"""Tests de l'app lettings : modèles, vues, URLs et parcours utilisateur."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from lettings.models import Address, Letting


class AddressModelTests(TestCase):
    """Tests du modèle Address : représentation, Meta, validators."""

    def setUp(self):
        self.address = Address.objects.create(
            number=12,
            street="rue Example",
            city="New York",
            state="NY",
            zip_code=75000,
            country_iso_code="USA",
        )

    def test_str_returns_number_and_street(self):
        self.assertEqual(str(self.address), "12 rue Example")

    def test_verbose_name_plural_is_addresses(self):
        self.assertEqual(Address._meta.verbose_name_plural, "addresses")

    def test_number_above_max_is_invalid(self):
        address = Address(
            number=10000,
            street="rue Example",
            city="New York",
            state="NY",
            zip_code=75000,
            country_iso_code="USA",
        )
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_state_too_short_is_invalid(self):
        address = Address(
            number=12,
            street="rue Example",
            city="New York",
            state="N",
            zip_code=75000,
            country_iso_code="USA",
        )
        with self.assertRaises(ValidationError):
            address.full_clean()

    def test_country_iso_code_too_short_is_invalid(self):
        address = Address(
            number=12,
            street="rue Example",
            city="New York",
            state="NY",
            zip_code=75000,
            country_iso_code="US",
        )
        with self.assertRaises(ValidationError):
            address.full_clean()


class LettingModelTests(TestCase):
    """Tests du modèle Letting : représentation et relation avec Address."""

    def setUp(self):
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

    def test_str_returns_title(self):
        self.assertEqual(str(self.letting), "Cozy Apartment")

    def test_address_relation_is_one_to_one(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Letting.objects.create(title="Another Place", address=self.address)


class LettingsViewsTests(TestCase):
    """Tests des vues index et letting : statut, template, contexte, 404."""

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

    def test_index_status_code_200(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertTemplateUsed(response, "lettings/index.html")

    def test_index_context_contains_lettings_list(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertIn("lettings_list", response.context)
        self.assertIn(self.letting, response.context["lettings_list"])

    def test_letting_detail_status_code_200(self):
        response = self.client.get(reverse("lettings:letting", args=[self.letting.id]))
        self.assertEqual(response.status_code, 200)

    def test_letting_detail_context_contains_title_and_address(self):
        response = self.client.get(reverse("lettings:letting", args=[self.letting.id]))
        self.assertEqual(response.context["title"], self.letting.title)
        self.assertEqual(response.context["address"], self.address)

    def test_letting_detail_404_if_not_found(self):
        response = self.client.get(reverse("lettings:letting", args=[9999]))
        self.assertEqual(response.status_code, 404)


class LettingsUrlsTests(TestCase):
    """Tests de résolution des routes namespacées de l'app lettings."""

    def test_index_url_resolves(self):
        self.assertEqual(reverse("lettings:index"), "/lettings/")

    def test_letting_url_resolves(self):
        self.assertEqual(reverse("lettings:letting", args=[1]), "/lettings/1/")


class LettingsIntegrationTests(TestCase):
    """Parcours utilisateur simple : liste des locations puis détail."""

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

    def test_user_journey_from_index_to_detail(self):
        response = self.client.get(reverse("lettings:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.letting.title)

        detail_url = reverse("lettings:letting", args=[self.letting.id])
        self.assertContains(response, detail_url)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.address.number))
        self.assertContains(response, self.address.street)
