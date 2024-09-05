from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib import messages
from .form import *
from .models import Utilisateur, Programme, Session, Candidat

def acceuil(request):
    return render(request, 'acceuil.html')

# CREATE

def create_utilisateur(request, role):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)  # Ne pas enregistrer tout de suite
            utilisateur.role = role  # Définir le rôle en fonction du paramètre
            utilisateur.save()  # Enregistrer l'utilisateur avec le rôle défini
            messages.success(request, f"Utilisateur {role} créé avec succès.")
            return redirect('list_utilisateurs')
    else:
        form = UtilisateurForm(initial={'role': role})  # Pré-remplir le formulaire avec le rôle

    return render(request, 'creer.html', {'form': form, 'role': role})

def create_programme(request):
    if request.method == 'POST':
        form = ProgrammeForm(request.POST,request.FILES,)
        if form.is_valid():
            form.save()
            messages.success(request, "Programme créé avec succès.")
            return redirect('list_programmes')
    else:
        form = ProgrammeForm()
    return render(request, 'creer.html', {'form': form})

def create_domaine(request):
    if request.method == 'POST':
        form = DomaineForm(request.POST,request.FILES,)
        if form.is_valid():
            form.save()
            messages.success(request, "Domaine créé avec succès.")
            return redirect('list_domaines')
    else:
        form = DomaineForm()
    return render(request, 'creer.html', {'form': form})

def create_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Session créée avec succès.")
            return redirect('list_sessions')
    else:
        form = SessionForm()
    return render(request, 'creer.html', {'form': form})

def inscription(request):
    if request.method == 'POST':
        try:
            utilisateur = Utilisateur.objects.get(username=request.POST['username'])
            form = CandidatForm(request.POST, instance=utilisateur)
            utilisateur.status = None
        except Utilisateur.DoesNotExist:
            form = CandidatForm(request.POST)

        if form.is_valid():
            form.save()
            if form.instance.pk:
                messages.success(request, "Demande d'admission envoyé avec succès...")
            else:
                messages.success(request, "Demande d'admission envoyé avec succès...")
            return redirect('acceuil')
    else:
        form = CandidatForm()
    return render(request, 'inscription.html', {'form': form})

def load_domaines(request):
    programme_ids = request.GET.getlist('programme_ids[]')
    domaines = Domaine.objects.filter(programme__id__in=programme_ids)
    return JsonResponse(list(domaines.values('id', 'code_programme')), safe=False)

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Vérifier si l'utilisateur existe dans la base de données
        try:
            user = Utilisateur.objects.get(username=username)
        except Utilisateur.DoesNotExist:
            user = None

        if user is not None:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                if authenticated_user.role=='Etudiant':
                    return redirect('acceuil')
                elif authenticated_user.role=='Enseignant':
                    return redirect('acceuil')
                if authenticated_user.role=='Admin':
                    return redirect('list_utilisateurs')
                if authenticated_user.role=='Candidat':
                    return redirect('acceuil')
                else:
                    return redirect('acceuil')
            else:
                # Si l'utilisateur existe mais avec un mot de passe incorrect
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            # Si l'utilisateur n'existe pas dans la base de données
            messages.info(request, "Vous devez d'abord faire une demande d'admission.")
    return render(request, 'login.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

# READ

def list_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'list_utilisateurs.html', {'utilisateurs': utilisateurs})

def list_utilisateurs_par_role(request, role):
    utilisateurs = Utilisateur.objects.filter(role=role)
    return render(request, 'list_utilisateurs.html', {'utilisateurs': utilisateurs, 'role': role})

def list_programmes(request):
    programmes = Programme.objects.all()
    return render(request, 'list_programmes.html', {'programmes': programmes})

def list_domaines(request):
    domaines = Domaine.objects.all()
    return render(request, 'list_domaines.html', {'domaines': domaines})


def list_sessions(request):
    sessions = Session.objects.all()
    return render(request, 'list_sessions.html', {'sessions': sessions})

def list_candidats(request):
    candidats = Candidat.objects.all()
    return render(request, 'list_candidats.html', {'candidats': candidats})

# UPDATE

