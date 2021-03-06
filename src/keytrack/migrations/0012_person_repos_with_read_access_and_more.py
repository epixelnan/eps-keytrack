# Generated by Django 4.0 on 2021-12-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0011_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='repos_with_read_access',
            field=models.ManyToManyField(related_name='repo_reader', to='keytrack.Repository'),
        ),
        migrations.AddField(
            model_name='person',
            name='repos_with_write_access',
            field=models.ManyToManyField(related_name='repo_writer', to='keytrack.Repository'),
        ),
    ]
