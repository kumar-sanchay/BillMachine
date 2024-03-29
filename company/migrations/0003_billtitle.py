# Generated by Django 3.0.4 on 2020-03-18 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20200318_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title1', models.CharField(max_length=10)),
                ('title2', models.CharField(blank=True, max_length=10, null=True)),
                ('title3', models.CharField(blank=True, max_length=10, null=True)),
                ('title4', models.CharField(blank=True, max_length=10, null=True)),
                ('title5', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_company_title', to='company.Company')),
            ],
            options={
                'verbose_name': 'Bill Title',
                'verbose_name_plural': 'Bill Titles',
            },
        ),
    ]
