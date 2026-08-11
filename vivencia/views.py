from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .function_view import adicionar_turma, adicionar_aluno, bater_ponto, grafico_presenca_hj, aluno_infor
from .models import Aluno, Turmas
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import Add_Turma, Add_Aluno, EmpresaVivenciaForm, LocalizacaoForm

@login_required
def aluno_home(request):
    return render(request, "aluno_home.html")


@login_required
def bate_ponto(request):
    presente, mensagem = bater_ponto(request)

    context = {
        "presente" : presente,
        "mensagem" : mensagem
    }

    return render(request,'bater_ponto.html',context)

from django.db import transaction

def adicionar_empresa(request):
    mensagem = ""

    if request.method == "POST" and request.POST.get("form_type") == "empresa":
        form_empresa = EmpresaVivenciaForm(request.POST)
        form_local = LocalizacaoForm(request.POST)

        if form_empresa.is_valid() and form_local.is_valid():
            with transaction.atomic():
                local = form_local.save()
                empresa = form_empresa.save(commit=False)
                empresa.local_da_empresa = local
                empresa.save()

            mensagem = f'A empresa "{empresa.nome_empresa}" foi adicionada com sucesso!'
            form_empresa = EmpresaVivenciaForm()
            form_local = LocalizacaoForm()
    else:
        form_empresa = EmpresaVivenciaForm()
        form_local = LocalizacaoForm()

    return form_empresa, form_local, mensagem

@login_required
def supervisor_home(request):
    turma_form, mensagem_turma = adicionar_turma(request)
    aluno_form, mensagem_aluno = adicionar_aluno(request)
    empresa_form, local_form, mensagem_empresa = adicionar_empresa(request)

    context = {
        'turma_form': turma_form,
        'aluno_form': aluno_form,
        'empresa_form': empresa_form,
        'local_form': local_form,
        'mensagem_aluno': mensagem_aluno,
        'mensagem_turma': mensagem_turma,
        'mensagem_empresa': mensagem_empresa,
    }

    return render(request, "supervisor_home.html", context)

@login_required
def super_dershboard(request):
    data_str = request.GET.get("data", "")
    if data_str:
        try:
            data = timezone.datetime.strptime(data_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            data = timezone.localdate()
    else:
        data = timezone.localdate()

    presentes_hj, total_aluno = grafico_presenca_hj(data)
    contexto = {
        "presentes_hj" : presentes_hj,
        "total_aluno" : total_aluno,
        "turmas" : Turmas.objects.all(),
        "data_selecionada" : data.isoformat(),
    }
    return render(request, 'super_dershboard.html', contexto)


def informacoes_aluno(request, user_id):
    aluno = get_object_or_404(Aluno, id=user_id)

    context = {
        "aluno": aluno,
        "presencas": aluno.presencas.order_by("-dia_ponto")
    }
    print(aluno.user.username)
    print(aluno.user.first_name)
    print(aluno.turma)
    return render(request, "aluno_inf.html", context)

