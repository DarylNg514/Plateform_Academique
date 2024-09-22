from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
import random  
from django.http import FileResponse
from collections import defaultdict
from auth_app.models import *
from .models import *
from auth_app.form import *
from .form import *


# Liste des groupes
def list_groupes(request):
    groupes = Groupe.objects.all()
    return render(request, 'list_groupes.html', {'groupes': groupes})

# Créer un groupe
def create_groupe(request):
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le groupe a été créé avec succès.')
            return redirect('list_groupes')
    else:
        form = GroupeForm()
    return render(request, 'create_groupe.html', {'form': form})

# Mettre à jour un groupe
def update_groupe(request, id):
    groupe = get_object_or_404(Groupe, id=id)
    if request.method == 'POST':
        form = GroupeForm(request.POST, instance=groupe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le groupe a été mis à jour avec succès.')
            return redirect('list_groupes')
    else:
        form = GroupeForm(instance=groupe)
    return render(request, 'update_groupe.html', {'form': form})

# Supprimer un groupe
def delete_groupe(request, id):
    groupe = get_object_or_404(Groupe, id=id)
    if request.method == 'POST':
        groupe.delete()
        messages.success(request, 'Le groupe a été supprimé avec succès.')
        return redirect('list_groupes')
    return render(request, 'delete_groupe.html', {'groupe': groupe})

# Vue pour créer une salle
def creer_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle créée avec succès.")
            return redirect('list_salles')
    else:
        form = SalleForm()
    return render(request, 'creer_salle.html', {'form': form})

# Vue pour lister toutes les salles
def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'list_salles.html', {'salles': salles})

# Vue pour mettre à jour une salle
def mettre_a_jour_salle(request, id):
    salle = get_object_or_404(Salle, id=id)
    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle mise à jour avec succès.")
            return redirect('list_salles')
    else:
        form = SalleForm(instance=salle)
    return render(request, 'update_salle.html', {'form': form})

# Vue pour supprimer une salle
def supprimer_salle(request, id):
    salle = get_object_or_404(Salle, id=id)
    if request.method == 'POST':
        salle.delete()
        messages.success(request, "Salle supprimée avec succès.")
        return redirect('list_salles')
    return render(request, 'delete_salle.html', {'salle': salle})


def list_cours(request):
    utilisateur = request.user
    
    # Récupérer tous les cours pour les administrateurs
    if utilisateur.role == 'Admin':
        cours_liste = Cours.objects.all()
    
    # Filtrer les cours pour les étudiants
    elif utilisateur.role == 'Etudiant':
        cours_liste = Cours.objects.filter(
            programme__in=utilisateur.programme.all(),
            domaine__in=utilisateur.domaine.all(),
            session=utilisateur.session
        ).distinct()
        
    # Filtrer les cours pour les enseignants
    elif utilisateur.role == 'Enseignant':
        cours_liste = Cours.objects.filter(
            attributions__professeur=utilisateur
        ).distinct()
        
    # Par défaut, retourner une liste vide si le rôle ne correspond à aucun cas
    else:
        cours_liste = Cours.objects.none()
        
    return render(request, 'list_cours.html', {'cours_liste': cours_liste})


def create_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours ajouté avec succès.")
            return redirect('list_cours')
    else:
        form = CoursForm()
    return render(request, 'cours_form.html', {'form': form})

def update_cours(request, id):
    cours = get_object_or_404(Cours, id=id)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours mis à jour avec succès.")
            return redirect('list_cours')
    else:
        form = CoursForm(instance=cours)
    return render(request, 'update_cours.html', {'form': form})

def delete_cours(request, id):
    cours = get_object_or_404(Cours, id=id)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, "Cours supprimé avec succès.")
        return redirect('list_cours')
    return render(request, 'delete_cours.html', {'cours': cours})

