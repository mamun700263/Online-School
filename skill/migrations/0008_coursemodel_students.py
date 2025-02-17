# Generated by Django 5.0.4 on 2024-09-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_unique_id'),
        ('skill', '0007_alter_coursemodel_taken_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='enrolled_courses', to='accounts.studentaccount'),
        ),
    ]
