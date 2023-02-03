# Generated by Django 4.1.3 on 2023-02-01 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nake_name', models.CharField(blank=True, default='', max_length=25, verbose_name='昵称')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(choices=[('female', '女'), ('male', '男')], default='male', max_length=6, verbose_name='性别')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='地址')),
                ('image', models.ImageField(default='images/profile.png', upload_to='images/%Y/%m', verbose_name='用户图像')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
    ]
