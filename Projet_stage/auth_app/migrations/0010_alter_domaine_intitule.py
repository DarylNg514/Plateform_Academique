# Generated by Django 5.1 on 2024-08-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0009_alter_domaine_code_programme_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domaine',
            name='intitule',
            field=models.CharField(max_length=500),
        ),
    ]
