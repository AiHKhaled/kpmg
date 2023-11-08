# Generated by Django 3.2.12 on 2023-11-06 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Cancelled', 'Cancelled')], default='To Do', max_length=15),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Draft', 'Draft'), ('Completed', 'Completed')], default='Draft', max_length=10),
        ),
    ]
