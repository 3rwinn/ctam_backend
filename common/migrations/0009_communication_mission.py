# Generated by Django 4.1.6 on 2023-09-19 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_alter_timeline_membre'),
    ]

    operations = [
        migrations.AddField(
            model_name='communication',
            name='mission',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='common.mission'),
            preserve_default=False,
        ),
    ]
