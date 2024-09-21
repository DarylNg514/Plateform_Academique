from django import forms
from datetime import time
from auth_app.models import *
from .models import *

class CoursForm(forms.ModelForm):
    programme = forms.ModelMultipleChoiceField(
        queryset=Programme.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Programmes"
    )
    domaine = forms.ModelMultipleChoiceField(
        queryset=Domaine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Domaines"
    )
    session = forms.ModelMultipleChoiceField(
        queryset=Session.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Sessions"
    )
    '''professeur = forms.ModelMultipleChoiceField(
        queryset=Utilisateur.objects.filter(role='Enseignant'),
        widget=forms.CheckboxSelectMultiple,
        label="Professeurs"
    )'''

    class Meta:
        model = Cours
        fields = ['sigle', 'titre', 'description', 'programme', 'domaine', 'session']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialiser les domaines en fonction des programmes choisis
        programmes = self.data.getlist('programme') or self.initial.get('programme')
        if programmes:
            self.fields['domaine'].queryset = Domaine.objects.filter(programme__in=programmes)
        
        # Personnaliser le label pour chaque domaine afin d'inclure le code du programme
        self.fields['domaine'].label_from_instance = lambda obj: f"{obj.code_programme} ({obj.programme.code_programme})"            
                    
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['cours']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if self.student:
            self.fields['cours'].queryset = Cours.objects.filter(programme__in=self.student.programme.all(), session=self.student.session)


class HoraireForm(forms.ModelForm):
    # Liste des jours de la semaine
    JOURS_SEMAINE = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ]
    
    # Liste des heures de 8h00 à 22h00
    HEURES_CHOIX = [(time(h, 0), f"{h:02d}:00") for h in range(8, 23)]
    
    jour = forms.ChoiceField(choices=JOURS_SEMAINE, label="Jour de la semaine")
    heure_debut = forms.ChoiceField(choices=HEURES_CHOIX, label="Heure de début")
    heure_fin = forms.ChoiceField(choices=HEURES_CHOIX, label="Heure de fin")
    professeur = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(role='Enseignant'), label="Professeur")  # Ajout du champ professeur
    
    class Meta:
        model = Horaire
        fields = ['cours', 'jour', 'heure_debut', 'heure_fin', 'salle', 'professeur']  # Ajout du champ professeur

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si nécessaire, personnalisez la requête pour les salles disponibles
        self.fields['salle'].queryset = Salle.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get("heure_debut")
        heure_fin = cleaned_data.get("heure_fin")
        
        if heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                raise forms.ValidationError("L'heure de fin doit être supérieure à l'heure de début.")
        
        return cleaned_data
    
class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'batiment','capacite']

# Formulaire pour ajouter un document de cours
class CoursDocumentForm(forms.ModelForm):
    class Meta:
        model = CoursDocument
        fields = ['titre', 'fichier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des placeholders
        self.fields['titre'].widget.attrs.update({
            'placeholder': 'Titre du document (ex: Chapitre 1 - Introduction)',
            'class': 'form-control'
        })
        


# Formulaire pour créer une évaluation
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['titre', 'type_resultat', 'note_maximale', 'ponderation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des placeholders
        self.fields['titre'].widget.attrs.update({
            'placeholder': 'Titre de l\'évaluation (ex: Examen final, Devoir 1)',
            'class': 'form-control'
        })
        self.fields['type_resultat'].widget.attrs.update({
            'placeholder': 'Type de résultat (ex: Examen, Projet)',
            'class': 'form-control'
        })
        self.fields['note_maximale'].widget.attrs.update({
            'placeholder': 'Note maximale (ex: 100)',
            'class': 'form-control'
        })
        self.fields['ponderation'].widget.attrs.update({
            'placeholder': 'Pondération (ex: 20%)',
            'class': 'form-control'
        })

# Formulaire pour attribuer une note à un étudiant
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note_obtenue']

    def clean_note_obtenue(self):
        note_obtenue = self.cleaned_data.get('note_obtenue')
        if note_obtenue < 0 or note_obtenue > 100:
            raise forms.ValidationError("La note doit être comprise entre 0 et 100.")
        return note_obtenue
    
# Formulaire pour créer un devoir
class DevoirForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = [ 'titre', 'consignes', 'date_limite', 'fichier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des placeholders et des classes CSS
        
        self.fields['titre'].widget.attrs.update({
            'placeholder': 'Titre du devoir (ex: Devoir 1)',
            'class': 'form-control'
        })
        self.fields['consignes'].widget.attrs.update({
            'placeholder': 'Consignes pour le devoir',
            'class': 'form-control'
        })
        self.fields['date_limite'].widget.attrs.update({
            'placeholder': 'Date limite (ex: 2024-12-31 23:59)',
            'class': 'form-control'
        })
        self.fields['fichier'].widget.attrs.update({
            'class': 'form-control-file'
        })
        
        
class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nogroupe', 'nom_groupe']
        labels = {
            'nogroupe': 'Numéro de Groupe',
            'nom_groupe': 'Nom du Groupe',
        }
        widgets = {
            'nogroupe': forms.TextInput(attrs={'placeholder': 'Entrez le numéro du groupe'}),
            'nom_groupe': forms.TextInput(attrs={'placeholder': 'Entrez le nom du groupe'}),
        }
        
class SoumissionEvaluationForm(forms.ModelForm):
    class Meta:
        model = SoumissionEvaluation
        fields = ['fichier']