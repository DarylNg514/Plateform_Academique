# Generated by Django 5.1 on 2024-09-16 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0018_delete_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='diplome',
            field=models.FileField(blank=True, default=None, null=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='passport',
            field=models.FileField(blank=True, default=None, null=True, upload_to='documents/'),
        ),
    ]
