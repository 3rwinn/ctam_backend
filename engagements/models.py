from django.db import models
from common.models import Mission, Palier
from membres.models import Membre

# Create your models here.
class Engagement(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    palier = models.ForeignKey(Palier, on_delete=models.CASCADE)
    annee = models.DateField()

    class Meta:
        unique_together = ('mission', 'membre', 'palier', 'annee')

    def __str__(self):
        return f"{self.mission} {self.membre} {self.palier}"
    

class Mouvement(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    montant = models.IntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.engagement} - {self.montant}"
    

class Depense(models.Model):
    libelle = models.CharField(max_length=150)
    montant = models.IntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    facture = models.FileField(upload_to='depenses/', null=True, blank=True)

