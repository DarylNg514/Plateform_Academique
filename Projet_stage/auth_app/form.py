from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import *
import re
from datetime import datetime

class UtilisateurForm(UserCreationForm):
    prenom = forms.CharField(max_length=30, required=True)
    nom = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=15, required=True)
    date_de_naissance = forms.DateField(label="Date de Naissance",
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1)))  
    adresse = forms.CharField( label="Addresse",
        max_length=50,
        required=True)
    code_postal = forms.CharField(max_length=10, required=True)
    sex = forms.ChoiceField(choices=Utilisateur.SEX_CHOICES, required=True)
    programme = forms.ModelMultipleChoiceField(
        queryset=Programme.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Utilisation de cases à cocher pour permettre la sélection multiple
        label="Programmes"
    )    
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=False)
    domaine = forms.ModelChoiceField(queryset=Domaine.objects.none(), required=False)
   
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = Utilisateur
        fields = ['username','image', 'prenom', 'nom', 'email', 'telephone', 'date_de_naissance', 'adresse', 'code_postal', 'sex', 'programme', 'session']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Affichez tous les champs disponibles pour déboguer
        print("Champs du formulaire:", self.fields.keys())
        # Essayez de supprimer le champ par son nom exact si détecté
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
        
        # Initialiser les domaines en fonction des programmes choisis
        programmes = self.data.getlist('programme') or self.initial.get('programme')
        if programmes:
            self.fields['domaine'].queryset = Domaine.objects.filter(programme__in=programmes)
            
        role = self.initial.get('role') or self.data.get('role')

        # Si le rôle est admin, on supprime les champs programme, session, et domaine
        if role == 'Admin':
            del self.fields['programme']
            del self.fields['session']
            del self.fields['domaine']
        
        # Si le rôle est enseignant, on transforme le champ domaine en sélection multiple (checkbox)
        elif role == 'Enseignant':
            del self.fields['session']
            self.fields['domaine'] = forms.ModelMultipleChoiceField(
                queryset=Domaine.objects.all(),
                widget=forms.CheckboxSelectMultiple,  # Utilisation de cases à cocher pour permettre la sélection multiple
                label="Domaines",
                required=False
            )
        
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom').strip()
        # Vérifier que tous les caractères sont des lettres ou des espaces
        if not all(char.isalpha() or char.isspace() for char in prenom):
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return prenom

    def clean_nom(self):
        nom = self.cleaned_data.get('nom').strip()
        # Vérifier que tous les caractères sont des lettres ou des espaces
        if not all(char.isalpha() or char.isspace() for char in nom):
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return nom

    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', adresse):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return adresse

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        # Pattern pour un numéro de téléphone valide
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(telephone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et au bon format.")
        return telephone

    def clean_code_postal(self):
        code_postal = self.cleaned_data.get('code_postal')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', code_postal):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return code_postal

    def clean_date_de_naissance(self):
        date_de_naissance = self.cleaned_data.get('date_de_naissance')
        age = (datetime.now().date() - date_de_naissance).days / 365.25
        if age < 18:
            raise forms.ValidationError("Vous devez avoir au moins 18 ans.")
        return date_de_naissance


class UtilisateurChangeForm(UserChangeForm):
    password = None 
    prenom = forms.CharField(max_length=30, required=True)
    nom = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=15, required=True)
    adresse = forms.CharField( label="Addresse",
        max_length=50,
        required=True)
    code_postal = forms.CharField(max_length=10, required=True)
    sex = forms.ChoiceField(choices=Utilisateur.SEX_CHOICES, required=True)
    role = forms.ChoiceField(choices=Utilisateur.ROLES_CHOICES, required=False)
    programme = forms.ModelMultipleChoiceField(
        queryset=Programme.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Utilisation de cases à cocher pour permettre la sélection multiple
        label="Programmes"
    )    
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=False)
    class Meta(UserChangeForm.Meta):
        model = Utilisateur
        fields = ['username','image', 'prenom', 'nom', 'email', 'telephone', 'adresse', 'code_postal', 'sex', 'role', 'programme', 'session','domaine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Affichez tous les champs disponibles pour déboguer
        print("Champs du formulaire:", self.fields.keys())
        # Essayez de supprimer le champ par son nom exact si détecté
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
            
        # Initialiser les domaines en fonction des programmes choisis
        programmes = self.data.getlist('programme') or self.initial.get('programme')
        if programmes:
            self.fields['domaine'].queryset = Domaine.objects.filter(programme__in=programmes)
            
        role = self.initial.get('role') or self.data.get('role')

        # Si le rôle est admin, on supprime les champs programme, session, et domaine
        if role == 'Admin':
            del self.fields['programme']
            del self.fields['session']
            del self.fields['domaine']
        
        # Si le rôle est enseignant, on transforme le champ domaine en sélection multiple (checkbox)
        elif role == 'Enseignant':
            del self.fields['session']
            self.fields['domaine'] = forms.ModelMultipleChoiceField(
                queryset=Domaine.objects.all(),
                widget=forms.CheckboxSelectMultiple,  # Utilisation de cases à cocher pour permettre la sélection multiple
                label="Domaines",
                required=False
            )
           
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email == email:
            return email
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom').strip()
        # Vérifier que tous les caractères sont des lettres ou des espaces
        if not all(char.isalpha() or char.isspace() for char in prenom):
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return prenom

    def clean_nom(self):
        nom = self.cleaned_data.get('nom').strip()
        # Vérifier que tous les caractères sont des lettres ou des espaces
        if not all(char.isalpha() or char.isspace() for char in nom):
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return nom
    
    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', adresse):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return adresse

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        # Pattern pour un numéro de téléphone valide
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(telephone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et au bon format.")
        return telephone

    def clean_code_postal(self):
        code_postal = self.cleaned_data.get('code_postal')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', code_postal):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return code_postal

# Formulaire pour la gestion des programmes
class ProgrammeForm(forms.ModelForm):
    code_programme = forms.CharField(max_length=30, required=True)
    intitule = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Programme
        fields = ['code_programme','image', 'intitule']
    
class DomaineForm(forms.ModelForm):
    code_programme = forms.CharField(max_length=30, required=True)
    intitule = forms.CharField(max_length=500, required=True)
    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), required=False)


    class Meta:
        model = Domaine
        fields = ['code_programme','image', 'intitule', 'programme']


