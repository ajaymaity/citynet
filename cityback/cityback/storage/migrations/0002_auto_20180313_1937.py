# Generated by Django 2.0.2 on 2018-03-13 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dublinbikesstationrealtimeupdate',
            name='last_update',
            field=models.DateTimeField(null=True),
        ),
    ]