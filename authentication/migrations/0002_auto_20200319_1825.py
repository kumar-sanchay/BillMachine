# Generated by Django 3.0.4 on 2020-03-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.SlugField(max_length=25, unique=True),
        ),
    ]
