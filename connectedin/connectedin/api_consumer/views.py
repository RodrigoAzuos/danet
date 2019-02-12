from django.shortcuts import render
from rest_framework.authtoken.models import Token
import requests
# Create your views here.
from perfis.models import Justificativa

BASE_URL = 'http://localhost:8000/api/v1/'

def get_token(usuario, senha):

    body = {'username': usuario,
            'password': senha}

    url = BASE_URL + 'token/'
    #
    headers = {
        "Content-Type": "application/json"
        }

    token = requests.post(url, json=body, headers=headers).json()['token']

    return token

def get_posts(token):

    token = 'token %s' %token
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
                }

    url = BASE_URL +'posts'

    posts = requests.get(url,headers=headers).json()

    return posts

def post_justificativa(token, descricao):

    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    url = BASE_URL + 'perfil/justificativa'

    body = {'descricao': descricao}

    return requests.post(url, json=body, headers=headers).json()

def confirmar_justificativa(token, pk):
    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    url = BASE_URL + 'perfil/justificativa/%s'%pk

    return requests.put(url, headers=headers).json()

def deletar_justificativa(token, pk):
    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    url = BASE_URL + 'perfil/justificativa/%s'%pk

    return requests.delete(url, headers=headers).json()

def reagir(token,pk, reacao):

    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    if reacao == '1':
        url = BASE_URL + 'posts/%d/reacao/like' %pk
    elif reacao == '2':
        url = BASE_URL + 'posts/%d/reacao/dislike' % pk


    return requests.get(url, headers=headers)

def comentar(token,pk,descricao):
    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    body = {'descricao': descricao}

    url = BASE_URL + 'posts/%d/comentarios/' % pk
    print(url)
    return requests.post(url, json=body, headers=headers).json()


def delete_comentario(token,post_id,pk):
    token = 'token %s' % token

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    url = BASE_URL + 'posts/%d/comentarios/%d' % (post_id, pk)

    return requests.delete(url, headers=headers)