def assigner_professeur(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    enseignants = Utilisateur.objects.filter(role='Enseignant')
    groupes = Groupe.objects.all()  # Récupérer tous les groupes

    if request.method == 'POST':
        enseignant_id = request.POST.get('enseignant')
        enseignant = get_object_or_404(Utilisateur, id=enseignant_id)
        groupe_id = request.POST.get('groupe')  # Récupérer l'ID du groupe depuis le formulaire
        groupe = get_object_or_404(Groupe, id=groupe_id)

        # Vérifier si une attribution existe déjà pour ce cours, professeur et groupe
        attribution_existante = Attribution.objects.filter(cours=cours, professeur=enseignant, groupe=groupe).first()

        if attribution_existante:
            messages.info(request, f"Le professeur {enseignant.nom} est déjà attribué au cours {cours.sigle} dans le groupe {groupe.nogroupe}.")
        else:
            # Créer une nouvelle attribution avec le groupe spécifié
            Attribution.objects.create(cours=cours, professeur=enseignant, groupe=groupe)
            messages.success(request, f"Le professeur {enseignant.nom} a été attribué au cours {cours.sigle} dans le groupe {groupe.nogroupe}.")

        return redirect('list_cours')

    return render(request, 'assigner_professeur.html', {'cours': cours, 'enseignants': enseignants, 'groupes': groupes})


def mes_cours_etudiant(request):
    etudiant = request.user
    if etudiant.role != 'Etudiant':
        return redirect('acceuil')  # Rediriger si l'utilisateur n'est pas un étudiant

    # Récupérer le groupe de l'étudiant
    groupe = etudiant.inscriptions.first().groupe if etudiant.inscriptions.exists() else None
    
    # Liste des cours auxquels l'étudiant est inscrit dans son groupe et qui ne sont pas abandonnés
    if groupe:
        cours_liste = Cours.objects.filter(
            inscriptions__etudiant=etudiant, 
            inscriptions__groupe=groupe, 
            inscriptions__abandonne=False
        ).distinct()
    else:
        cours_liste = Cours.objects.none()  # Aucun cours si l'étudiant n'a pas de groupe associé

    return render(request, 'mes_cours_etudiant.html', {'cours_liste': cours_liste})

# Annulation/Abandon de cours
def abandonner_cours(request, cours_id):
    # Récupérer l'inscription correspondante pour l'étudiant connecté et le cours en question
    inscription = get_object_or_404(Inscription, cours_id=cours_id, etudiant=request.user)
    if request.method == 'POST':
        inscription.abandonne = True
        inscription.save()
        messages.success(request, "Cours abandonné avec succès.")
        return redirect('mes_cours_etudiant')
    return render(request, 'annuler_cours.html', {'inscription': inscription})

    
def mes_cours_professeur(request):
    professeur = request.user
    if professeur.role != 'Enseignant':
        return redirect('acceuil')  # Rediriger si l'utilisateur n'est pas un professeur

    # Récupérer les cours enseignés par le professeur dans les groupes auxquels il est associé
    cours_liste = Cours.objects.filter(attributions__professeur=professeur).distinct()

    # Dictionnaire pour stocker les cours, les groupes associés et les étudiants inscrits paginés
    cours_etudiants_pagination = {}
    cours_groupes = {}  # Dictionnaire pour stocker les groupes associés à chaque cours
    for cours in cours_liste:
        # Récupérer les groupes associés au professeur pour ce cours
        groupes = professeur.attributions.filter(cours=cours).values_list('groupe__nom_groupe', flat=True).distinct()
        cours_groupes[cours.id] = ", ".join(groupes)

        # Récupérer les étudiants non abandonnés inscrits au cours et au même groupe que le professeur
        etudiants = Inscription.objects.filter(
            cours=cours, 
            groupe__in=professeur.attributions.filter(cours=cours).values_list('groupe', flat=True),
            abandonne=False
        ).select_related('etudiant')

        # Créer un objet Paginator
        paginator = Paginator(etudiants, 10)  # 10 étudiants par page

        # Obtenir le numéro de page depuis les paramètres GET
        page_number = request.GET.get(f'page_{cours.id}', 1)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Ajouter la page actuelle au dictionnaire avec le cours correspondant
        cours_etudiants_pagination[cours] = page_obj

    return render(request, 'mes_cours_professeur.html', {
        'cours_etudiants_pagination': cours_etudiants_pagination,
        'cours_groupes': cours_groupes,  # Passer les groupes au template
        'professeur': professeur
    })

    
def voir_etudiant(request, etudiant_id):
    # Récupérer l'étudiant spécifié par l'ID
    etudiant = get_object_or_404(Utilisateur, id=etudiant_id, role='Etudiant')

    # Récupérer l'utilisateur connecté
    utilisateur_connecte = request.user

    # Vérifier si l'utilisateur a le droit de consulter les informations de cet étudiant
    if utilisateur_connecte.role == 'Admin' or utilisateur_connecte == etudiant:
        # L'admin ou l'étudiant lui-même peut voir toutes les informations
        inscriptions = Inscription.objects.filter(etudiant=etudiant, abandonne=False).select_related('cours', 'groupe')
    elif utilisateur_connecte.role == 'Enseignant':
        # Le professeur peut voir les cours qu'il enseigne et les étudiants de son groupe
        inscriptions = Inscription.objects.filter(
            etudiant=etudiant,
            abandonne=False,
            cours__attributions__professeur=utilisateur_connecte,
            groupe__in=utilisateur_connecte.attributions.values_list('groupe', flat=True)
        ).distinct()
    else:
        # Si l'utilisateur n'est ni admin, ni professeur du cours, ni l'étudiant lui-même
        messages.error(request, "Vous n'êtes pas autorisé à consulter les informations de cet étudiant.")
        return redirect('acceuil')

    # Récupérer les notes obtenues par l'étudiant
    notes = Note.objects.filter(etudiant=etudiant)

    # Passer les informations de l'étudiant, les cours et les notes au template
    return render(request, 'voir_etudiant.html', {
        'etudiant': etudiant,
        'inscriptions': inscriptions,
        'notes': notes
    })

# Vue pour lister les évaluations d'un cours
def liste_evaluations(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    evaluations = Evaluation.objects.filter(cours=cours)
    
    # Vérifier si l'utilisateur est un étudiant
    if request.user.role == 'Etudiant':
        for evaluation in evaluations:
            evaluation.soumission_existante = evaluation.soumissions.filter(etudiant=request.user).exists()
    
    return render(request, 'liste_evaluations.html', {
        'cours': cours,
        'evaluations': evaluations,
        'now': timezone.now()  # Ajouter la date actuelle pour comparaison dans le template
    })
    
# Vue pour créer une évaluation
def create_evaluation(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.cours = cours
            evaluation.save()
            messages.success(request, 'Évaluation ajoutée avec succès.')
            return redirect('mes_cours_professeur')
    else:
        form = EvaluationForm()
    return render(request, 'create_evaluation.html', {'form': form, 'cours': cours})

# Vue pour mettre à jour une évaluation
def update_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Évaluation mise à jour avec succès.')
            return redirect('liste_evaluations', cours_id=evaluation.cours.id)  # Rediriger vers la liste des évaluations du cours
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'update_evaluation.html', {'form': form, 'evaluation': evaluation})

# Vue pour supprimer une évaluation
def delete_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    cours_id = evaluation.cours.id
    if request.method == 'POST':
        evaluation.delete()
        messages.success(request, 'Évaluation supprimée avec succès.')
        return redirect('liste_evaluations', cours_id=cours_id)  # Rediriger vers la liste des évaluations du cours
    return render(request, 'delete_evaluation.html', {'evaluation': evaluation})

def liste_soumissions(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if request.user.role == 'Etudiant':
        return redirect('acceuil')  # Rediriger si l'utilisateur n'est pas un enseignant

    # Récupérer toutes les soumissions pour l'évaluation
    soumissions = SoumissionEvaluation.objects.filter(evaluation=evaluation)
    
    # Récupérer toutes les notes pour l'évaluation
    notes = Note.objects.filter(evaluation=evaluation)
    
    # Créer un dictionnaire des notes avec l'ID de l'étudiant comme clé
    notes_par_etudiant = {note.etudiant.id: note for note in notes}
    
    # Passer le dictionnaire des notes au template
    return render(request, 'liste_soumissions.html', {
        'evaluation': evaluation,
        'soumissions': soumissions,
        'notes_par_etudiant': notes_par_etudiant,  # Dictionnaire des notes par étudiant
    })


def soumettre_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    
    # Vérifier la date limite
    if evaluation.date_limite and evaluation.date_limite < timezone.now():
        messages.error(request, "La date limite de soumission pour cette évaluation est dépassée.")
        return redirect('liste_evaluations', cours_id=evaluation.cours.id)

    # Vérifier si une soumission existe déjà
    soumission = SoumissionEvaluation.objects.filter(evaluation=evaluation, etudiant=request.user).first()

    if request.method == 'POST':
        form = SoumissionEvaluationForm(request.POST, request.FILES, instance=soumission)
        if form.is_valid():
            soumission = form.save(commit=False)
            soumission.evaluation = evaluation
            soumission.etudiant = request.user
            soumission.soumission_effectuee = True
            soumission.save()
            messages.success(request, "Votre soumission a été envoyée avec succès.")
            return redirect('liste_evaluations', cours_id=evaluation.cours.id)
    else:
        form = SoumissionEvaluationForm(instance=soumission)

    return render(request, 'soumettre_evaluation.html', {'form': form, 'evaluation': evaluation, 'soumission': soumission})



# Vue pour lister les documents d'un cours
def liste_documents(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    documents = CoursDocument.objects.filter(cours=cours)

    return render(request, 'liste_documents.html', {'cours': cours, 'documents': documents})

# Vue pour mettre à jour un document de cours
def update_document(request, document_id):
    document = get_object_or_404(CoursDocument, id=document_id)
    if request.method == 'POST':
        form = CoursDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document mis à jour avec succès.')
            return redirect('liste_documents', cours_id=document.cours.id)  # Rediriger vers la liste des documents du cours
    else:
        form = CoursDocumentForm(instance=document)
    return render(request, 'update_document.html', {'form': form, 'document': document})

# Vue pour supprimer un document de cours
def delete_document(request, document_id):
    document = get_object_or_404(CoursDocument, id=document_id)
    cours_id = document.cours.id
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('liste_documents', cours_id=cours_id)  # Rediriger vers la liste des documents du cours
    return render(request, 'delete_document.html', {'document': document})

# Vue pour ajouter un document de cours
def ajouter_document(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    if request.method == 'POST':
        form = CoursDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.cours = cours
            document.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect('mes_cours_professeur')
    else:
        form = CoursDocumentForm()
    return render(request, 'ajouter_document.html', {'form': form, 'cours': cours})

# Vue pour consulter un document par un etudiant
def consulter_document(request, document_id):
    document = get_object_or_404(CoursDocument, id=document_id)

    if request.user.role == 'Etudiant':
        # Enregistrer la consultation du document
        ConsultationDocument.objects.create(document=document, etudiant=request.user)

    # Télécharger ou afficher le document
    return FileResponse(document.fichier, as_attachment=True)

# Vue pour voir ceux qui ont consulter un document par un enseignant
def consultations_document(request, document_id):
    document = get_object_or_404(CoursDocument, id=document_id)
    if request.user.role == 'Etudiant':
        return redirect('acceuil')  # Rediriger si l'utilisateur n'est pas un enseignant

    # Récupérer les consultations pour ce document
    consultations = ConsultationDocument.objects.filter(document=document)

    return render(request, 'consultations_document.html', {
        'document': document,
        'consultations': consultations,
    })

# Vue pour assigner une note à un étudiant
'''def assigner_note(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.evaluation = evaluation
            note.save()
            messages.success(request, 'Note attribuée avec succès.')
            return redirect('mes_cours_professeur')
    else:
        form = NoteForm(initial={'evaluation': evaluation})
    return render(request, 'assigner_note.html', {'form': form, 'evaluation': evaluation})
'''

def list_notes_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    notes = Note.objects.filter(evaluation__cours=cours).select_related('etudiant', 'evaluation')

    return render(request, 'list_notes_cours.html', {'cours': cours, 'notes': notes})

def assigner_note(request, etudiant_id):
    etudiant = get_object_or_404(Utilisateur, id=etudiant_id, role='Etudiant')
    evaluation_id = request.GET.get('evaluation')
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)

    # Vérifier si la note existe déjà
    note, created = Note.objects.get_or_create(evaluation=evaluation, etudiant=etudiant, defaults={'note_obtenue': 0, 'est_attribuee': False})

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, evaluation=evaluation)
        if form.is_valid():
            note = form.save(commit=False)
            note.est_attribuee = True  # Marquer la note comme attribuée
            note.save()
            messages.success(request, f'Note attribuée avec succès pour {etudiant.get_full_name()}')
            return redirect('liste_soumissions', evaluation_id=evaluation.id)
    else:
        form = NoteForm(instance=note, evaluation=evaluation)

    return render(request, 'assigner_note.html', {
        'form': form, 
        'etudiant': etudiant, 
        'evaluation': evaluation, 
        'note_est_attribuee': note.est_attribuee  # Ajouter ce contexte pour le template
    })


def voir_notes_etudiant(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    notes = Note.objects.filter(evaluation__cours=cours, etudiant=request.user)
    return render(request, 'voir_notes_etudiant.html', {
        'cours': cours,
        'notes': notes,
    })


def inscrire_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    etudiant = request.user
    
    # Vérifier si l'utilisateur est bien un étudiant
    if etudiant.role != 'Etudiant':
        messages.error(request, "Vous devez être étudiant pour vous inscrire à un cours.")
        return redirect('list_cours')

    # Vérifier si le cours a des groupes disponibles
    groupes_disponibles = cours.attributions.values_list('groupe', flat=True).distinct()
    if not groupes_disponibles:
        messages.error(request, "Aucun groupe n'est disponible pour ce cours.")
        return redirect('list_cours')

    # Sélectionner un groupe aléatoirement parmi les groupes disponibles
    groupe_assigné = random.choice(groupes_disponibles)
    groupe = Groupe.objects.get(id=groupe_assigné)

    # Vérifier si l'étudiant est déjà inscrit à ce cours dans ce groupe, même si l'inscription est abandonnée
    inscription, created = Inscription.objects.get_or_create(cours=cours, etudiant=etudiant, groupe=groupe)
    
    if created or inscription.abandonne:
        inscription.abandonne = False
        inscription.save()
        messages.success(request, f"Vous êtes maintenant inscrit au cours {cours.sigle} (Groupe: {groupe.nogroupe}).")
    else:
        messages.info(request, f"Vous êtes déjà inscrit à ce cours dans le groupe {groupe.nogroupe}.")

    return redirect('mes_cours_etudiant')


# Consulter les notes pour un étudiant
def consulter_notes(request):
    notes = Note.objects.filter(etudiant=request.user)
    return render(request, 'consulter_notes.html', {'notes': notes})

# Consulter l'horaire et la salle d'un cours
def rechercher_cours(request):
    query = request.GET.get('q', '')
    if query:
        cours = Cours.objects.filter(titre__icontains=query)
    else:
        cours = []
    return render(request, 'rechercher_cours.html', {'cours': cours, 'query': query})

# Créer un nouvel horaire
def create_horaire(request):
    if request.method == 'POST':
        form = HoraireForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Horaire ajouté avec succès.")
                return redirect('list_horaires')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = HoraireForm()
    return render(request, 'create_horaire.html', {'form': form})

def list_horaires(request):
    utilisateur = request.user 
    horaires = Horaire.objects.all() 
    if utilisateur.role == 'Enseignant':
        horaires = Horaire.objects.filter(professeur=utilisateur).distinct()
    elif utilisateur.role == 'Etudiant':
        horaires = Horaire.objects.filter(cours__inscriptions__etudiant=utilisateur, cours__inscriptions__abandonne=False).distinct()
    # Organiser les horaires par jour de la semaine
    horaires_par_jour = defaultdict(list)
    for horaire in horaires:
        horaires_par_jour[horaire.jour].append(horaire)
    # Trier les jours dans l'ordre de la semaine
    jours_ordre = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    horaires_tries = {jour: horaires_par_jour[jour] for jour in jours_ordre if jour in horaires_par_jour}
    return render(request, 'list_horaires.html', {
        'horaires': horaires_tries,
        'utilisateur': utilisateur  
    })
        
def voir_mes_horaires(request):
    utilisateur = request.user

    if utilisateur.role == 'Etudiant':
        # Récupérer les cours de l'étudiant
        inscriptions = utilisateur.inscriptions.filter(abandonne=False)
        horaires = Horaire.objects.filter(cours__in=inscriptions.values_list('cours', flat=True))
    elif utilisateur.role == 'Enseignant':
        # Récupérer les cours enseignés par l'enseignant
        horaires = Horaire.objects.filter(cours__professeur=utilisateur)
    else:
        horaires = []

    return render(request, 'voir_mes_horaires.html', {'horaires': horaires})

# Mettre à jour un horaire existant
def update_horaire(request, id):
    horaire = get_object_or_404(Horaire, id=id)
    if request.method == 'POST':
        form = HoraireForm(request.POST, instance=horaire)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Horaire mis à jour avec succès.")
                return redirect('list_horaires')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = HoraireForm(instance=horaire)
    return render(request, 'update_horaire.html', {'form': form})

# Supprimer un horaire existant
def delete_horaire(request, id):
    horaire = get_object_or_404(Horaire, id=id)
    if request.method == 'POST':
        horaire.delete()
        messages.success(request, "Horaire supprimé avec succès.")
        return redirect('list_horaires')
    return render(request, 'delete_horaire.html', {'horaire': horaire})
