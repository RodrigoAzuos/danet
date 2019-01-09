from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Perfil, Convite

# Create your views here.

@login_required(login_url='/login')
def index(request):
	form = PasswordChangeForm(request.user)
	logado = get_perfil_logado(request)

	return render(request, 'minha_pagina.html', { 'logado' : logado, 'form': form})

def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id = perfil_id)
	logado = get_perfil_logado(request)
	convidar = pode_convidar(request, perfil_id)

	if logado in perfil.bloqueados.all() or perfil in logado.bloqueados.all():
		return redirect('time_line')

	return render(request, 'perfil.html', 
		          {'perfil' : perfil, 'logado': logado, 'convidar':convidar})

@login_required(login_url='/login')
def convidar(request, perfil_id):

	if pode_convidar(request,perfil_id):
		perfil = get_perfil_logado(request)
		perfil_convidado = Perfil.objects.get(id = perfil_id)
		perfil.convidar(perfil_convidado)
		return redirect('time_line')

@login_required(login_url='/login')
def get_perfil_logado(request):

	perfil = Perfil
	if request.user.perfil:
		return request.user.perfil

	return perfil

@login_required(login_url='/login')
def aceitar(request, convite_id):

	convite = Convite.objects.get(pk=convite_id)
	convite.aceitar()
	return redirect('index')

@login_required(login_url='/login')
def apagar(request, convite_id):

	convite = Convite.objects.get(pk=convite_id)
	convite.apagar()
	return redirect('index')

@login_required(login_url='/login')
def bloquear_contato(request, perfil_id):

	perfil = get_perfil_logado(request)
	perfil_bloqueado = Perfil.objects.get(pk=perfil_id)
	perfil.bloquear(perfil_bloqueado)

	return redirect('time_line')

@login_required(login_url='/login')
def desbloquear_contato(request, perfil_id):

	perfil = get_perfil_logado(request)
	perfil_bloqueado = Perfil.objects.get(pk=perfil_id)
	perfil.desbloquear(perfil_bloqueado)

	return redirect('index')

@login_required(login_url='/login')
def desfazer_amizade(request, perfil_id):

	perfil = Perfil.objects.get(pk=perfil_id)
	get_perfil_logado(request).desfazer_amizade(perfil)

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

	return True





