# Generated by Django 5.0.4 on 2024-08-30 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mobile',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]