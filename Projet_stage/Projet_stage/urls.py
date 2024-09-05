"""
URL configuration for Projet_stage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from auth_app import views as vsa
from cours_app import views as vsc



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vsa.acceuil, name='acceuil'),
    
    path('utilisateurs/', vsa.list_utilisateurs, name='list_utilisateurs'),
    path('utilisateurs/inscrire/', vsa.inscription, name='inscription'),
    path('ajax/load-domaines/', vsa.load_domaines, name='load_domaines'),

    path('connexion/', vsa.connexion, name='connexion'),
    path('deconnexion/', vsa.deconnexion, name='deconnexion'),
    path('utilisateurs/update/<int:id>/', vsa.update_utilisateur, name='update_utilisateur'),
    path('utilisateurs/delete/<int:id>/', vsa.delete_utilisateur, name='delete_utilisateur'),
    
    path('utilisateurs/create/<str:role>/', vsa.create_utilisateur, name='create_utilisateur'),
    path('utilisateurs/enseignants/', vsa.list_utilisateurs_par_role, {'role': 'Enseignant'}, name='list_enseignants'),
    path('utilisateurs/etudiants/', vsa.list_utilisateurs_par_role, {'role': 'Etudiant'}, name='list_etudiants'),
    path('utilisateurs/admins/', vsa.list_utilisateurs_par_role, {'role': 'Admin'}, name='list_admins'),
    path('utilisateurs/candidats/', vsa.list_utilisateurs_par_role, {'role': 'Candidat'}, name='list_candidats'),
    
    path('programme/', vsa.list_programmes, name='list_programmes'),
    path('programme/create/', vsa.create_programme, name='create_programme'),    
    path('programme/update/<int:id>/', vsa.update_programme, name='update_programme'),
    path('programme/delete/<int:id>/', vsa.delete_programme, name='delete_programme'),
    
    path('domaine/', vsa.list_domaines, name='list_domaines'),
    path('domaine/create/', vsa.create_domaine, name='create_domaine'),
    path('domaine/update/<int:id>/', vsa.update_domaine, name='update_domaine'),
    path('domaine/delete/<int:id>/', vsa.delete_domaine, name='delete_domaine'),

    path('session/', vsa.list_sessions, name='list_sessions'),
    path('session/create/', vsa.create_session, name='create_session'),
    path('session/update/<int:id>/', vsa.update_session, name='update_session'),
    path('session/delete/<int:id>/', vsa.delete_session, name='delete_session'),
    
    path('messages/envoyer/', vsa.envoyer_message, name='envoyer_message'),
    path('messages/', vsa.afficher_messages, name='afficher_messages'),
    path('messages/<int:id>/', vsa.lire_message, name='lire_message'),
    path('messages/supprimer/<int:id>/', vsa.supprimer_message, name='supprimer_message'),
    
    path('candidate/<int:user_id>/', vsa.accepter_candidat, name='accepter_candidat'),
    path('candidate/supprimer/<int:user_id>/', vsa.refuser_candidat, name='refuser_candidat'),
    
    path('profil/', vsa.profil_utilisateur, name='profil_utilisateur'),
    
    
    path('cours/create/', vsc.create_cours, name='create_cours'),
    path('cours/professeur/', vsc.list_cours_professeur, name='list_cours_professeur'),
    path('cours/inscrire/', vsc.inscrire_cours, name='inscrire_cours'),
    path('cours/modifier/<int:id>/', vsc.modifier_inscription, name='modifier_inscription'),
    path('cours/supprimer/<int:id>/', vsc.supprimer_inscription, name='supprimer_inscription'),
    path('cours/rechercher/', vsc.rechercher_cours, name='rechercher_cours'),
    path('cours/planifier/', vsc.planifier_horaire, name='planifier_horaire'),
    path('cours/notes/', vsc.consulter_notes, name='consulter_notes'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
