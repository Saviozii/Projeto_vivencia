from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from login_contas.views import login_view
from vivencia.views import supervisor_home, aluno_home, bate_ponto, super_dershboard, informacoes_aluno
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.static import serve


urlpatterns = [
    path('', lambda r: HttpResponseRedirect('login/')),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('supervisor_home/',supervisor_home, name = 'supervisor_home'),
    path('aluno_home/',aluno_home, name = 'aluno_home'),
    path('aluno_home/bater_ponto',bate_ponto, name = 'bater_ponto'),
    path('super_dershboard', super_dershboard, name = 'super_dershboard'),
    path("informacoes_aluno/<int:aluno_id>/",informacoes_aluno,name="informacoes_aluno"),
]

# Serve arquivos de mídia (fotos) também em produção, apenas para usuários logados
urlpatterns += [
    path('media/<path:path>', login_required(serve), {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)