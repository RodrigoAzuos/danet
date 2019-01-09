from django.db import models

# Create your models here.
from perfis.models import Base, Perfil


class Post(Base):

    resumo = models.CharField('Resumo', max_length=10000, null=False, blank=False)
    autor = models.ForeignKey(Perfil, null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
    curtidas = models.ManyToManyField(Perfil, related_name='posts_curtidos')
    foto = models.ImageField('Foto', upload_to='imagens/%Y/',null=True,blank=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def apagar(self, super_user, autor):
        if super_user or autor == self.autor:
            self.delete()

    def __str__(self):
        return self.descricao

class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comentarios', blank=False, null=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.descricao