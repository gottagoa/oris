# Generated by Django 4.2.4 on 2023-09-22 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacy',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Глава'),
        ),
    ]
