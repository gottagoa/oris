# Generated by Django 4.2.4 on 2023-08-27 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_contacts_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='category/default.jpg', upload_to='category/image/', verbose_name='Картинка'),
        ),
    ]
