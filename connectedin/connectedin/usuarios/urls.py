from django.urls import path,include
from django.contrib.auth.views import login, logout_then_login
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from usuarios import views

urlpatterns = [
    ##Usuario##
    path('registrar/', views.RegistrarUsuarioView.as_view() , name = 'registrar'),
    path('registrar_superusuario/', views.RegistrarSuperUsuarioView.as_view() , name = 'registrar_super_user'),
    path('perfil/<int:perfil_id>/tornar_superuser', views.tornar_superuser , name = 'tornar_superuser'),
    path('login/', views.login, name='login'),
    path('logout/', logout_then_login, {'login_url': 'login'},name= 'logout'),

    path('alterar-senha/', views.AlterarSenhaView.as_view(), name= 'alterar_senha'),
    path('alterar-foto/', views.alterar_foto, name= 'alterar_foto'),

    path('', include('django.contrib.auth.urls')),
    path('senha-reset/sucesso/', PasswordResetDoneView.as_view(template_name='email_enviado.html'), name= 'password_reset_done'),
    path('senha-reset/', PasswordResetView.as_view(template_name='resetar_senha_2.html'), name= 'resetar_senha'),
    path('senha-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='redefinir_senha.html'),  name='password_reset_confirm'),
    path('senha-reset/concluído/',PasswordResetCompleteView.as_view(template_name='completo.html'), name='password_reset_complete'),
]
