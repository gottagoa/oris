# Generated by Django 4.2.4 on 2023-08-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_alter_about_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(default='service/default.jpg', upload_to='service/image/', verbose_name='Иконка'),
        ),
    ]
