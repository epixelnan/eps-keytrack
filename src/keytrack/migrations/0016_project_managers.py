# Generated by Django 4.0 on 2021-12-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0015_alter_project_deployment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='managers',
            field=models.ManyToManyField(to='keytrack.Person'),
        ),
    ]