# Formulaire pour la gestion des sessions
class SessionForm(forms.ModelForm):
    code_session = forms.CharField(max_length=30, required=True)
    date_debut = forms.DateField(widget=forms.SelectDateWidget, required=True)
    date_fin = forms.DateField(widget=forms.SelectDateWidget, required=True)

    class Meta:
        model = Session
        fields = ['code_session','image', 'date_debut', 'date_fin']

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin:
            if date_debut > date_fin:
                raise forms.ValidationError("La date de début doit être antérieure à la date de fin.")
        return cleaned_data
    
    
class CandidatForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
    )
    prenom = forms.CharField(label="Prenom", max_length=30, required=True)
    nom = forms.CharField(label="Nom", max_length=30, required=True)
    telephone = forms.CharField(max_length=15, required=True)
    date_de_naissance = forms.DateField(label="Date de Naissance",
        required=True,
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1)))
    adresse = forms.CharField(label="Addresse",
        max_length=50,
        required=True)
    code_postal = forms.CharField(max_length=10, required=True)
    sex = forms.ChoiceField(choices=Utilisateur.SEX_CHOICES, required=True)
    programme = forms.ModelMultipleChoiceField(
        queryset=Programme.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Utilisation de cases à cocher pour permettre la sélection multiple
        label="Programmes"
    )
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=False)
    domaine = forms.ModelChoiceField(queryset=Domaine.objects.none(), required=False)

    class Meta:
        model = Utilisateur
        fields = ['username','image', 'prenom', 'nom', 'email', 'telephone', 'date_de_naissance', 'adresse', 'code_postal', 'sex', 'programme', 'session','domaine']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Champs du formulaire:", self.fields.keys())
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

        # Initialiser les domaines en fonction des programmes choisis
        programmes = self.data.getlist('programme') or self.initial.get('programme')
        if programmes:
            self.fields['domaine'].queryset = Domaine.objects.filter(programme__in=programmes)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists() and not self.instance.pk:
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Utilisateur.objects.filter(username=username).exists() and not self.instance.pk:
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom').strip()
        if not all(char.isalpha() or char.isspace() for char in prenom):
            raise forms.ValidationError("Le prénom doit contenir uniquement des lettres.")
        return prenom

    def clean_nom(self):
        nom = self.cleaned_data.get('nom').strip()
        if not all(char.isalpha() or char.isspace() for char in nom):
            raise forms.ValidationError("Le nom doit contenir uniquement des lettres.")
        return nom

    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if not re.match(r'^\d+ [a-zA-Z0-9 ]+$', adresse):
            raise forms.ValidationError("Veuillez entrer une adresse valide.")
        return adresse

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        pattern = re.compile(r'^(?:\+1\s?)?\(?[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not pattern.match(telephone):
            raise forms.ValidationError("Le numéro de téléphone doit être valide et au bon format.")
        return telephone

    def clean_code_postal(self):
        code_postal = self.cleaned_data.get('code_postal')
        if not re.match(r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$', code_postal):
            raise forms.ValidationError("Veuillez entrer un code postal valide au Canada (format: A1A 1A1).")
        return code_postal

    def clean_date_de_naissance(self):
        date_de_naissance = self.cleaned_data.get('date_de_naissance')
        age = (datetime.now().date() - date_de_naissance).days / 365.25
        if age < 18:
            raise forms.ValidationError("Vous devez avoir au moins 18 ans.")
        return date_de_naissance

    def clean_programme(self):
        programmes = self.cleaned_data.get('programme')
        if programmes.count() > 3:
            raise forms.ValidationError("Vous pouvez sélectionner un maximum de 3 programmes.")
        return programmes    

class MessageForm(forms.ModelForm):
    destinataire = forms.ModelChoiceField(
        queryset=Utilisateur.objects.none(), 
        required=True, 
        label="Destinataire"
    )
    sujet = forms.CharField(max_length=255, required=False, label="Sujet")
    contenu = forms.CharField(widget=forms.Textarea, required=True, label="Message")

    class Meta:
        model = Message
        fields = ['destinataire', 'sujet', 'contenu']

    def __init__(self, *args, **kwargs):
        # Ajouter l'expéditeur comme argument supplémentaire
        self.expéditeur = kwargs.pop('expéditeur', None)
        super().__init__(*args, **kwargs)

        # Filtrer les destinataires et ajuster le label pour inclure le rôle, programme, session et domaine
        if self.expéditeur:
            if self.expéditeur.role == 'Candidat':
                queryset = Utilisateur.objects.filter(role='Admin')
            else:
                queryset = Utilisateur.objects.all()

            self.fields['destinataire'].queryset = queryset
            self.fields['destinataire'].label_from_instance = self.label_from_instance_with_details

    def label_from_instance_with_details(self, obj):
        # Construction du label avec le rôle, programme, session, et domaine
        label = f"{obj.username} ({obj.get_role_display()})"
        if obj.programme:
            label += f" - Programme: {obj.programme.code_programme}"
        if obj.session:
            label += f" - Session: {obj.session.code_session}"
        if hasattr(obj, 'domaine') and obj.domaine:
            label += f" - Domaine: {obj.domaine.code_programme}"
        return label

    def save(self, commit=True):
        # Assigner automatiquement l'expéditeur lors de la sauvegarde du message
        message = super().save(commit=False)
        if self.expéditeur:
            message.expéditeur = self.expéditeur
        if commit:
            message.save()
        return message
    
class ProgrammeChoiceForm(forms.Form):
    programme = forms.ModelChoiceField(queryset=Programme.objects.none(), label="Choisissez un programme")

    def __init__(self, *args, **kwargs):
        programmes = kwargs.pop('programmes')
        super().__init__(*args, **kwargs)
        self.fields['programme'].queryset = programmes