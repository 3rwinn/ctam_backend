from django.db import models
from common.models import Mission

class Membre(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    sexe = models.CharField(max_length=5)
    fonction = models.CharField(max_length=150, blank=True)
    marie = models.BooleanField(default=False)
    baptise = models.BooleanField(default=False)
    contact = models.CharField(max_length=15)
    habitation = models.CharField(max_length=150)
    nouveau = models.BooleanField(default=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    encadreur = models.CharField(max_length=150, null=True)
    merged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

