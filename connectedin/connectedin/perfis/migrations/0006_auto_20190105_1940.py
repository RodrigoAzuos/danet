# Generated by Django 2.0 on 2019-01-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0005_perfil_bloqueado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='bloqueado',
        ),
        migrations.AddField(
            model_name='perfil',
            name='bloqueados',
            field=models.ManyToManyField(related_name='contatos_bloqueados', to='perfis.Perfil'),
        ),
    ]
