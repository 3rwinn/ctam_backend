# Generated by Django 4.1.6 on 2023-07-28 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_remove_palier_libelle_palier_montant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=150)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Nouveau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('prenom', models.CharField(max_length=150)),
                ('sexe', models.CharField(max_length=5)),
                ('fonction', models.CharField(blank=True, max_length=150)),
                ('marie', models.BooleanField(default=False)),
                ('baptise', models.BooleanField(default=False)),
                ('contact', models.CharField(max_length=15)),
                ('habitation', models.CharField(max_length=150)),
                ('encadreur', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('prenom', models.CharField(max_length=150)),
                ('sexe', models.CharField(max_length=5)),
                ('fonction', models.CharField(blank=True, max_length=150)),
                ('marie', models.BooleanField(default=False)),
                ('baptise', models.BooleanField(default=False)),
                ('contact', models.CharField(max_length=15)),
                ('habitation', models.CharField(max_length=150)),
                ('nouveau', models.BooleanField(default=False)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.mission')),
            ],
        ),
    ]