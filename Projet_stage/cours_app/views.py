from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from auth_app.models import *
from .models import *
from auth_app.form import *
from .form import *

# Ajouter un ou plusieurs cours (par un administrateur)
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

# Liste des cours pour un professeur spécifique
def list_cours_professeur(request):
    professeur = request.user
    cours = Cours.objects.filter(professeur=professeur)
    return render(request, 'list_cours_professeur.html', {'cours': cours})

# Inscription d'un étudiant à un ou plusieurs cours
def inscrire_cours(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, student=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription aux cours réussie.")
            return redirect('list_cours_etudiant')
    else:
        form = InscriptionForm(student=request.user)
    return render(request, 'inscription_form.html', {'form': form})

# Modifier ou annuler une inscription à un cours
def modifier_inscription(request, id):
    inscription = get_object_or_404(Inscription, id=id, etudiant=request.user)
    if request.method == 'POST':
        form = InscriptionForm(request.POST, instance=inscription, student=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription modifiée avec succès.")
            return redirect('list_cours_etudiant')
    else:
        form = InscriptionForm(instance=inscription, student=request.user)
    return render(request, 'inscription_form.html', {'form': form})

# Supprimer une inscription à un cours
def supprimer_inscription(request, id):
    inscription = get_object_or_404(Inscription, id=id, etudiant=request.user)
    if request.method == 'POST':
        inscription.delete()
        messages.success(request, "Inscription annulée.")
        return redirect('list_cours_etudiant')
    return render(request, 'confirmation.html', {'inscription': inscription})

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

# Planifier les horaires des cours (pour un administrateur)
def planifier_horaire(request):
    if request.method == 'POST':
        form = HoraireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Horaire planifié avec succès.")
            return redirect('list_horaires')
    else:
        form = HoraireForm()
    return render(request, 'horaire_form.html', {'form': form})
