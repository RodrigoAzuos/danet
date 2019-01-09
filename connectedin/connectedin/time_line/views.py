from django.shortcuts import render, redirect
from django.views.generic.base import View
# Create your views here.
from perfis.models import Perfil
from perfis.views import get_perfil_logado
from time_line.forms import PostModelForm
from time_line.models import Post


class TimeLinePost(View):

    def get(self, request):

        form = PostModelForm()
        logado = get_perfil_logado(request)
        perfis = Perfil.objects.all()
        filtro = None
        resultados = None

        posts = Post.objects.all().filter(autor__contatos=logado).order_by('-criado_em') |\
                Post.objects.all().filter(autor=logado).order_by('-criado_em')

        if 'q' in request.GET:
            filtro = request.GET['q']

        if filtro:
            resultados = perfis.filter(usuario__username__icontains=filtro)


            for perfil in resultados:

                if perfil in get_perfil_logado(request).bloqueados.all():
                    resultados = resultados.exclude(pk=perfil.pk)


                if get_perfil_logado(request) in perfil.bloqueados.all():
                   resultados = resultados.exclude(pk=perfil.pk)

            # print(resultados)


        return render(request, 'time_line.html', {'post_form':form, 'posts':posts,
                                                  'logado': logado, 'resultados': resultados})

    def post(self, request):

        form = PostModelForm(request.POST, request.FILES)

        if form.is_valid():

            model_instance = form.save(commit=False)
            model_instance.autor = get_perfil_logado(request)
            model_instance.save()

            return redirect('time_line')

        return render(request, "time_line.html", {'form': form})


def apagar_postagem(request, post_id):

    autor = get_perfil_logado(request)
    super_user = autor.usuario.is_superuser
    post = Post.objects.get(pk=post_id)
    post.apagar(super_user,autor)

    return redirect('time_line')