# Generated by Django 4.1.6 on 2023-08-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engagements', '0004_mouvement_date_alter_engagement_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='depense',
            name='date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='depense',
            name='libelle',
            field=models.CharField(default='ok', max_length=150),
            preserve_default=False,
        ),
    ]
