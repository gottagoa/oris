# Generated by Django 4.2.4 on 2023-09-07 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_appointment_appointment_datetime_and_more'),
        ('post', '0011_alter_about_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.doctor'),
        ),
    ]
