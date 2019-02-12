from django.db import models

# Create your models here.
from perfis.models import Base, Perfil


class Post(Base):

    resumo = models.CharField('Resumo', max_length=10000, null=False, blank=False)
    autor = models.ForeignKey(Perfil, null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    foto = models.ImageField('Foto', upload_to='imagens/%Y/',null=True,blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def apagar(self, super_user, autor):
        if super_user or autor == self.autor:
            self.delete()

    def adicionar_tag(self, tag):
        self.tags.add(tag)
        self.save()

    def like(self):

        return len(self.reacoes.all().filter(tipo='like'))

    def dislike(self):
        return len(self.reacoes.all().filter(tipo='dislike'))

    def __str__(self):
        return self.resumo

class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comentarios', blank=False, null=False)
    perfil = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name= 'meus_comentarios', blank=False, null=False )

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.descricao

class Alerta(models.Model):

    mensagem = models.CharField('Mensagem', max_length=256, blank=False, null=False)
    tipo = models.CharField('Mensagem', max_length=256, blank=False, null=False)
    perfil = models.ForeignKey(Perfil, on_delete = models.CASCADE, related_name = 'alertas', blank=False, null=False)

    def __str__(self):
        return self.mensagem

class Reacao(Base):

    REACAO_CHOICE = (
        ('l', 'like'),
        ('d', 'dislike'),
    )

    tipo = models.CharField(max_length=1,choices=REACAO_CHOICE, default='l')
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=False,blank=False, related_name='minhas_reacoes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False,blank=False, related_name='reacoes')

    def __str__(self):
        return self.tipo

class Tag(Base):

    descricao = models.CharField(max_length=256, null=False,blank=False)

    def __str__(self):
        return self.descricao