def update_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    if request.method == 'POST':
        form = UtilisateurChangeForm(request.POST,request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur mis à jour avec succès.")
            return redirect('list_utilisateurs')
    else:
        form = UtilisateurChangeForm(instance=utilisateur)
    return render(request, 'update.html', {'form': form})



def update_programme(request, id):
    programme = get_object_or_404(Programme, id=id)
    if request.method == 'POST':
        form = ProgrammeForm(request.POST,request.FILES, instance=programme)
        if form.is_valid():
            form.save()
            messages.success(request, "Programme mis à jour avec succès.")
            return redirect('list_programmes')
    else:
        form = ProgrammeForm(instance=programme)
    return render(request, 'update.html', {'form': form})

def update_domaine(request, id):
    domaine = get_object_or_404(Domaine, id=id)
    if request.method == 'POST':
        form = DomaineForm(request.POST,request.FILES, instance=domaine)
        if form.is_valid():
            form.save()
            messages.success(request, "Domaine mis à jour avec succès.")
            return redirect('list_domaines')
    else:
        form = DomaineForm(instance=domaine)
    return render(request, 'update.html', {'form': form})

def update_session(request, id):
    session = get_object_or_404(Session, id=id)
    if request.method == 'POST':
        form = SessionForm(request.POST,request.FILES, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session mise à jour avec succès.")
            return redirect('list_sessions')
    else:
        form = SessionForm(instance=session)
    return render(request, 'update.html', {'form': form})

def update_candidat(request, id):
    candidat = get_object_or_404(Candidat, id=id)
    if request.method == 'POST':
        form = CandidatForm(request.POST,request.FILES, instance=candidat)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidat mis à jour avec succès.")
            return redirect('list_candidats')
    else:
        form = CandidatForm(instance=candidat)
    return render(request, 'update.html', {'form': form})

# DELETE

def delete_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
        return redirect('list_utilisateurs')
    return render(request, 'delete_utilisateur.html', {'utilisateur': utilisateur})

def delete_programme(request, id):
    programme = get_object_or_404(Programme, id=id)
    if request.method == 'POST':
        programme.delete()
        messages.success(request, "Programme supprimé avec succès.")
        return redirect('list_programmes')
    return render(request, 'delete_programme.html', {'programme': programme})

def delete_domaine(request, id):
    domaine = get_object_or_404(Domaine, id=id)
    if request.method == 'POST':
        domaine.delete()
        messages.success(request, "Domaine supprimé avec succès.")
        return redirect('list_programmes')
    return render(request, 'delete_domaine.html', {'domaine': domaine})


def delete_session(request, id):
    session = get_object_or_404(Session, id=id)
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Session supprimée avec succès.")
        return redirect('list_sessions')
    return render(request, 'delete_session.html', {'session': session})

def delete_candidat(request, id):
    candidat = get_object_or_404(Candidat, id=id)
    if request.method == 'POST':
        candidat.delete()
        messages.success(request, "Candidat supprimé avec succès.")
        return redirect('list_candidats')
    return render(request, 'delete_candidat.html', {'candidat': candidat})

def envoyer_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, expéditeur=request.user)
        if form.is_valid():
            form.save()
            return redirect('afficher_messages')
    else:
        form = MessageForm(expéditeur=request.user)

    return render(request, 'envoyer_message.html', {'form': form})

def afficher_messages(request):
    messages = Message.objects.filter(destinataire=request.user).order_by('-date_envoi')
    return render(request, 'afficher_messages.html', {'messages': messages})

def lire_message(request, id):
    message = get_object_or_404(Message, id=id, destinataire=request.user)
    if not message.lu:
        message.lu = True
        message.save()
    return render(request, 'lire_message.html', {'message': message})

def supprimer_message(request, id):
    message = get_object_or_404(Message, id=id, destinataire=request.user)
    message.delete()
    return redirect('afficher_messages')

def accepter_candidat(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id, role='Candidat')
    
    # Vérifier si le candidat a sélectionné plus d'un programme
    if utilisateur.programme.count() > 1:
        if request.method == 'POST':
            form = ProgrammeChoiceForm(request.POST, programmes=utilisateur.programme.all())
            if form.is_valid():
                programme_choisi = form.cleaned_data['programme']
                utilisateur.programme.set([programme_choisi])  # Assigner uniquement le programme choisi
                utilisateur.status = True
                utilisateur.role = 'Etudiant'
                utilisateur.save()

                # Envoyer un message au candidat
                Message.objects.create(
                    expéditeur=request.user,
                    destinataire=utilisateur,
                    sujet="Demande d'admission acceptée",
                    contenu=f"Félicitations ! Votre demande d'admission a été acceptée et vous avez été inscrit dans le programme : {programme_choisi.intitule}. Bienvenue en tant qu'étudiant."
                )

                return redirect('list_utilisateurs')
        else:
            form = ProgrammeChoiceForm(programmes=utilisateur.programme.all())
        
        return render(request, 'accepter_candidat.html', {'form': form, 'utilisateur': utilisateur})
    
    # Sinon, accepter directement le candidat avec le seul programme choisi
    utilisateur.status = True  # Statut accepté
    utilisateur.role = 'Etudiant'  # Changer le rôle en 'Étudiant'
    utilisateur.save()

    # Envoyer un message au candidat
    Message.objects.create(
        expéditeur=request.user,  # L'admin connecté est l'expéditeur
        destinataire=utilisateur,
        sujet="Demande d'admission acceptée",
        contenu="Félicitations ! Votre demande d'admission a été acceptée. Bienvenue en tant qu'étudiant."
    )

    return redirect('list_utilisateurs')

def refuser_candidat(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id, role='Candidat')
    utilisateur.status = False  
    utilisateur.save()

    # Envoyer un message au candidat
    Message.objects.create(
        expéditeur=request.user,  # L'admin connecté est l'expéditeur
        destinataire=utilisateur,
        sujet="Demande d'admission refusée",
        contenu="Nous regrettons de vous informer que votre demande d'admission a été refusée."
    )

    return redirect('list_utilisateurs')  

def profil_utilisateur(request):
    utilisateur = request.user  # Obtenir l'utilisateur connecté

    if request.method == 'POST':
        if 'modifier' in request.POST:
            # Utiliser CandidatForm si l'utilisateur est un candidat, sinon UtilisateurChangeForm
            if utilisateur.role == 'Candidat':
                form = CandidatForm(request.POST, request.FILES, instance=utilisateur)
            else:
                form = UtilisateurChangeForm(request.POST, request.FILES, instance=utilisateur)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Vos informations ont été mises à jour avec succès.")
                return redirect('profil_utilisateur')  # Redirection vers la page de profil pour visualisation après la mise à jour

        elif 'supprimer' in request.POST:
            utilisateur.delete()
            messages.success(request, "Votre compte a été supprimé avec succès.")
            return redirect('acceuil')  # Rediriger vers la page d'accueil après suppression du compte
    else:
        if utilisateur.role == 'Candidat':
            form = CandidatForm(instance=utilisateur)
        else:
            form = UtilisateurChangeForm(instance=utilisateur)

    return render(request, 'profil_utilisateur.html', {'form': form,  'is_editing': 'edit' in request.GET})