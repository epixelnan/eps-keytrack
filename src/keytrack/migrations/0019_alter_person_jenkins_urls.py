# Generated by Django 4.0 on 2022-01-03 06:52

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0018_alter_person_jenkins_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='jenkins_urls',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=4096), default=list, size=None),
        ),
    ]
