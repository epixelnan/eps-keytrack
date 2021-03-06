# Generated by Django 4.0 on 2021-12-23 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0009_person_projects_with_db_access_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deployment_type',
            field=models.CharField(choices=[('manual', 'Manual'), ('docker', 'Docker'), ('k8s', 'Kubernetes')], default='other', max_length=32),
        ),
        migrations.AddField(
            model_name='project',
            name='framework',
            field=models.CharField(choices=[('drupal', 'Drupal'), ('django', 'Django'), ('other', 'Other')], default='other', max_length=32),
        ),
    ]
