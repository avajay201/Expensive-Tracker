# Generated by Django 4.2.16 on 2024-09-12 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expensiveTracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='current_location',
            new_name='location',
        ),
    ]
