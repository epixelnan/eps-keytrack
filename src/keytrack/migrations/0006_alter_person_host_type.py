# Generated by Django 4.0 on 2021-12-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytrack', '0005_person_host_ip_person_host_name_person_host_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='host_type',
            field=models.CharField(choices=[('mswin', 'Windows'), ('mac', 'Mac OS'), ('linux', 'Linux-based'), ('other', 'Other')], default='other', max_length=32),
        ),
    ]
