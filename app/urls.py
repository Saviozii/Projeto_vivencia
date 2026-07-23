"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login_contas.views import login_view
from vivencia.views import supervisor_home, aluno_home, bate_ponto, super_dershboard, informaoes_aluno

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('supervisor_home/',supervisor_home, name = 'supervisor_home'),
    path('aluno_home/',aluno_home, name = 'aluno_home'),
    path('aluno_home/bater_ponto',bate_ponto, name = 'bater_ponto'),
    path('super_dershboard', super_dershboard, name = 'super_dershboard'),
    path("informacoes_aluno/<int:user_id>/",informaoes_aluno,name="informacoes_aluno")
]

