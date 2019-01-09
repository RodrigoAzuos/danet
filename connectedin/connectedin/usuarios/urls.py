from django.urls import path,include
from django.contrib.auth.views import login, logout_then_login
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from usuarios import views

urlpatterns = [
    ##Usuario##
    path('registrar/', views.RegistrarUsuarioView.as_view() , name = 'registrar'),
    path('registrarsuperusuario/', views.RegistrarSuperUsuarioView.as_view() , name = 'registrar_super_user'),

    path('login/', login, {'template_name': 'login.html'}, name='login'),
    path('logout/', logout_then_login, {'login_url': 'login'},name= 'logout'),

    path('alterar_senha/', views.AlterarSenhaView.as_view(), name= 'alterar_senha'),

    path('', include('django.contrib.auth.urls')),
    path('senha_reset/sucesso/', PasswordResetDoneView.as_view(template_name='email_enviado.html'), name= 'password_reset_done'),
    path('senha_reset/', PasswordResetView.as_view(template_name='resetar_senha_2.html'), name= 'resetar_senha'),
    path('senha_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='redefinir_senha.html'),  name='password_reset_confirm'),
    path('senha_reset/concluído/',PasswordResetCompleteView.as_view(template_name='completo.html'), name='password_reset_complete'),
]
