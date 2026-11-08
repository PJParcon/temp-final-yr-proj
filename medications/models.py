from django.db import models
from django.conf import settings


class Medication(models.Model):
    class MedicationForm(models.TextChoices):
        TABLET = 'tablet', 'Tablet'
        LIQUID = 'liquid', 'Liquid'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField('Medication name', max_length=200)
    strength = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    medication_form = models.CharField(max_length=10, choices=MedicationForm.choices, default=MedicationForm.TABLET)
    frequency = models.CharField(max_length=200)
    instructions = models.TextField('Additional instructions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
