from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions, authentication
from api.serializers import ComentarioSerializer, TagSerializer, PostSerializer, JustificativaSerializer
from rest_framework.response import Response
from time_line.models import Comentario, Tag, Post, Reacao
from perfis.models import Perfil, Justificativa

from perfis.views import get_perfil_logado
from django.db.models import Q


class DefaultMixin(object):

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
       permissions.IsAuthenticated,
    )

class ComentarioViewSet(DefaultMixin, viewsets.ModelViewSet):

    serializer_class = ComentarioSerializer
    queryset = Comentario.objects.all()
    permission_classes = (permissions.IsAuthenticated),

    def create(self, request, post_id, *args, **kwargs):

        perfil = request.user.perfil
        serializer = ComentarioSerializer(data=request.data,
                                          context= {'post_id':post_id, 'perfil_id': perfil.id})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, post_id, *args, **kwargs):
        queryset = self.filter_queryset(Comentario.objects.filter(post__pk=post_id))

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, post_id, comentario_id, *args, **kwargs):

        comentario = Comentario.objects.get(pk=comentario_id)
        serializer = ComentarioSerializer(comentario)
        comentario.delete()

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class TagViewSet(DefaultMixin, viewsets.ModelViewSet):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class PostViewSet(DefaultMixin, viewsets.ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):

        logado = get_perfil_logado(request)

        queryset = Post.objects.all().order_by('-criado_em')

        if not logado.usuario.is_superuser:
            queryset = Post.objects.filter(Q(autor__contatos=logado) or Q(autor=logado)).order_by('-criado_em')

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class JustificativaViewSet(DefaultMixin, viewsets.ModelViewSet):

    serializer_class = JustificativaSerializer
    queryset = Justificativa.objects.all()

    def create(self, request, *args, **kwargs):

        perfil = request.user.perfil
        serializer = JustificativaSerializer(data=request.data,context={'perfil_id': perfil.id})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):

        perfil = request.user.perfil
        queryset = self.filter_queryset(Justificativa.objects.filter(perfil__pk=perfil.id))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, justificativa_id, *args, **kwargs):
        justificativa = Justificativa.objects.get(pk=justificativa_id)
        justificativa.invalidar()
        serializer = JustificativaSerializer(justificativa)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def confirmar_justificativa(self, request,justificativa_id):

        perfil = request.user.perfil
        justificativa = Justificativa.objects.get(pk=justificativa_id)
        justificativa.confirmar()

        serializer = JustificativaSerializer(justificativa)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class ReacaoPost(DefaultMixin,viewsets.ViewSet):

    def reagir(self, request, post_id,tipo_reacao):

        if tipo_reacao == "like" or tipo_reacao == 'dislike':

            perfil = request.user.perfil
            post = Post.objects.get(pk=post_id)
            reacao = post.reacoes.all().filter(perfil=perfil.pk)

            if reacao:
                reacao = reacao[0]

                if tipo_reacao == reacao.tipo:
                    reacao.delete()

                    quantidade = post.reacoes.all().count()

                    return Response(status=status.HTTP_204_NO_CONTENT, data={
                        "postagem": {
                            "id": reacao.post.pk
                        },
                        "reacao": {
                            "tipo": reacao.tipo,
                            "perfil": reacao.perfil.pk
                        },
                        "quantidade": quantidade
                    })

                else:

                    reacao.tipo = tipo_reacao
                    reacao.save()

            else:

                reacao = Reacao(tipo=tipo_reacao,perfil=perfil, post=post)
                reacao.save()

            quantidade = post.reacoes.all().count()

            return Response(status=status.HTTP_200_OK, data={
                "postagem": {
                    "id": reacao.post.pk
                },
                "reacao":{
                    "tipo": reacao.tipo,
                    "perfil": reacao.perfil.pk
                },
                "quantidade": quantidade
            })

        else:

            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'mensage': 'reações permitidas: like ou dislike'
            })





