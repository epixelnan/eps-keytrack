# Generated by Django 4.0 on 2021-12-23 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0010_project_deployment_type_project_framework'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=4096)),
            ],
        ),
    ]
