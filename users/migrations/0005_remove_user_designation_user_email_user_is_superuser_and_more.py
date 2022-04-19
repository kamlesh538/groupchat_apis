# Generated by Django 4.0.4 on 2022-04-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='designation',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
