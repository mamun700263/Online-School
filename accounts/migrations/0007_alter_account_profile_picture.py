# Generated by Django 5.0.4 on 2024-10-13 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_account_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.URLField(blank=True, default='https://i.ibb.co.com/zHJyw5w/User-Profile-PNG-Clipart.png', null=True),
        ),
    ]