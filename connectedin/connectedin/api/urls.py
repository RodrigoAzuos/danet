from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ComentarioViewSet, TagViewSet, ReacaoPost, PostViewSet, JustificativaViewSet
from  rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/reacao/<str:tipo_reacao>',
         ReacaoPost.as_view({'get': 'reagir'}), name='reagir-post'),
    path('token/', obtain_auth_token),
    path('posts/<int:post_id>/comentarios/',
        ComentarioViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='comentarios'),
    path('posts/<int:post_id>/comentarios/<int:comentario_id>',
        ComentarioViewSet.as_view({'delete':'destroy'}),
        name='comentarios'),

    path('perfil/justificativa', JustificativaViewSet.as_view({'post':'create',
                                                                'get':'list'})),
    path('perfil/justificativa/<int:justificativa_id>',
         JustificativaViewSet.as_view({'delete': 'destroy',
                                       'put': 'confirmar_justificativa'})),

]