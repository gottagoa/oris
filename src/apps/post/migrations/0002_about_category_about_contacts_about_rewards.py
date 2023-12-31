# Generated by Django 4.2.4 on 2023-08-26 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='category',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='about', to='post.category'),
        ),
        migrations.AddField(
            model_name='about',
            name='contacts',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to='post.contacts'),
        ),
        migrations.AddField(
            model_name='about',
            name='rewards',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rewards', to='post.rewards'),
        ),
    ]
