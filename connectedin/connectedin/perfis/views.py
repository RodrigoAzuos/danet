from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.db import transaction
from time_line.models import Alerta
from .models import Perfil, Convite, Justificativa
from .forms import JusificativaForm

# Create your views here.
TIPOS_ALERTA = ['success', 'warning', 'danger']
@login_required(login_url='/login')
def index(request):

	form = PasswordChangeForm(request.user)
	logado = get_perfil_logado(request)
	perfis = Perfil.objects.all()
	alerta = get_alerta(request)
	get_alerta(request)
	if logado.desativado():
		return redirect('ativar_conta')

	return render(request, 'minha_pagina.html', { 'logado' : logado, 'form': form,
												  'perfis':perfis, 'alerta':alerta,
												  'tipos':TIPOS_ALERTA})

@login_required(login_url='/login')
def exibir_perfil(request, perfil_id):

	logado = get_perfil_logado(request)

	if logado.desativado():
		return redirect('ativar_conta')

	perfil = Perfil.objects.get(id = perfil_id)
	convidar = pode_convidar(request, perfil_id)
	desativado = perfil.desativado()

	if logado in perfil.bloqueados.all() or perfil in logado.bloqueados.all():
		return redirect('time_line')

	return render(request, 'perfil.html',
				  {'perfil' : perfil, 'logado': logado, 'convidar':convidar, 'desativado':desativado})

@login_required(login_url='/login')
def convidar(request, perfil_id):

	if pode_convidar(request,perfil_id):
		perfil = get_perfil_logado(request)
		perfil_convidado = Perfil.objects.get(id = perfil_id)
		perfil.convidar(perfil_convidado)

		criar_alerta(request, "Convite enviado, aguarde ser aceito!", TIPOS_ALERTA[0])
		return redirect('time_line')

@login_required(login_url='/login')
def get_perfil_logado(request):

	perfil = Perfil
	if request.user.perfil:
		return request.user.perfil

	return perfil

@transaction.Atomic(using=None, savepoint=True)
@login_required(login_url='/login')
def aceitar(request, convite_id):

	convite = Convite.objects.get(pk=convite_id)
	convite.aceitar()

	criar_alerta(request, "Convite aceito, agora podem ficar por dentro de tudo que acontece.", TIPOS_ALERTA[0])

	return redirect('index')

@transaction.Atomic(using=None, savepoint=True)
@login_required(login_url='/login')
def apagar(request, convite_id):

	convite = Convite.objects.get(pk=convite_id)
	convite.apagar()
	criar_alerta(request, "Convite ignorado, não se preocupe que manteremos o sigilo", TIPOS_ALERTA[2])
	return redirect('index')

@login_required(login_url='/login')
def bloquear_contato(request, perfil_id):

	perfil = get_perfil_logado(request)
	perfil_bloqueado = Perfil.objects.get(pk=perfil_id)
	perfil.bloquear(perfil_bloqueado)

	criar_alerta(request, "Contato bloqueado, faça desbloqueio na sua tela de perfil assim que resolver essa questão. Enaquanto isso ele não poderá ver nada a seu respeito ;)"
				 , TIPOS_ALERTA[1])

	return redirect('time_line')

@login_required(login_url='/login')
def desbloquear_contato(request, perfil_id):

	perfil = get_perfil_logado(request)
	perfil_bloqueado = Perfil.objects.get(pk=perfil_id)
	perfil.desbloquear(perfil_bloqueado)

	criar_alerta(request,"Contato desbloqueado, Tudo volta a ser como era antes, Aproveite! ;)" , TIPOS_ALERTA[0])

	return redirect('index')

@transaction.Atomic(using=None, savepoint=True)
@login_required(login_url='/login')
def desfazer_amizade(request, perfil_id):

	perfil = Perfil.objects.get(pk=perfil_id)
	get_perfil_logado(request).desfazer_amizade(perfil)

	criar_alerta(request, "Amizade desfeita, poderá mandar outro convite quando achar coveniente ;)", TIPOS_ALERTA[1])

	return redirect('index')

def pode_convidar(request, perfil_id):

	perfil = Perfil.objects.get(pk=perfil_id)
	logado= get_perfil_logado(request)

	for convite in logado.convites_enviados.all():
		if convite.convidado == perfil:
			return False

	for convite in logado.convites_recebidos.all():
		if convite.solicitante == perfil:
			return False

	if logado in perfil.contatos.all() or logado in perfil.bloqueados.all():
			return False

	if logado in perfil.bloqueados.all() or perfil in logado.bloqueados.all():
		return False

	if logado.pk == perfil_id:
		return False

	return True
@login_required(login_url='/login')
def desativar_conta(request):

	form = PasswordChangeForm(request.user)
	form_justificativa = JusificativaForm()
	logado = get_perfil_logado(request)
	perfis = Perfil.objects.all()

	if request.method == "GET":

		return render(request,"desativar_conta.html",
					  { 'logado' : logado, 'form': form, 'perfis':perfis, 'form_justificativa':form_justificativa})

	elif request.method == "POST":

		form_justificativa = JusificativaForm(request.POST)

		if not conta_desativada_logado(request):

			if form_justificativa.is_valid():

				model_instance = form_justificativa.save(commit=False)
				model_instance.perfil = get_perfil_logado(request)
				model_instance.save()

				justificativa = Justificativa.objects.get(pk=model_instance.pk)

				return render(request, "desativar_conta.html",
						  {'logado': logado, 'form': form, 'perfis': perfis,
						   'form_justificativa': form_justificativa,'justificativa':justificativa} )

		return redirect('index')

@login_required(login_url='/login')
def confirmar_justificativa(request, justificativa_id):

	justificativa = Justificativa.objects.get(pk=justificativa_id)
	justificativa.confirmar()

	return redirect('logout')

@login_required(login_url='/login')
def apagar_justificativa(request, justificativa_id):

	justificativa = Justificativa.objects.get(pk=justificativa_id)
	justificativa.invalidar()

	criar_alerta(request, "Bloqueio de conta não confirmado ;)", TIPOS_ALERTA[1])

	return redirect('index')

def conta_desativada_logado(request):

	logado = get_perfil_logado(request)

	return logado.desativado()

def conta_desativada(request, perfil_id):

	perfil = Perfil.objects.get(pk=perfil_id)
	desativado = perfil.justificativas.filter(situacao=True).exists()

	return desativado

def ativar_conta(request):
	logado = get_perfil_logado(request)
	justificativa = logado.justificativas.get(situacao=True)
	logado = get_perfil_logado(request)

	return render(request, "ativar_conta.html", {'logado':logado, 'justificativa' : justificativa})

def get_alerta(request):
	alert = None
	try:
		alerta = Alerta.objects.all().filter(perfil=get_perfil_logado(request))[0]
		alert = alerta
	except Exception as e:
		alerta = None
		return alerta
	alerta.delete()
	return alert

def criar_alerta(request, mensagem, tipo):

	alerta = Alerta.objects.create(mensagem=mensagem,
						  tipo=tipo,
						  perfil=get_perfil_logado(request))

	return alerta