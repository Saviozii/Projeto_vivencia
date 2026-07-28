from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import Add_Turma, Add_Aluno
from django.http import HttpResponse
from .function_view import adicionar_turma, adicionar_aluno, bater_ponto, grafico_presenca_hj, aluno_infor
from .models import Aluno
from django.shortcuts import render, get_object_or_404

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


@login_required
def supervisor_home(request):
    turma_form, mensagem_turma = adicionar_turma(request)
    aluno_form, mensagem_aluno = adicionar_aluno(request)

    context = {
        'turma_form' : turma_form,
        'aluno_form' : aluno_form,
        'mensagem_aluno' : mensagem_aluno,
        'mensagem_turma' : mensagem_turma,
    }

    return render(request,"supervisor_home.html",context)

@login_required
def super_dershboard(request):
    presentes_hj, total_aluno = grafico_presenca_hj() 
    contexto = {
        "presentes_hj" : presentes_hj,
        "total_aluno" : total_aluno
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

