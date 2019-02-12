from django.urls import path
from time_line import views
urlpatterns = [

    path('timeline', views.TimeLinePost.as_view(), name='time_line'),
    path('post/<int:post_id>/deletar', views.apagar_postagem, name='deletar_post'),
    path('timeline/tag/<int:tag_id>', views.BuscarPostTag.as_view(), name='busca_tag'),
    path('timeline/busca/', views.PesquisaPostTag.as_view(), name='busca_tag_form'),
    path('post/<int:pk>/reacao/<str:reacao>', views.reagir, name = 'reagir_web'),
    path('post/<int:post_id>/comentar', views.comentar, name = 'comentar'),
    path('post/<int:post_id>/comentario/<int:pk>/delete', views.deletar_comentario, name = 'delete_comentario'),

]