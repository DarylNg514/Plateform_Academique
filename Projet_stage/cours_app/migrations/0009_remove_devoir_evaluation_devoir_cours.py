# Generated by Django 5.1 on 2024-09-20 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours_app', '0008_devoir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devoir',
            name='evaluation',
        ),
        migrations.AddField(
            model_name='devoir',
            name='Cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devoirs', to='cours_app.cours'),
        ),
    ]
