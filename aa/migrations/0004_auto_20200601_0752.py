# Generated by Django 3.0.6 on 2020-06-01 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa', '0003_auto_20200531_2335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockquotes',
            old_name='Change',
            new_name='change',
        ),
    ]
