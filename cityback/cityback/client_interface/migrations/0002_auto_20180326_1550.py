# Generated by Django 2.0.2 on 2018-03-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dublinbikesstationaverage',
            name='time',
            field=models.TimeField(db_index=True, null=True),
        ),
    ]
