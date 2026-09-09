from django.contrib import admin
from django.urls import path
from gestion_visites.views import (
    connexion, 
    dashboard_agent, 
    dashboard_admin, 
    enregistrer_visite,
    visites_en_cours, 
    enregistrer_sortie,
     historique_visites,
     liste_visiteurs,
      deconnexion)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', connexion, name='connexion'),

    path(
        'dashboard/agent/',
        dashboard_agent,
        name='dashboard_agent'
    ),

    path(
        'dashboard/admin/',
        dashboard_admin,
        name='dashboard_admin'
    ),

    path(
    'visite/enregistrer/',
    enregistrer_visite,
    name='enregistrer_visite'
),

   path(
    'visites/en-cours/',
    visites_en_cours,
    name='visites_en_cours'
),

path(
    'visite/<int:visite_id>/sortie/',
    enregistrer_sortie,
    name='enregistrer_sortie'
),

path(
    'historique/',
    historique_visites,
    name='historique_visites'
),

path(
    'visiteurs/',
    liste_visiteurs,
    name='liste_visiteurs'
),

path(
    'deconnexion/',
    deconnexion,
    name='deconnexion'
),
]