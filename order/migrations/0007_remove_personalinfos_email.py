# Generated by Django 3.2.8 on 2021-10-29 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20211028_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinfos',
            name='email',
        ),
    ]
