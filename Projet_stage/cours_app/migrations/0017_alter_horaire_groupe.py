# Generated by Django 5.1 on 2024-09-26 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours_app', '0016_evaluation_consignes_evaluation_date_publication_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horaire',
            name='groupe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='horaires', to='cours_app.groupe'),
        ),
    ]
