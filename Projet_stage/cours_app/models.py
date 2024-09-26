from django.db import models
from django.core.exceptions import ValidationError
from auth_app.models import Utilisateur, Programme, Domaine, Session
from django.utils import timezone

# Modèle représentant une salle de classe
class Salle(models.Model):
    nom = models.CharField(max_length=50, unique=True)  # Nom de la salle (ex: SB-R440)
    batiment = models.CharField(max_length=50)  # Nom ou code du bâtiment (ex: Bâtiment A)
    capacite = models.IntegerField()  # Capacité de la salle

    def __str__(self):
        return f"{self.nom} - {self.batiment} (Capacité: {self.capacite})"

# Modèle représentant un cours
class Cours(models.Model):
    sigle = models.CharField(max_length=10, unique=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    #professeur = models.ManyToManyField(Utilisateur, limit_choices_to={'role': 'Enseignant'}, related_name='cours_enseignes')
    programme = models.ManyToManyField(Programme, related_name='cours')
    domaine = models.ManyToManyField(Domaine, related_name='cours', blank=True)
    session = models.ManyToManyField(Session, related_name='cours')

    def __str__(self):
        return f"{self.sigle} - {self.titre}"

        
class Groupe(models.Model):
    nogroupe = models.CharField(max_length=20, unique=True)  # Identifiant unique pour chaque groupe
    nom_groupe = models.CharField(max_length=100)  # Nom du groupe pour une meilleure lisibilité

    def __str__(self):
        return f"{self.nogroupe} - {self.nom_groupe}"

class Attribution(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='attributions')
    professeur = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Enseignant'}, on_delete=models.CASCADE, related_name='attributions')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='attributions',null=True, blank=True)  # Clé étrangère vers le modèle Groupe

    class Meta:
        unique_together = ('cours', 'professeur', 'groupe')

    def __str__(self):
        return f"{self.groupe.nogroupe} - {self.professeur.nom} - {self.cours.sigle}"

    def clean(self):
        # S'assurer qu'un professeur ne peut pas être assigné deux fois au même cours dans le même groupe
        if Attribution.objects.filter(cours=self.cours, professeur=self.professeur, groupe=self.groupe).exists():
            raise ValidationError(f"Le professeur {self.professeur.nom} est déjà assigné au cours {self.cours.sigle} dans le groupe {self.groupe.nogroupe}.")

        
class Inscription(models.Model):
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='inscriptions')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='inscriptions')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='inscriptions', null=True, blank=True)  # Clé étrangère vers le modèle Groupe
    date_inscription = models.DateField(auto_now_add=True)
    abandonne = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'cours', 'groupe')

    def __str__(self):
        return f"{self.etudiant.username} inscrit à {self.cours.sigle} (Groupe: {self.groupe.nogroupe})"

    def clean(self):
        # Vérifier que le groupe n'a pas déjà 40 étudiants inscrits
        if self.groupe and Inscription.objects.filter(groupe=self.groupe, abandonne=False).count() >= 40:
            raise ValidationError(f"Le groupe {self.groupe.nogroupe} est complet. Impossible d'ajouter plus d'étudiants.")

    def save(self, *args, **kwargs):
        # Appeler la méthode clean avant de sauvegarder pour valider les règles
        self.clean()
        super(Inscription, self).save(*args, **kwargs)    
        

# Modèle représentant un horaire
class Horaire(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='horaires')  # Lien avec le groupe
    jour = models.CharField(max_length=15)  # Ex: Lundi, Mardi, etc.
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='horaires')

    class Meta:
        unique_together = ('groupe', 'salle', 'jour', 'heure_debut')

    def __str__(self):
        return f"{self.groupe.nom_groupe} - {self.jour}: {self.heure_debut} - {self.heure_fin} ({self.salle})"

    def clean(self):
        # Vérifier les conflits d'horaires avant de sauvegarder l'horaire
        # 1. Conflit de salle: deux groupes ne doivent pas être planifiés à la même heure dans la même salle
        conflicts = Horaire.objects.filter(
            salle=self.salle,
            jour=self.jour,
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        ).exclude(id=self.id)
        if conflicts.exists():
            raise ValidationError(f"Conflit d'horaire: La salle {self.salle.nom} est déjà réservée à ce créneau horaire.")

        # 2. Conflit de groupe: un groupe ne doit pas avoir deux cours en même temps
        groupe_conflits = Horaire.objects.filter(
            groupe=self.groupe,
            jour=self.jour,
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        ).exclude(id=self.id)
        if groupe_conflits.exists():
            raise ValidationError(f"Conflit d'horaire: Le groupe {self.groupe.nom_groupe} a déjà un cours prévu à ce créneau horaire.")

    def save(self, *args, **kwargs):
        # Appeler la méthode clean avant de sauvegarder pour valider les règles
        self.clean()
        super(Horaire, self).save(*args, **kwargs)


# Modèle représentant un document pour un cours
class CoursDocument(models.Model):
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents_cours/')

    def __str__(self):
        return f"{self.titre} - {self.cours.sigle}"


# Modèle représentant une évaluation pour un cours
class Evaluation(models.Model):
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE, related_name='evaluations')
    titre = models.CharField(max_length=200)
    type_resultat = models.CharField(max_length=50)  # Exemple : Examen, Devoir, Projet
    note_maximale = models.DecimalField(max_digits=5, decimal_places=2)
    ponderation = models.DecimalField(max_digits=5, decimal_places=2)  # Pourcentage de la note finale
    date_limite = models.DateTimeField(null=True, blank=True)  # Date limite pour la soumission de l'évaluation
    fichier = models.FileField(upload_to='documents_evaluation/', blank=True, null=True)
    consignes = models.TextField(default='')
    date_publication = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    

    def __str__(self):
        return f"{self.titre} - {self.cours.sigle}"
    

# Modèle représentant une note obtenue par un étudiant dans une évaluation
class Note(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='notes')
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='notes')
    note_obtenue = models.DecimalField(max_digits=5, decimal_places=2)
    est_attribuee = models.BooleanField(default=False)  # Indique si la note a déjà été attribuée

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
        
class Devoir(models.Model):
    Cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='devoirs', blank=True, null=True)
    titre = models.CharField(max_length=200)
    consignes = models.TextField()
    date_limite = models.DateTimeField()
    fichier = models.FileField(upload_to='devoirs/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.evaluation.cours.sigle}"

class ConsultationDocument(models.Model):
    document = models.ForeignKey('CoursDocument', on_delete=models.CASCADE, related_name='consultations')
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='consultations')
    date_consultation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.etudiant.username} a consulté {self.document.titre} le {self.date_consultation}"
    
class SoumissionEvaluation(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='soumissions')
    etudiant = models.ForeignKey(Utilisateur, limit_choices_to={'role': 'Etudiant'}, on_delete=models.CASCADE, related_name='soumissions')
    fichier = models.FileField(upload_to='soumissions_evaluations/')
    date_soumission = models.DateTimeField(auto_now_add=True)
    soumission_effectuee = models.BooleanField(default=False)  # Nouveau champ

    class Meta:
        unique_together = ('evaluation', 'etudiant')  # Un étudiant ne peut soumettre qu'une fois par évaluation

    def __str__(self):
        return f"Soumission de {self.etudiant.username} pour {self.evaluation.titre}"
