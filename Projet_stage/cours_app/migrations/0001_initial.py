# Generated by Django 5.1 on 2024-09-03 17:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0016_delete_cour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigle', models.CharField(max_length=10, unique=True)),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('salle', models.CharField(blank=True, max_length=50, null=True)),
                ('horaire', models.TextField(blank=True, null=True)),
                ('domaine', models.ManyToManyField(blank=True, related_name='cours', to='auth_app.domaine')),
                ('professeur', models.ManyToManyField(limit_choices_to={'role': 'Enseignant'}, related_name='cours_enseignes', to=settings.AUTH_USER_MODEL)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours', to='auth_app.programme')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours', to='auth_app.session')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('type_resultat', models.CharField(max_length=50)),
                ('note_maximale', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ponderation', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='cours_app.cours')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_obtenue', models.DecimalField(decimal_places=2, max_digits=5)),
                ('etudiant', models.ForeignKey(limit_choices_to={'role': 'Etudiant'}, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='cours_app.evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='Horaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(max_length=15)),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('salle', models.CharField(max_length=50)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='cours_app.cours')),
            ],
            options={
                'unique_together': {('cours', 'salle', 'jour', 'heure_debut')},
            },
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_inscription', models.DateField(auto_now_add=True)),
                ('abandonne', models.BooleanField(default=False)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='cours_app.cours')),
                ('etudiant', models.ForeignKey(limit_choices_to={'role': 'Etudiant'}, on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('etudiant', 'cours')},
            },
        ),
    ]
