# Generated by Django 4.1.6 on 2023-09-05 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_remove_palier_libelle_palier_montant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SuiviBanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('montant', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('action', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SortieCaisse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.mission')),
                ('type_sortie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.typesortie')),
            ],
        ),
        migrations.CreateModel(
            name='FicheDimanche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('entrees', models.JSONField()),
                ('sorties', models.JSONField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.mission')),
            ],
        ),
        migrations.CreateModel(
            name='EntreeCaisse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.mission')),
                ('type_entree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.typeentree')),
            ],
        ),
    ]
