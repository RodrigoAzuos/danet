# Generated by Django 2.0 on 2019-01-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0004_remove_perfil_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bloqueado',
            field=models.ManyToManyField(related_name='bloqueados', to='perfis.Perfil'),
        ),
    ]
