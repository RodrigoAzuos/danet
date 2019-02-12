from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


from django.db import transaction
from django.forms import forms

from perfis.views import get_perfil_logado, criar_alerta, TIPOS_ALERTA
from usuarios.forms import RegistrarUsuarioForm
from perfis.models import Perfil

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
import os

# Create your views here.

# metodo api_consumer
from api_consumer.views import get_token


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        print(password)

        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Este usuario não existe!')
            return render(request, 'login.html', {'form': form})

        match_check = check_password(password,usuario.password)
        if not match_check:
            messages.error(request, 'Usuário e/ou senha incorretos')

            return render(request, 'login.html', {'form': form})
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                get_token(username,password)
                auth_login(request, user)
                return redirect('index')
    elif request.method == 'GET':
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


class RegistrarUsuarioView(View):

    def get(self, request):
        form = RegistrarUsuarioForm

        return render(request, 'registrar.html', {'form': form})

    @transaction.Atomic(using=None, savepoint=True)
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST, request.FILES)

        if (form.is_valid()):
            dados = form.data
            try:
                foto = request.FILES['foto']
            except:
                foto = None

            try:
                perfil = Perfil(sexo=dados['sexo'],
                                telefone=dados['telefone'],
                                nome_empresa=dados['nome_empresa'],
                                data_nascimento=dados['data_nascimento'],
                                foto=foto)

                usuario = User.objects.create_user(username=dados['usuario'],
                                                   first_name=dados['first_name'],
                                                   last_name=dados['last_name'],
                                                   email=dados['email'],
                                                   password=dados['senha'])

                perfil.usuario = usuario
                perfil.save()

                return redirect('index')

            except(ValidationError):
                #usuario.delete()
                form.adiciona_erro("Digite uma data no formato YYYY-mm-dd")
            # except:
            #     usuario.delete()

        return render(request, 'registrar.html', {'form': form})

class RegistrarSuperUsuarioView(View):
    pass
    #
    # def get(self, request):
    #
    #     form = RegistrarUsuarioForm
    #     return render(request, 'registrar.html', {'form': form})
    #
    # def post(self, request):
    #     form = RegistrarUsuarioForm(request.POST, request.FILES)
    #
    #     if (form.is_valid()):
    #         dados = form.data
    #
    #
    #         try:
    #             perfil = Perfil(sexo=dados['sexo'],
    #                         telefone=dados['telefone'],
    #                         nome_empresa=dados['nome_empresa'],
    #                         data_nascimento=dados['data_nascimento'],
    #                         foto=dados['foto'])
    #
    #             usuario = User.objects.create_superuser(username=dados['usuario'],
    #                                                first_name=dados['first_name'],
    #                                                last_name=dados['last_name'],
    #                                                email=dados['email'],
    #                                                password=dados['senha'])
    #
    #             perfil.usuario = usuario
    #             perfil.save()
    #             return redirect('index')
    #
    #         except(ValidationError):
    #             usuario.delete()
    #             form.adiciona_erro("Digite uma data no formato YYYY-mm-dd")
    #
    #
    #     return render(request, 'registrar.html', {'form': form})

class AlterarSenhaView(View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        logado = get_perfil_logado(request)
        perfis = Perfil.Objects.all()

        return render(request, 'minha_pagina.html',
                       {'form': form, 'logado': logado, 'perfis':perfis})

    def post(self, request):

        logado = get_perfil_logado(request)
        form = PasswordChangeForm(request.user, request.POST)
        perfis = Perfil.objects.all()

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha alterada com sucesso!')

            return render(request, 'minha_pagina.html',
                          {'form': form, 'logado': logado, 'perfis':perfis})
        else:
            messages.error(request, 'Algo de erado com sua senha')

        return render(request, 'minha_pagina.html',
                      {'form': form, 'logado': logado,'perfis':perfis})

@login_required(login_url='/login')
def tornar_superuser(request, perfil_id):

    logado = get_perfil_logado(request)

    if logado.usuario.is_superuser:
        perfil = Perfil.objects.get(pk=perfil_id)
        perfil.usuario.is_superuser = True
        perfil.usuario.save()
        criar_alerta(request, "Super usuário criado com sucesso", TIPOS_ALERTA[0])
        return redirect('index')

    criar_alerta(request, "Você precisa ser um super usuário", TIPOS_ALERTA[2])
    return redirect('index')

@login_required(login_url='/login')
def alterar_foto(request):
    logado = get_perfil_logado(request)
    try:
        foto = request.FILES['foto']
    except:
        criar_alerta(request, "Envie uma foto válida", TIPOS_ALERTA[2])
        foto = None

    if request.method == 'POST':

        logado.foto = foto
        logado.save()

        criar_alerta(request, "Foto alterada com secesso!", TIPOS_ALERTA[0])
        return redirect('index')

