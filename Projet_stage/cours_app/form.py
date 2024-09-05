from django import forms
from auth_app.models import *
from .models import Cours, Inscription, Evaluation, Note, Horaire

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['sigle', 'titre', 'description', 'programme', 'domaine', 'session', 'professeur', 'salle', 'horaire']

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['cours']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        self.fields['cours'].queryset = Cours.objects.filter(programme=self.student.programme)

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['titre', 'type_resultat', 'note_maximale', 'ponderation']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['evaluation', 'note_obtenue']

class HoraireForm(forms.ModelForm):
    class Meta:
        model = Horaire
        fields = ['cours', 'jour', 'heure_debut', 'heure_fin', 'salle']
