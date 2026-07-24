from django.contrib import admin
from django.urls import path
from login_contas.views import login_view
from vivencia.views import supervisor_home, aluno_home, bate_ponto, super_dershboard, informacoes_aluno

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('supervisor_home/',supervisor_home, name = 'supervisor_home'),
    path('aluno_home/',aluno_home, name = 'aluno_home'),
    path('aluno_home/bater_ponto',bate_ponto, name = 'bater_ponto'),
    path('super_dershboard', super_dershboard, name = 'super_dershboard'),
    path("informacoes_aluno/<int:user_id>/",informacoes_aluno,name="informacoes_aluno"),
]

