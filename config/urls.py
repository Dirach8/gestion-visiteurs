from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gestion_visites.views import (
    connexion, 
    dashboard_agent, 
    dashboard_admin,
     gestion_services,
     ajouter_service, 
     modifier_service,
    enregistrer_visite,
    visites_en_cours, 
    enregistrer_sortie,
     historique_visites,
     liste_visiteurs,
     gestion_utilisateurs,
     ajouter_utilisateur,
     modifier_utilisateur,
     reinitialiser_mot_de_passe,
      deconnexion,
      modifier_visiteur,
      detail_visiteur,)

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

path(
    'visiteur/<int:visiteur_id>/modifier/',
    modifier_visiteur,
    name='modifier_visiteur'
),

path(
    'visiteur/<int:visiteur_id>/',
    detail_visiteur,
    name='detail_visiteur'
),

path(
    'services/',
    gestion_services,
    name='gestion_services'
),

path(
    'services/ajouter/',
    ajouter_service,
    name='ajouter_service'
),

path(
    'services/<int:service_id>/modifier/',
    modifier_service,
    name='modifier_service'
),

path(
    'utilisateurs/',
    gestion_utilisateurs,
    name='gestion_utilisateurs'
),

path(
    'utilisateurs/ajouter/',
    ajouter_utilisateur,
    name='ajouter_utilisateur'
),

path(
    'utilisateurs/<int:utilisateur_id>/modifier/',
    modifier_utilisateur,
    name='modifier_utilisateur'
),

path(
    'utilisateurs/<int:utilisateur_id>/mot-de-passe/',
    reinitialiser_mot_de_passe,
    name='reinitialiser_mot_de_passe'
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )