# Generated by Django 4.2.4 on 2023-09-09 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_alter_about_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='post/image/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерея',
            },
        ),
        migrations.AlterField(
            model_name='about',
            name='page',
            field=models.CharField(choices=[('about', 'About'), ('doctors', 'Doctors'), ('services', 'Services'), ('categories', 'cateogories'), ('index', 'index'), ('faq', 'faq'), ('gallery', 'gallery')], max_length=30, null=True, verbose_name='Страница'),
        ),
    ]
