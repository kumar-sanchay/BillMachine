# Generated by Django 3.0.4 on 2020-03-23 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_billtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
