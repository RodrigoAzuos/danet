from rest_framework import serializers, exceptions
from perfis.models import Perfil, Justificativa
from time_line.models import Comentario, Post, Reacao, Tag



class PerfilSerializer(serializers.ModelSerializer):

    class Meta:

        model = Perfil
        fields = ('id','nome', 'data_nascimento', )


class ReacaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Reacao
        fields = ('id', 'tipo',)

class TagSerializer(serializers.ModelSerializer):

    class Meta:

        model = Tag
        fields = ('id', 'descricao',)

class ComentarioSerializerSimples(serializers.ModelSerializer):

    perfil = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Comentario
        fields = ('id','descricao','perfil',)

class PostSerializer(serializers.ModelSerializer):

    reacoes = ReacaoSerializer(many=True, read_only=True)
    autor = PerfilSerializer(read_only=True, many=False)
    criado_em = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    tags = TagSerializer(many=True, read_only=True)
    comentarios = ComentarioSerializerSimples(many=True, read_only=True)

    class Meta:


        model = Post
        fields = ('id','foto','resumo','reacoes','tags','autor','criado_em' ,'like','dislike', 'comentarios',)

class ComentarioSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(read_only=True)
    perfil = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:

        model = Comentario
        fields = ('id','descricao', 'post', 'perfil')

    def create(self, validated_data):

        post_id = self.context.get('post_id')
        perfil_id = self.context.get('perfil_id')
        descricao = validated_data['descricao']

        try:
            post = Post.objects.get(pk=post_id)
            perfil = Perfil.objects.get(pk=perfil_id)
            comentario = Comentario.objects.create(post=post, perfil=perfil, descricao=descricao)
            return comentario

        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='Post não localizado.')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível adicionar o comentário.')


class ReacaoSerializer(serializers.ModelSerializer):

    perfil = PerfilSerializer(many=False, read_only=True)

    class Meta:
        model = Reacao
        fields = ('id', 'tipo', 'post', 'perfil', )

class JustificativaSerializer(serializers.ModelSerializer):

    perfil = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Justificativa
        fields = ('id','descricao','situacao', 'perfil')
        read_only_fields = ('situacao',)

    def create(self, validated_data):

        perfil_id = self.context.get('perfil_id')
        descricao = validated_data['descricao']

        try:

            perfil = Perfil.objects.get(pk=perfil_id)
            justificativa = Justificativa.objects.create(perfil=perfil, descricao=descricao, situacao=False)
            return justificativa

        except perfil.DoesNotExist:
            raise exceptions.NotFound(detail='Perfil não encontrado')
        except:
            raise exceptions.NotAcceptable(detail='Não foi possível criar a justificativa.')