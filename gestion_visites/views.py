from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .decorators import role_required

from .models import Visite,Visiteur, Service
from django.db.models import Q


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
            
        if utilisateur.is_superuser:
                return redirect('dashboard_admin')

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

@login_required
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
    
    total_visiteurs = Visiteur.objects.count()

    dernieres_visites = Visite.objects.select_related(
        'visiteur',
        'service'
    ).order_by('-date_heure_entree')[:5]

    contexte = {
        'visites_presentes': visites_presentes,
        'visites_aujourd_hui': visites_aujourd_hui,
        'sorties_aujourd_hui': sorties_aujourd_hui,
        'dernieres_visites': dernieres_visites,
        'total_visiteurs': total_visiteurs,
    }

    return render(
        request,
        'gestion_visites/dashboard_agent.html',
        contexte
    )


@login_required
@role_required('ADMINISTRATEUR')
def dashboard_admin(request):

    total_visiteurs = Visiteur.objects.count()

    total_visites = Visite.objects.count()

    visites_presentes = Visite.objects.filter(
        statut=Visite.StatutVisite.PRESENT
    ).count()

    total_services = Service.objects.count()

    contexte = {
        'total_visiteurs': total_visiteurs,
        'total_visites': total_visites,
        'visites_presentes': visites_presentes,
        'total_services': total_services,
    }

    return render(
        request,
        'gestion_visites/dashboard_admin.html',
        contexte
    )
    
    
@login_required
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

        if request.user.is_superuser or request.user.groups.filter(
    name='ADMINISTRATEUR'
).exists():
           return redirect('dashboard_admin')

           return redirect('dashboard_agent')

    return render(
        request,
        'gestion_visites/enregistrer_visite.html',
        {
            'services': services
        }
    )
@login_required
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
@login_required
def enregistrer_sortie(request, visite_id):

    visite = Visite.objects.get(
        id=visite_id,
        statut=Visite.StatutVisite.PRESENT
    )

    visite.date_heure_sortie = timezone.now()
    visite.statut = Visite.StatutVisite.SORTI
    visite.save()

    return redirect('visites_en_cours')   

@login_required
def historique_visites(request):

    recherche = request.GET.get('recherche', '').strip()
    service_id = request.GET.get('service', '').strip()
    statut = request.GET.get('statut', '').strip()

    visites = Visite.objects.all().select_related(
        'visiteur',
        'service'
    )

    if recherche:
        visites = visites.filter(
            Q(visiteur__nom__icontains=recherche) |
            Q(visiteur__prenom__icontains=recherche) |
            Q(visiteur__telephone__icontains=recherche) |
            Q(visiteur__numero_piece__icontains=recherche) |
            Q(service__nom__icontains=recherche) |
            Q(motif__icontains=recherche)
        )

    if service_id:
        visites = visites.filter(
            service_id=service_id
        )
        
    if statut:
        visites = visites.filter(
        statut=statut
    )

    visites = visites.order_by('-date_heure_entree')

    services = Service.objects.filter(
        statut=True
    ).order_by('nom')

    return render(
        request,
        'gestion_visites/historique.html',
        {
            'visites': visites,
            'recherche': recherche,
            'services': services,
            'service_id': service_id,
            'statut': statut
        }
    )
@login_required
def liste_visiteurs(request):

    recherche = request.GET.get('recherche', '').strip()

    visiteurs = Visiteur.objects.all()

    if recherche:
        visiteurs = visiteurs.filter(
            Q(nom__icontains=recherche) |
            Q(prenom__icontains=recherche) |
            Q(telephone__icontains=recherche) |
            Q(numero_piece__icontains=recherche)
        )

    visiteurs = visiteurs.order_by('nom', 'prenom')

    return render(
        request,
        'gestion_visites/visiteurs.html',
        {
            'visiteurs': visiteurs,
            'recherche': recherche
        }
    )
    
@login_required
def modifier_visiteur(request, visiteur_id):

    visiteur = Visiteur.objects.get(id=visiteur_id)

    if request.method == 'POST':

        visiteur.nom = request.POST.get('nom')
        visiteur.prenom = request.POST.get('prenom')
        visiteur.telephone = request.POST.get('telephone')
        visiteur.type_piece = request.POST.get('type_piece')
        visiteur.numero_piece = request.POST.get('numero_piece')

        visiteur.save()

        return redirect('liste_visiteurs')

    return render(
        request,
        'gestion_visites/modifier_visiteur.html',
        {
            'visiteur': visiteur
        }
    )
    
