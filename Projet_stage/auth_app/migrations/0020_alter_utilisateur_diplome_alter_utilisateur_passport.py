# Generated by Django 5.1 on 2024-09-16 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0019_alter_utilisateur_diplome_alter_utilisateur_passport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='diplome',
            field=models.FileField(default=None, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='passport',
            field=models.FileField(default=None, upload_to='documents/'),
        ),
    ]
