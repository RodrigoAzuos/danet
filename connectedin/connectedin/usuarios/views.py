from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic.base import View

from perfis.views import get_perfil_logado
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.models import User
from perfis.models import Perfil
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

class RegistrarUsuarioView(View):

    def get(self, request):
        form = RegistrarUsuarioForm
        print(form)
        return render(request, 'registrar.html', {'form': form})

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        print(form.data)

        if (form.is_valid()):
            dados = form.data

            try:
                perfil = Perfil(sexo=dados['sexo'],
                            telefone=dados['telefone'],
                            data_nascimento=dados['data_nascimento'])

                usuario = User.objects.create_user(username=dados['usuario'],
                                                   first_name=dados['first_name'],
                                                   last_name=dados['last_name'],
                                                   email=dados['email'],
                                                   password=dados['senha'])

                perfil.usuario = usuario

                perfil.save()

                return redirect('index')

            except(ValidationError):
                usuario.delete()
                form.adiciona_erro("Digite uma data no formato YYYY-mm-dd")


        return render(request, 'registrar.html', {'form': form})


class RegistrarSuperUsuarioView(View):

    def get(self, request):
        print("super")
        form = RegistrarUsuarioForm
        return render(request, 'registrar.html', {'form': form})

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)

        if (form.is_valid()):
            dados = form.data
            print("super")

            try:
                perfil = Perfil(sexo=dados['sexo'],
                            telefone=dados['telefone'],
                            data_nascimento=dados['data_nascimento'])

                usuario = User.objects.create_superuser(username=dados['usuario'],
                                                   first_name=dados['first_name'],
                                                   last_name=dados['last_name'],
                                                   email=dados['email'],
                                                   password=dados['senha'])

                perfil.usuario = usuario
                perfil.save()
                return redirect('index')

            except(ValidationError):
                usuario.delete()
                form.adiciona_erro("Digite uma data no formato YYYY-mm-dd")


        return render(request, 'registrar.html', {'form': form})


class AlterarSenhaView(View):


    def get(self, request):
        form = PasswordChangeForm(request.user)
        logado = get_perfil_logado(request)

        return render(request, 'minha_pagina.html',
                       {'form': form, 'logado': logado})

    def post(self, request):

        logado = get_perfil_logado(request)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha alterada com sucesso!')

            return render(request, 'minha_pagina.html',
                          {'form': form, 'logado': logado})
        else:
            messages.error(request, 'Algo de erado com sua senha')

        return render(request, 'minha_pagina.html',
                      {'form': form, 'logado': logado})