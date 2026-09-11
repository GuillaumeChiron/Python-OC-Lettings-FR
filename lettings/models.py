"""modele des classes de l'app lettings : adresses et locations"""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """adresse postale associé à une location

    ``state`` attend un code à 2 chiffres et ``country_iso_code```
    un code ISO sur 3 lettres"""

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)]
    )

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return f"{self.number} {self.street}"


class Letting(models.Model):
    """location ratachée à une adresse

    une location possède une unique adresse avec une relation
    ``OneToOneField``"""

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
