from django.db import models
from django.contrib.auth.models import User


class Visiteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    type_piece = models.CharField(max_length=50)
    numero_piece = models.CharField(max_length=50)

    structure_delivrance = models.CharField(
        max_length=100,
        blank=True
    )

    date_delivrance = models.DateField(
        null=True,
        blank=True
    )

    date_expiration = models.DateField(
        null=True,
        blank=True
    )

    document_cnib = models.FileField(
        upload_to='documents_cnib/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    statut = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
class Visite(models.Model):

    class StatutVisite(models.TextChoices):
        PRESENT = 'PRESENT', 'Présent'
        SORTI = 'SORTI', 'Sorti'

    visiteur = models.ForeignKey(
        Visiteur,
        on_delete=models.PROTECT,
        related_name='visites'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='visites'
    )

    enregistre_par = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='visites_enregistrees'
    )

    motif = models.TextField()
    observation = models.TextField(blank=True)

    date_heure_entree = models.DateTimeField()
    date_heure_sortie = models.DateTimeField(
        null=True,
        blank=True
    )

    statut = models.CharField(
        max_length=10,
        choices=StatutVisite.choices,
        default=StatutVisite.PRESENT
    )

    def __str__(self):
        return f"{self.visiteur} - {self.service} - {self.statut}"    
    