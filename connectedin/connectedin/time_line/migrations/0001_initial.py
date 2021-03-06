# Generated by Django 2.0 on 2019-01-03 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('descricao', models.CharField(max_length=256, verbose_name='Descricao')),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('titulo', models.CharField(max_length=128, verbose_name='Titulo')),
                ('resumo', models.CharField(max_length=10000, verbose_name='Resumo')),
                ('tags', models.CharField(blank=True, max_length=255, null=True, verbose_name='Palavra_chave')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='imagens/%Y/', verbose_name='Foto')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='perfis.Perfil')),
                ('curtidas', models.ManyToManyField(related_name='posts_curtidos', to='perfis.Perfil')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.AddField(
            model_name='comentario',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='time_line.Post'),
        ),
    ]
