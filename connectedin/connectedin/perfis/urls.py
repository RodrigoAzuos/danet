from django.urls import path
from django.contrib.auth.views import login, logout_then_login

from perfis import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('perfil/<int:perfil_id>', views.exibir_perfil, name='exibir'),
    path('perfil/<int:perfil_id>/desfazer-amizade', views.desfazer_amizade, name='desfazer_amizade'),
    path('desativar-conta', views.desativar_conta, name='desativar_conta'),
    path('confirmar-desativacao/<int:justificativa_id>', views.confirmar_justificativa, name='confirmar_desativacao'),
    path('apagar-justificativa/<int:justificativa_id>', views.apagar_justificativa, name='apagar_desativacao'),
    path('perfil/ativar/<int:justificativa_id>', views.ativar, name='ativar'),
    path('ativar-conta', views.ativar_conta, name='ativar_conta'),

    path('convidar/<int:perfil_id>', views.convidar, name='convidar'),
    path('aceitar/<int:convite_id>', views.aceitar, name='aceitar'),
    path('recusar/<int:convite_id>', views.apagar, name='recusar'),
    path('apagarsolicitacao/<int:convite_id>', views.apagar, name='apagar_solicitacao'),
    path('perfil/<int:perfil_id>/bloquear', views.bloquear_contato, name='bloquear_contato'),
    path('perfil/<int:perfil_id>/desbloquear', views.desbloquear_contato, name='desbloquear_contato'),
]


