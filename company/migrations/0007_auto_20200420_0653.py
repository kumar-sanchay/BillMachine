# Generated by Django 3.0.4 on 2020-04-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_company_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=50, verbose_name='company name'),
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]
