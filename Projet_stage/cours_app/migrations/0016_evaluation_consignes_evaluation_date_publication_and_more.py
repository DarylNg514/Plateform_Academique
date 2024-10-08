# Generated by Django 5.1 on 2024-09-26 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours_app', '0015_horaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='consignes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='date_publication',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='documents_evaluation/'),
        ),
        migrations.AlterField(
            model_name='horaire',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='cours_app.groupe'),
        ),
    ]
