# Generated by Django 3.0.2 on 2020-11-03 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20201103_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='Image',
        ),
    ]
