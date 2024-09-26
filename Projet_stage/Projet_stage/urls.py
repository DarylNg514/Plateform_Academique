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
    path('contact/', vsa.contact, name='contact'),
    path('blog/', vsa.blog, name='blog'),
    path('about/', vsa.about, name='about'),
    path('personnel/', vsa.personnel, name='personnel'),
    path('cours/', vsa.cours, name='cours'),
    
    path('utilisateurs/', vsa.list_utilisateurs, name='list_utilisateurs'),
    path('utilisateurs/inscrire/', vsa.inscription, name='inscription'),    
    path('utilisateurs/payer/', vsa.payer_inscription, name='payer_inscription'),
    
    # Vue pour le paiement réussi qui enregistre l'utilisateur
    path('utilisateurs/paiement_succes/', vsa.paiement_succes_inscription, name='paiement_succes_inscription'),
    path('utilisateurs/changer-frais/', vsa.changer_frais_admission, name='changer_frais_inscription'),
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
    
    path('groupes/', vsc.list_groupes, name='list_groupes'),
    path('groupes/create/', vsc.create_groupe, name='create_groupe'),
    path('groupes/update/<int:id>/', vsc.update_groupe, name='update_groupe'),
    path('groupes/delete/<int:id>/', vsc.delete_groupe, name='delete_groupe'),
    
    path('salles/', vsc.liste_salles, name='list_salles'),
    path('salles/creer/', vsc.creer_salle, name='create_salle'),
    path('salles/<int:id>/modifier/', vsc.mettre_a_jour_salle, name='update_salle'),
    path('salles/<int:id>/supprimer/', vsc.supprimer_salle, name='delete_salle'),
    
    
    # Liste des cours
    path('cours/liste', vsc.list_cours, name='list_cours'),
    path('cours/creer/', vsc.create_cours, name='create_cours'),
    path('cours/<int:id>/modifier/', vsc.update_cours, name='update_cours'),
    path('cours/<int:id>/supprimer/', vsc.delete_cours, name='delete_cours'),
    path('mes-cours-professeur/', vsc.mes_cours_professeur, name='mes_cours_professeur'),
    path('etudiants/<int:etudiant_id>/', vsc.voir_etudiant, name='voir_etudiant'),
    path('mes-cours-etudiant/', vsc.mes_cours_etudiant, name='mes_cours_etudiant'),
    path('cours/attribuer/<int:cours_id>/', vsc.assigner_professeur, name='assigner_professeur'),
    path('cours/inscrire/<int:cours_id>/', vsc.inscrire_cours, name='inscrire_cours'),
    path('abandonner-cours/<int:cours_id>/', vsc.abandonner_cours, name='abandonner_cours'),
    
    # URLs pour les évaluations
    path('cours/<int:cours_id>/evaluations/', vsc.liste_evaluations, name='liste_evaluations'),
    path('cours/<int:cours_id>/evaluation/create/', vsc.create_evaluation, name='create_evaluation'),
    path('update-evaluation/<int:evaluation_id>/', vsc.update_evaluation, name='update_evaluation'),
    path('delete-evaluation/<int:evaluation_id>/', vsc.delete_evaluation, name='delete_evaluation'),
    path('soumettre-evaluation/<int:evaluation_id>/', vsc.soumettre_evaluation, name='soumettre_evaluation'),
    path('liste-soumissions/<int:evaluation_id>/', vsc.liste_soumissions, name='liste_soumissions'),
      
    path('cours/<int:cours_id>/documents/', vsc.liste_documents, name='liste_documents'),
    path('cours/<int:cours_id>/document/add/', vsc.ajouter_document, name='ajouter_document'),
    path('update-document/<int:document_id>/', vsc.update_document, name='update_document'),
    path('delete-document/<int:document_id>/', vsc.delete_document, name='delete_document'),
    path('consulter-document/<int:document_id>/', vsc.consulter_document, name='consulter_document'),
    path('consultations-document/<int:document_id>/', vsc.consultations_document, name='consultations_document'),
 

    # URLs pour les notes
    path('list_notes_cours/<int:cours_id>/', vsc.list_notes_cours, name='list_notes_cours'),
    path('assigner-note/<int:etudiant_id>/', vsc.assigner_note, name='assigner_note'),
    path('voir-notes/<int:cours_id>/', vsc.voir_notes_etudiant, name='voir_notes_etudiant'),
    #path('etudiant/<int:etudiant_id>/assigner-note/', vsc.assigner_note, name='assigner_note'),


    # URLs pour les horaires
    path('horaire/creer/', vsc.create_horaire, name='create_horaire'),
    path('horaires/', vsc.list_horaires, name='list_horaires'),
    path('horaire/modifier/<int:id>/', vsc.update_horaire, name='update_horaire'),
    path('horaire/supprimer/<int:id>/', vsc.delete_horaire, name='delete_horaire'),

    path('recherche/', vsc.search_cours, name='search_cours'),

    path('cours/rechercher/', vsc.rechercher_cours, name='rechercher_cours'),
    path('cours/notes/', vsc.consulter_notes, name='consulter_notes'),

    path('chatbot/', vsc.chatbot_view, name='chatbot'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
