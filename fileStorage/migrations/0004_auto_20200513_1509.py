# Generated by Django 3.0.4 on 2020-05-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileStorage', '0003_filestorage_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='filestorage',
            name='cgst',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='filestorage',
            name='gst',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='filestorage',
            name='igst',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='filestorage',
            name='sgst',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
