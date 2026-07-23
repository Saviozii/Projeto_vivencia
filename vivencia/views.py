from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import Add_Turma, Add_Aluno
from django.http import HttpResponse
from .function_view import adicionar_turma, adicionar_aluno, bater_ponto, grafico_presenca_hj, aluno_infor
from .models import Aluno

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
    presentes_hj = grafico_presenca_hj() 
    contexto = {
        "presentes_hj" : presentes_hj
    }
    return render(request, 'super_dershboard.html', contexto)


def informaoes_aluno(request,user_id):
    aluno_inf, presencas = aluno_infor(user_id)
    contexto = {
        'aluno_inf' : aluno_inf,
        'presencas' : presencas
    }
    return render(request, 'aluno_inf.html', contexto)

