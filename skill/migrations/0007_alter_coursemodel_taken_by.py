# Generated by Django 5.0.4 on 2024-09-13 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_profile_picture'),
        ('skill', '0006_coursemodel_description_coursemodel_skills_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='taken_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='accounts.teacheraccount'),
        ),
    ]
