# Generated by Django 5.2.3 on 2025-06-25 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='task',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