@login_required
def detail_visiteur(request, visiteur_id):

    visiteur = Visiteur.objects.get(id=visiteur_id)

    visites = Visite.objects.filter(
        visiteur=visiteur
    ).select_related(
        'service'
    ).order_by(
        '-date_heure_entree'
    )

    return render(
        request,
        'gestion_visites/detail_visiteur.html',
        {
            'visiteur': visiteur,
            'visites': visites
        }
    )
    
@login_required
@role_required('ADMINISTRATEUR')
def gestion_services(request):

    services = Service.objects.all().order_by('nom')

    return render(
        request,
        'gestion_visites/gestion_services.html',
        {
            'services': services
        }
    )        
    
@login_required
@role_required('ADMINISTRATEUR')
def ajouter_service(request):

    if request.method == 'POST':

        nom = request.POST.get('nom')
        description = request.POST.get('description')

        Service.objects.create(
            nom=nom,
            description=description,
            statut=True
        )

        return redirect('gestion_services')

    return render(
        request,
        'gestion_visites/ajouter_service.html'
    )  
    
@login_required
@role_required('ADMINISTRATEUR')
def modifier_service(request, service_id):

    service = Service.objects.get(id=service_id)

    if request.method == 'POST':

        service.nom = request.POST.get('nom')
        service.description = request.POST.get('description')
        service.statut = request.POST.get('statut') == 'on'

        service.save()

        return redirect('gestion_services')

    return render(
        request,
        'gestion_visites/modifier_service.html',
        {
            'service': service
        }
    )  
    
@login_required
@role_required('ADMINISTRATEUR')
def gestion_utilisateurs(request):

    utilisateurs = User.objects.all().order_by('username')

    return render(
        request,
        'gestion_visites/gestion_utilisateurs.html',
        {
            'utilisateurs': utilisateurs
        }
    )
    
@login_required
@role_required('ADMINISTRATEUR')
def ajouter_utilisateur(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'

        if password != password_confirmation:
            return render(
                request,
                'gestion_visites/ajouter_utilisateur.html',
                {
                    'erreur': 'Les mots de passe ne correspondent pas.'
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'gestion_visites/ajouter_utilisateur.html',
                {
                    'erreur': 'Ce nom d’utilisateur existe déjà.'
                }
            )

        utilisateur = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        utilisateur.is_active = is_active
        utilisateur.save()

        if role == 'ADMINISTRATEUR':
            groupe = Group.objects.get(name='ADMINISTRATEUR')
            utilisateur.groups.add(groupe)

        elif role == 'AGENT_ACCUEIL':
            groupe = Group.objects.get(name='AGENT_ACCUEIL')
            utilisateur.groups.add(groupe)

        return redirect('gestion_utilisateurs')

    return render(
        request,
        'gestion_visites/ajouter_utilisateur.html'
    ) 
    
@login_required
@role_required('ADMINISTRATEUR')
def modifier_utilisateur(request, utilisateur_id):

    utilisateur = User.objects.get(id=utilisateur_id)

    if request.method == 'POST':

        utilisateur.first_name = request.POST.get('first_name')
        utilisateur.last_name = request.POST.get('last_name')

        role = request.POST.get('role')
        utilisateur.is_active = request.POST.get('is_active') == 'on'

        utilisateur.groups.clear()

        if role == 'ADMINISTRATEUR':
            groupe = Group.objects.get(name='ADMINISTRATEUR')
            utilisateur.groups.add(groupe)

        elif role == 'AGENT_ACCUEIL':
            groupe = Group.objects.get(name='AGENT_ACCUEIL')
            utilisateur.groups.add(groupe)

        utilisateur.save()

        return redirect('gestion_utilisateurs')

    return render(
        request,
        'gestion_visites/modifier_utilisateur.html',
        {
            'utilisateur': utilisateur
        }
    )
    
@login_required
@role_required('ADMINISTRATEUR')
def reinitialiser_mot_de_passe(request, utilisateur_id):

    utilisateur = User.objects.get(id=utilisateur_id)

    if request.method == 'POST':

        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password != password_confirmation:
            return render(
                request,
                'gestion_visites/reinitialiser_mot_de_passe.html',
                {
                    'utilisateur': utilisateur,
                    'erreur': 'Les mots de passe ne correspondent pas.'
                }
            )

        utilisateur.set_password(password)
        utilisateur.save()

        return redirect('gestion_utilisateurs')

    return render(
        request,
        'gestion_visites/reinitialiser_mot_de_passe.html',
        {
            'utilisateur': utilisateur
        }
    )               
        

def deconnexion(request):
    logout(request)
    return redirect('connexion')