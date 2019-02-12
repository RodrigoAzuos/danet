from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View
# Create your views here.
from perfis.models import Perfil
from perfis.views import get_perfil_logado,conta_desativada_logado, get_alerta, TIPOS_ALERTA, criar_alerta
from time_line.forms import PostModelForm
from time_line.models import Post, Tag
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from rest_framework.authtoken.models import Token

from api_consumer.views import get_posts, reagir as reagir_api, comentar as comentar_api, delete_comentario


class TimeLinePost(View):

    def get(self, request):

        form = PostModelForm()
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None
        alerta = get_alerta(request)
        tags = Tag.objects.all().order_by('-id')[:3:1]

        token = Token.objects.get(user_id=logado.id)


        if logado.desativado():
            return redirect('ativar_conta')

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:

            resultados = filtrar(request, perfis, logado, filtro)

        posts_list = get_posts(token)

        if logado.usuario.is_superuser:
            # posts_list = Post.objects.all().order_by('-criado_em')
            posts_list = get_posts(token)


        paginator = Paginator(posts_list, 8)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            posts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            posts = paginator.page(paginator.num_pages)

        return render(request, 'time_line.html', {'form':form, 'posts':posts,'tags':tags,
                                                  'logado': logado, 'resultados': resultados,
                                                  'alerta':alerta, 'tipos':TIPOS_ALERTA})

    def post(self, request):

        form = PostModelForm(request.POST, request.FILES)
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None
        alerta = get_alerta(request)
        tags = Tag.objects.all().order_by('-id')[:3:1]

        if logado.desativado():
            return redirect('ativar_conta')

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:
            resultados = filtrar(request,perfis,logado,filtro)

        posts_list = Post.objects.all().filter(autor__contatos=logado).order_by('-criado_em') | \
                     Post.objects.all().filter(autor=logado).order_by('-criado_em')

        if logado.usuario.is_superuser:
            posts_list = Post.objects.all().order_by('-criado_em')

        paginator = Paginator(posts_list, 8)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            posts = paginator.page(page)
        except (EmptyPage, InvalidPage):
            posts = paginator.page(paginator.num_pages)

        if form.is_valid():

            # model_instance = form.save(commit=False)
            dados = form.data
            try:
                foto = request.FILES['foto']
            except:
                foto = None

            post = Post(autor=logado,
                        resumo= dados['resumo'],
                        foto = foto)
            tags = dados['tags'].split(',')
            post.save()

            criar_tags(tags,post)




            return redirect('time_line')

        print(form.errors)

        return render(request, 'time_line.html', {'form': form, 'posts': posts,'tags':tags,
                                                  'logado': logado, 'resultados': resultados,
                                                  'alerta': alerta, 'tipos': TIPOS_ALERTA})

@login_required(login_url='/login')
def apagar_postagem(request, post_id):

    autor = get_perfil_logado(request)
    super_user = autor.usuario.is_superuser
    post = Post.objects.get(pk=post_id)
    post.apagar(super_user,autor)

    criar_alerta(request, "Post deletado", TIPOS_ALERTA[2])

    return redirect('time_line')

def filtrar(request, perfis, logado, filtro):
    print('oi')
    resultados = perfis.filter(usuario__username__icontains=filtro)

    for perfil in resultados:

        if perfil in get_perfil_logado(request).bloqueados.all():
            resultados = resultados.exclude(pk=perfil.pk)

        if get_perfil_logado(request) in perfil.bloqueados.all():
            resultados = resultados.exclude(pk=perfil.pk)

    return resultados

def criar_tags(tags,post):

    tag_list = []

    for tag in tags:

        if Tag.objects.filter(descricao=tag).exists():
            post.adicionar_tag(Tag.objects.get(descricao=tag))

        else:
            nova_tag = Tag(descricao=tag)
            nova_tag.save()
            post.adicionar_tag(nova_tag)


    return tag_list

class BuscarPostTag(View):

    def get(self, request, tag_id):

        form = PostModelForm()
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None
        alerta = get_alerta(request)

        post_list = Post.objects.all().filter(tags=tag_id)
        tags = Tag.objects.all().order_by('-id')[:3:1]


        return render(request, 'time_line.html', {'form': form, 'posts': post_list,
                                                  'logado': logado, 'resultados': resultados,
                                                  'alerta': alerta, 'tipos': TIPOS_ALERTA, 'tags':tags})

class PesquisaPostTag(View):

    def get(self, request):

        form = PostModelForm()
        logado = get_perfil_logado(request)
        filtro = None
        resultados = None
        alerta = get_alerta(request)
        tags = Tag.objects.all().order_by('-id')[:3:1]

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:

            tag = Tag.objects.all().filter(descricao__icontains=filtro)
            resultados = Post.objects.all().filter(tags=tag[0].id)


        return render(request, 'time_line.html', {'form': form, 'posts': resultados,
                                                  'logado': logado, 'alerta': alerta, 'tipos': TIPOS_ALERTA, 'tags': tags})

def reagir(request, pk,reacao):

    logado = get_perfil_logado(request)
    token = Token.objects.get(user_id=logado.id)
    reagir_api(token, pk,reacao)

    return redirect('time_line')

def comentar(request, post_id):

    logado = get_perfil_logado(request)
    token = Token.objects.get(user_id=logado.id)
    comentar_api(token, post_id,request.POST['comentario'])

    print(request.stream)

    return redirect('time_line')

def deletar_comentario(request,post_id,pk):

    logado = get_perfil_logado(request)
    token = Token.objects.get(user_id=logado.id)
    delete_comentario(token,post_id,pk)

    return redirect('time_line')













