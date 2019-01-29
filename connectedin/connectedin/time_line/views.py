from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View
# Create your views here.
from perfis.models import Perfil
from perfis.views import get_perfil_logado,conta_desativada_logado, get_alerta, TIPOS_ALERTA, criar_alerta
from time_line.forms import PostModelForm
from time_line.models import Post
from django.core.paginator import Paginator, InvalidPage, EmptyPage


class TimeLinePost(View):

    def get(self, request):

        form = PostModelForm()
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None
        alerta = get_alerta(request)

        if logado.desativado():
            return redirect('ativar_conta')

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:
            resultados = perfis.filter(usuario__username__icontains=filtro)


            for perfil in resultados:

                if perfil in get_perfil_logado(request).bloqueados.all():
                    resultados = resultados.exclude(pk=perfil.pk)


                if get_perfil_logado(request) in perfil.bloqueados.all():
                   resultados = resultados.exclude(pk=perfil.pk)

        posts_list = Post.objects.all().filter(autor__contatos=logado).order_by('-criado_em') |\
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

        return render(request, 'time_line.html', {'form':form, 'posts':posts,
                                                  'logado': logado, 'resultados': resultados,
                                                  'alerta':alerta, 'tipos':TIPOS_ALERTA})

    def post(self, request):

        form = PostModelForm(request.POST, request.FILES)
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None
        alerta = get_alerta(request)

        if logado.desativado():
            return redirect('ativar_conta')

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:
            resultados = perfis.filter(usuario__username__icontains=filtro)

            for perfil in resultados:

                if perfil in get_perfil_logado(request).bloqueados.all():
                    resultados = resultados.exclude(pk=perfil.pk)

                if get_perfil_logado(request) in perfil.bloqueados.all():
                    resultados = resultados.exclude(pk=perfil.pk)

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

            model_instance = form.save(commit=False)
            model_instance.autor = get_perfil_logado(request)
            model_instance.save()

            return redirect('time_line')

        return render(request, 'time_line.html', {'form': form, 'posts': posts,
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