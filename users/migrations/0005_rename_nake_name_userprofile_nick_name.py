# Generated by Django 4.1.3 on 2023-02-24 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='nake_name',
            new_name='nick_name',
        ),
    ]
