# Generated by Django 5.1 on 2024-09-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours_app', '0011_evaluation_date_limite_consultationdocument_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='soumissionevaluation',
            name='soumission_effectuee',
            field=models.BooleanField(default=False),
        ),
    ]
