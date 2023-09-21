# Generated by Django 4.2.4 on 2023-09-02 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_appointment_patient_name_appointment_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_datetime',
        ),
        migrations.AddField(
            model_name='appointment',
            name='day',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]