from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib import messages
from .form import *
from .models import *
from cours_app.models import *

def acceuil(request):
    enseignants = Utilisateur.objects.filter(role='Enseignant')
    etudiants = Utilisateur.objects.filter(role='Etudiant')
    cours = Cours.objects.all()
    return render(request, 'acceuil.html', {'enseignants': enseignants, 'etudiants': etudiants, 'cours': cours})

def contact(request):
    return render(request, 'contact.html')

def cours(request):
    cours_liste = Cours.objects.all()  # Récupérer tous les cours
    return render(request, 'courses.html', {'cours_liste': cours_liste})

def blog(request):
    return render(request, 'blog.html')

def about(request):
    return render(request, 'about.html')

def personnel(request):
    enseignants = Utilisateur.objects.filter(role='Enseignant')  # Filtrer les utilisateurs avec le rôle 'Enseignant'
    return render(request, 'teacher.html', {'enseignants': enseignants})

# CREATE

def create_utilisateur(request, role):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, request.FILES)
        if form.is_valid():
            utilisateur = form.save(commit=False)  # Ne pas enregistrer tout de suite
            utilisateur.role = role  # Définir le rôle en fonction du paramètre
            utilisateur.save()  # Enregistrer l'utilisateur avec le rôle défini

            # Assigner les programmes sélectionnés
            programmes = form.cleaned_data['programme']
            utilisateur.programme.set(programmes)

            # Assigner les domaines sélectionnés
            domaines = form.cleaned_data['domaine']
            utilisateur.domaine.set(domaines)

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
        form = CandidatForm(request.POST, request.FILES)
        if form.is_valid():
            # Créez un utilisateur temporaire mais ne le marquez pas comme inscrit
            utilisateur = form.save(commit=False)
            utilisateur.role = 'Candidat'
            utilisateur.save()

            # Enregistrez les fichiers directement sur l'utilisateur
            if 'diplome' in request.FILES:
                utilisateur.diplome = request.FILES['diplome']
            if 'passport' in request.FILES:
                utilisateur.passport = request.FILES['passport']
            
            # Enregistrez également les programmes et le domaine
            programmes_selectionnes = form.cleaned_data.get('programme')
            domaine_selectionne = form.cleaned_data.get('domaine')

            if programmes_selectionnes:
                utilisateur.programme.set(programmes_selectionnes)
            if domaine_selectionne:
                utilisateur.domaine.set([domaine_selectionne])

            # Sauvegarder l'utilisateur, mais ne pas activer sa candidature tant que le paiement n'est pas confirmé
            utilisateur.save()

            # Stocker l'ID de l'utilisateur dans la session pour lier l'inscription après le paiement
            request.session['utilisateur_id'] = utilisateur.id

            # Rediriger vers la page de paiement
            messages.info(request, "Vous devez payer les frais d'admission avant de finaliser votre inscription.")
            return redirect('payer_inscription')  # Rediriger vers la page de paiement
    else:
        form = CandidatForm()

    return render(request, 'inscription.html', {'form': form})


def payer_inscription(request):
    # Récupérer l'utilisateur temporaire stocké dans la session
    utilisateur_id = request.session.get('utilisateur_id')
    
    if not utilisateur_id:
        messages.error(request, "Aucun utilisateur en attente de paiement.")
        return redirect('inscription')  # Rediriger vers la page d'inscription si aucun utilisateur

    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id, role='Candidat')

    # Récupère les frais actuels
    parametres = Frais_admission.objects.first()  
    frais_admission = parametres.montant if parametres else 100.00  # Valeur par défaut si non défini

    context = {
        'utilisateur': utilisateur,
        'frais_admission': format(frais_admission, '.2f')
    }

    # Rendre la page de paiement, même en cas de requête GET
    return render(request, 'payer.html', context)


def paiement_succes_inscription(request):
    # Récupérer l'utilisateur temporaire stocké dans la session
    utilisateur_id = request.session.get('utilisateur_id')
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id, role='Candidat')

    # Marquer l'utilisateur comme ayant payé les frais d'admission
    utilisateur.frais_paye = True
    utilisateur.save()

    # Nettoyer la session après le paiement
    request.session.pop('utilisateur_id', None)

    # Message de succès de paiement
    messages.success(request, "Paiement effectué avec succès. Votre demande d'admission est en cours de traitement.")

    # Message pour informer qu'il peut désormais se connecter
    messages.info(request, f"Vous pouvez maintenant vous connecter avec votre nom d'utilisateur : {utilisateur.username} et le mot de passe que vous avez défini lors de votre demande d'admission.")

    return redirect('acceuil')



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
                # Vérifier si l'utilisateur est un candidat et si le paiement a été effectué
                if authenticated_user.role == 'Candidat' and not authenticated_user.frais_paye:
                    messages.info(request, "Vous devez payer les frais d'admission avant de vous connecter.")
                    return redirect('payer_inscription')

                # Connexion de l'utilisateur et redirection en fonction de son rôle
                login(request, authenticated_user)
                if authenticated_user.role == 'Etudiant':
                    return redirect('mes_cours_etudiant')
                elif authenticated_user.role == 'Enseignant':
                    return redirect('mes_cours_professeur')
                elif authenticated_user.role == 'Admin':
                    return redirect('list_utilisateurs')
                elif authenticated_user.role == 'Candidat':
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
            messages.success(request, "Message envoyé avec succès.")
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
    # Récupérer l'utilisateur en question (candidat)
    utilisateur = get_object_or_404(Utilisateur, id=user_id, role='Candidat')

    if request.method == 'POST':
        # Récupérer le commentaire soumis dans le formulaire
        commentaire = request.POST.get('comment', '')

        # Mettre à jour le statut du candidat à "refusé" (False)
        utilisateur.status = False
        utilisateur.save()

        # Créer et envoyer un message au candidat avec la raison du rejet
        Message.objects.create(
            expéditeur=request.user,  # L'admin connecté en tant qu'expéditeur
            destinataire=utilisateur,  # Le candidat comme destinataire
            sujet="Demande d'admission refusée",
            contenu=f"Nous regrettons de vous informer que votre demande d'admission a été refusée. Raison : {commentaire}"
        )

        # Ajouter un message de succès pour l'administrateur
        messages.success(request, "Le candidat a été rejeté avec succès.")

    # Redirection vers la liste des utilisateurs après la soumission du formulaire
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
            return redirect('acceuil')  
    else:
        if utilisateur.role == 'Candidat':
            form = CandidatForm(instance=utilisateur)
        else:
            form = UtilisateurChangeForm(instance=utilisateur)

    return render(request, 'profil_utilisateur.html', {'form': form,  'is_editing': 'edit' in request.GET})

def changer_frais_admission(request):
    parametres, created = Frais_admission.objects.get_or_create(id=1) 

    if request.method == 'POST':
        form = FraisInscriptionForm(request.POST, instance=parametres)
        if form.is_valid():
            form.save()
            return redirect('list_utilisateurs')  
    else:
        form = FraisInscriptionForm(instance=parametres)

    return render(request, 'changer_frais.html', {'form': form})