# Generated by Django 5.0.4 on 2024-09-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
