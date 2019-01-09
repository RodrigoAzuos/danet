from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Base(models.Model):

    criado_em = models.DateTimeField('Criado em', auto_now_add=True, blank=False, null=False)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

    def get_criado_em(self, format):
        return self.criado_em.__format__(format).__str__()

    def get_atualizado_em(self, format):
        return self.atualizado_em.__format__(format).__str__()

class Perfil(Base):


	SEXO_CHOICES = (
		('M', 'Masculino'),
		('F', 'Feminino'),
	)

	sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
	telefone = models.CharField(max_length = 15, null = False, blank=False)
	nome_empresa = models.CharField(max_length = 255, null = False, blank=False)
	data_nascimento = models.DateField(null=False, blank=False)
	foto = models.ImageField('Foto', upload_to='imagens/%Y/', null=True, blank=True)
	contatos = models.ManyToManyField('Perfil')
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
	bloqueados = models.ManyToManyField('Perfil', related_name='contatos_bloqueados')

	class Meta:
		verbose_name = 'Perfil'
		verbose_name_plural = 'Perfis'

	def __str__(self):
		return "%s %s" % (self.nome(), self.sobrenome())

	def nome(self):
		return self.usuario.first_name

	def sobrenome(self):
		return self.usuario.last_name

	def convidar(self, perfil_convidado):

		c = Convite(solicitante = self, convidado = perfil_convidado)
		c.save()

	def bloquear(self, perfil_bloqueado):

		self.bloqueados.add(perfil_bloqueado)
		self.contatos.remove(perfil_bloqueado)
		perfil_bloqueado.contatos.remove(self)
		perfil_bloqueado.save()
		self.save()

	def desbloquear(self, perfil_bloqueado):

		self.bloqueados.remove(perfil_bloqueado)
		self.contatos.add(perfil_bloqueado)
		perfil_bloqueado.contatos.add(self)
		perfil_bloqueado.save()
		self.save()

	def desfazer_amizade(self, perfil):

		self.contatos.remove(perfil)
		perfil.contatos.remove(self)
		self.save()
		perfil.save()

class Convite(Base):

	solicitante = models.ForeignKey(Perfil, on_delete = models.CASCADE,
									 related_name = 'convites_enviados')
	convidado = models.ForeignKey(Perfil, on_delete = models.CASCADE,
									 related_name = 'convites_recebidos')

	def aceitar(self):
		self.solicitante.contatos.add(self.convidado)
		self.convidado.contatos.add(self.solicitante)
		self.apagar()

	def apagar(self):
		self.delete()

	def __str__(self):
		return 'de %s para %s' % (self.solicitante, self.convidado)

