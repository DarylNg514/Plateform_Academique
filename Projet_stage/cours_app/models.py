from django.db import models
from auth_app.models import *
# Modèle représentant un cours
class Cours(models.Model):
    sigle = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    professeur = models.ManyToManyField(Utilisateur, limit_choices_to={'role': 'Enseignant'}, related_name='cours_enseignes')
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='cours')
    domaine = models.ManyToManyField(Domaine, related_name='cours', blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='cours')
    salle = models.CharField(max_length=50, null=True, blank=True)  # Nom de la salle de cours
    horaire = models.TextField(null=True, blank=True)  # Horaire du cours (jour/heure)

    def __str__(self):
        return f"{self.sigle} - {self.titre}"

# Modèle représentant une inscription à un cours par un étudiant
class Inscription(models.Model):
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='inscriptions')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateField(auto_now_add=True)
    abandonne = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'cours')

    def __str__(self):
        return f"{self.etudiant.username} inscrit à {self.cours.sigle}"

# Modèle représentant une évaluation pour un cours
class Evaluation(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='evaluations')
    titre = models.CharField(max_length=200)
    type_resultat = models.CharField(max_length=50)  # Exemple : Examen, Devoir, Projet
    note_maximale = models.DecimalField(max_digits=5, decimal_places=2)
    ponderation = models.DecimalField(max_digits=5, decimal_places=2)  # Pourcentage de la note finale

    def __str__(self):
        return f"{self.titre} - {self.cours.sigle}"
    
# Modèle représentant une note obtenue par un étudiant dans une évaluation
class Note(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='notes')
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='notes')
    note_obtenue = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.etudiant.username} - {self.evaluation.titre}: {self.note_obtenue}"

    def get_mention(self):
        # Fonction pour déterminer la mention en fonction de la note obtenue
        if self.note_obtenue >= 90:
            return 'A+'
        elif self.note_obtenue >= 85:
            return 'A'
        elif self.note_obtenue >= 80:
            return 'A-'
        elif self.note_obtenue >= 75:
            return 'B+'
        elif self.note_obtenue >= 70:
            return 'B'
        elif self.note_obtenue >= 65:
            return 'B-'
        elif self.note_obtenue >= 60:
            return 'C+'
        elif self.note_obtenue >= 55:
            return 'C'
        elif self.note_obtenue >= 50:
            return 'D'
        else:
            return 'E'  # Échec

# Modèle représentant un horaire
class Horaire(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='horaires')
    jour = models.CharField(max_length=15)  # Ex: Lundi, Mardi, etc.
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50)

    class Meta:
        unique_together = ('cours', 'salle', 'jour', 'heure_debut')

    def __str__(self):
        return f"{self.cours.sigle} - {self.jour}: {self.heure_debut} - {self.heure_fin} ({self.salle})"