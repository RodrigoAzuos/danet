from django.urls import path
from time_line import views
urlpatterns = [

    path('timeline', views.TimeLinePost.as_view(), name='time_line'),
    path('post/<int:post_id>/deletar', views.apagar_postagem, name='deletar_post'),

]