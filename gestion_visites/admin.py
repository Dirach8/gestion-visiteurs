from django.contrib import admin
from .models import Visiteur, Service, Visite


@admin.register(Visiteur)
class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'type_piece', 'numero_piece')
    search_fields = ('nom', 'prenom', 'telephone', 'numero_piece')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'statut')
    search_fields = ('nom',)
    list_filter = ('statut',)


@admin.register(Visite)
class VisiteAdmin(admin.ModelAdmin):
    list_display = (
        'visiteur',
        'service',
        'enregistre_par',
        'motif',
        'date_heure_entree',
        'date_heure_sortie',
        'statut'
    )
    search_fields = (
        'visiteur__nom',
        'visiteur__prenom',
        'motif',
    )
    list_filter = ('statut', 'service')