# Generated by Django 4.1.3 on 2022-11-10 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='flight',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'managed': False},
        ),
    ]