# Generated by Django 4.2.8 on 2024-01-23 08:19

from django.db import migrations, models
import mainMessages.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainMessages', '0004_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default_avatar.png', upload_to=mainMessages.models.upload_path),
        ),
    ]