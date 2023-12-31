# Generated by Django 4.2.4 on 2023-09-13 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_appointment_appointment_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='medical_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='patient_files/'),
        ),
    ]
