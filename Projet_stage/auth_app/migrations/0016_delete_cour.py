# Generated by Django 5.1 on 2024-09-03 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0015_remove_utilisateur_domaine_cour_utilisateur_domaine'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cour',
        ),
    ]
