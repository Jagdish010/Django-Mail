# Generated by Django 2.2.17 on 2021-05-09 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0007_customerfeedback_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerfeedback',
            name='feedback_notification',
            field=models.BooleanField(default=False, verbose_name='Notification'),
        ),
    ]
