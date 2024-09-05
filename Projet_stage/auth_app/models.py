from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Programme(models.Model):
    image = models.ImageField(upload_to='images/',  blank=True, null=True)
    code_programme = models.CharField(max_length=30, unique=True)
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return self.code_programme
class Domaine(models.Model):
    image = models.ImageField(upload_to='images/',  blank=True, null=True)
    code_programme = models.CharField(max_length=30, unique=True)
    intitule = models.CharField(max_length=500)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    def __str__(self):
        return self.code_programme

class Session(models.Model):
    image = models.ImageField(upload_to='images/',  blank=True, null=True)
    code_session = models.CharField(max_length=30, unique=True)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.code_session
    
class Candidat(models.Model):
    nom_utilisateur = models.CharField(max_length=30)
    mot_de_passe = models.CharField(max_length=30)
    email = models.EmailField()
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

class Utilisateur(AbstractUser):
    ROLES_CHOICES = [
        ('Admin', 'Administrateur'),
        ('Candidat', 'Candidat'),
        ('Enseignant', 'Enseignant'),
        ('Etudiant', 'Étudiant'),
    ]
    SEX_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
        ('Autre', 'Autre'),
    ]
    
    image = models.ImageField(upload_to='images/',  blank=True, null=True)
    prenom = models.CharField(max_length=30)
    nom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    date_de_naissance = models.DateField()
    adresse = models.TextField()
    code_postal = models.CharField(max_length=10)
    sex = models.CharField(max_length=30, choices=SEX_CHOICES, default='Homme')
    status = models.BooleanField(null=True, blank=True)  
    role = models.CharField(max_length=30, choices=ROLES_CHOICES, default='Candidat', null=True, blank=True)
    programme = models.ManyToManyField('Programme', blank=True) 
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    domaine = models.ManyToManyField('Domaine', blank=True)


    def save(self, *args, **kwargs):
        # Définir is_staff et is_superuser à True par défaut si le rôle est 'Admin'
        if self.role == 'Admin':
            self.is_staff = True
            self.is_superuser = True
        super(Utilisateur, self).save(*args, **kwargs)

class Message(models.Model):
    expéditeur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='messages_envoyés', 
        on_delete=models.CASCADE
    )
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='messages_reçus', 
        on_delete=models.CASCADE
    )
    sujet = models.CharField(max_length=255, blank=True, null=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f'Message de {self.expéditeur.username} à {self.destinataire.username} - {self.sujet} - {self.date_formatee()}'
    
    def date_formatee(self):
        return self.date_envoi.strftime('%d-%m-%Y %H:%M')

    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        