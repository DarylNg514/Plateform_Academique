# Generated by Django 5.1 on 2024-09-20 04:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours_app', '0005_remove_cours_professeur_horaire_professeur'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributions', to='cours_app.cours')),
                ('professeur', models.ForeignKey(limit_choices_to={'role': 'Enseignant'}, on_delete=django.db.models.deletion.CASCADE, related_name='attributions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('cours', 'professeur')},
            },
        ),
    ]
