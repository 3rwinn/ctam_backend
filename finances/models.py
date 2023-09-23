from django.db import models
from common.models import Mission, TypeSortie, TypeEntree
from django.contrib.auth.models import User

# Create your models here.
class EntreeCaisse(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    montant = models.IntegerField()
    type_entree = models.ForeignKey(TypeEntree, on_delete=models.CASCADE)
    commentaire = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mission} - {self.montant} - {self.type_entree} - {self.date}"
    
class SortieCaisse(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    montant = models.IntegerField()
    type_sortie = models.ForeignKey(TypeSortie, on_delete=models.CASCADE)
    commentaire = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    facture = models.FileField(upload_to='sorties/', null=True, blank=True)

    def __str__(self):
        return f"{self.mission} - {self.montant} - {self.type_sortie} - {self.date}"
    
class SuiviBanque(models.Model):
    date = models.DateField()
    montant = models.IntegerField()
    commentaire = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    action = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.date} - {self.action} - {self.montant}"
    
class FicheDimanche(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    date = models.DateField()
    entrees = models.JSONField()
    sorties = models.JSONField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.mission} - {self.date}"