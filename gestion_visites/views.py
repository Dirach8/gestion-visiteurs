from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth import logout

from .models import Visite,Visiteur, Service


def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        utilisateur = authenticate(
            request,
            username=username,
            password=password
        )

        if utilisateur is not None:
            login(request, utilisateur)

            if utilisateur.groups.filter(name='AGENT_ACCUEIL').exists():
                return redirect('dashboard_agent')

            if utilisateur.groups.filter(name='ADMINISTRATEUR').exists():
                return redirect('dashboard_admin')

            return redirect('/admin/')

        return render(
            request,
            'gestion_visites/login.html',
            {
                'erreur': 'Nom d’utilisateur ou mot de passe incorrect.'
            }
        )

    return render(request, 'gestion_visites/login.html')


def dashboard_agent(request):
    visites_presentes = Visite.objects.filter(
        statut=Visite.StatutVisite.PRESENT
    ).count()

    visites_aujourd_hui = Visite.objects.filter(
        date_heure_entree__date=timezone.now().date()
    ).count()

    sorties_aujourd_hui = Visite.objects.filter(
        date_heure_sortie__date=timezone.now().date()
    ).count()

    dernieres_visites = Visite.objects.select_related(
        'visiteur',
        'service'
    ).order_by('-date_heure_entree')[:5]

    contexte = {
        'visites_presentes': visites_presentes,
        'visites_aujourd_hui': visites_aujourd_hui,
        'sorties_aujourd_hui': sorties_aujourd_hui,
        'dernieres_visites': dernieres_visites,
    }

    return render(
        request,
        'gestion_visites/dashboard_agent.html',
        contexte
    )


def dashboard_admin(request):
    return render(
        request,
        'gestion_visites/dashboard_admin.html'
    )

def enregistrer_visite(request):

    services = Service.objects.filter(statut=True)

    if request.method == 'POST':

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        type_piece = request.POST.get('type_piece')
        numero_piece = request.POST.get('numero_piece')

        service_id = request.POST.get('service')
        motif = request.POST.get('motif')
        observation = request.POST.get('observation')

        visiteur, created = Visiteur.objects.get_or_create(
    numero_piece=numero_piece,
    defaults={
        'nom': nom,
        'prenom': prenom,
        'telephone': telephone,
        'type_piece': type_piece,
    }
)

        service = Service.objects.get(id=service_id)

        Visite.objects.create(
            visiteur=visiteur,
            service=service,
            enregistre_par=request.user,
            motif=motif,
            observation=observation,
            date_heure_entree=timezone.now(),
            statut=Visite.StatutVisite.PRESENT
        )

        return redirect('dashboard_agent')

    return render(
        request,
        'gestion_visites/enregistrer_visite.html',
        {
            'services': services
        }
    )

def visites_en_cours(request):
    visites = Visite.objects.filter(
        statut=Visite.StatutVisite.PRESENT
    ).select_related(
        'visiteur',
        'service'
    ).order_by('-date_heure_entree')

    return render(
        request,
        'gestion_visites/visites_en_cours.html',
        {
            'visites': visites
        }
    )

def enregistrer_sortie(request, visite_id):

    visite = Visite.objects.get(
        id=visite_id,
        statut=Visite.StatutVisite.PRESENT
    )

    visite.date_heure_sortie = timezone.now()
    visite.statut = Visite.StatutVisite.SORTI
    visite.save()

    return redirect('visites_en_cours')   


def historique_visites(request):

    visites = Visite.objects.all().select_related(
        'visiteur',
        'service'
    ).order_by('-date_heure_entree')

    return render(
        request,
        'gestion_visites/historique.html',
        {
            'visites': visites
        }
    )

def liste_visiteurs(request):

    visiteurs = Visiteur.objects.all().order_by('nom', 'prenom')

    return render(
        request,
        'gestion_visites/visiteurs.html',
        {
            'visiteurs': visiteurs
        }
    )

def deconnexion(request):
    logout(request)
    return redirect('connexion')