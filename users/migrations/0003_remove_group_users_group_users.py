# Generated by Django 4.0.4 on 2022-04-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='users',
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to='users.user'),
        ),
    ]
