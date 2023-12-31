# Generated by Django 4.2.4 on 2023-08-26 01:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user/images/', verbose_name='Аватар')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('mobile', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=10, null=True, verbose_name='Пол')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный аккаунт')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Пользователь не является специалистом')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.TextField(blank=True, null=True, verbose_name='Квалификация')),
                ('experience', models.CharField(blank=True, max_length=5, null=True, verbose_name='Опыт работы')),
                ('education', models.TextField(blank=True, null=True, verbose_name='Образование')),
                ('certifications', models.TextField(blank=True, null=True, verbose_name='Сертификаты')),
                ('speciality', models.CharField(blank=True, max_length=200, null=True, verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Специалист',
                'verbose_name_plural': 'Специалисты',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
            },
        ),
    ]
