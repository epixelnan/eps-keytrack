# Generated by Django 4.0.4 on 2022-07-10 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0028_remove_person_managers_person_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='hosts',
        ),
        migrations.AddField(
            model_name='host',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='keytrack.person'),
            preserve_default=False,
        ),
    ]
