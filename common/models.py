from django.db import models

# Create your models here.
class Mission(models.Model):
    libelle = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.libelle}"
    
class Palier(models.Model):
    montant = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.libelle}"
    
class TypeSortie(models.Model):
    libelle = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.libelle}"
    
class TypeEntree(models.Model):
    libelle = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.libelle}"


class Evenement(models.Model):
    libelle = models.CharField(max_length=150)
    date = models.DateField()
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.libelle}"
    

class Communication(models.Model):
    libelle = models.CharField(max_length=150)
    membres = models.JSONField(blank=True, null=True) # {full_name: "John Doe", contact: "123456789"}

    def __str__(self):
        return f"{self.libelle}"
    

class TimeLine(models.Model):
    action = models.TextField()
    membre = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action}"
    