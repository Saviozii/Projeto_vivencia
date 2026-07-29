#function_view.py:
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import Add_Turma, Add_Aluno
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Aluno, Turmas, Presenca
from django.utils import timezone

def adicionar_turma(request):
    mensagem = ''

    if request.method == "POST" and request.POST.get("form_type") == "turma":
        form = Add_Turma(request.POST or None)
        
        if form.is_valid():
            turma = form.save()
            mensagem = f'A turma "{turma.turma}" foi adicionada com sucesso!'
            
            form = Add_Turma()

    else:
        form = Add_Turma()

    return form, mensagem


def adicionar_aluno(request):
    mensagem = ""

    if request.method == "POST" and request.POST.get("form_type") == "aluno":
        form = Add_Aluno(request.POST, request.FILES)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["nome"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["senha"]
            )

            aluno = Aluno.objects.create(
                user=user,
                turma=form.cleaned_data["turma"],
                foto=form.cleaned_data["foto"]
            )

            mensagem = (
                f"O aluno {aluno.user.first_name} "
                f"da turma {aluno.turma} foi adicionado")

            form = Add_Aluno()
    else:
        form = Add_Aluno()

    return form, mensagem


def bater_ponto(request):
    aluno = request.user.aluno
    mensagem = ''
    presente = None

    if request.method == 'POST':
        dia_hj = timezone.localdate()
        hora_agr = timezone.localtime().time()

        presente = Presenca.objects.filter(
            aluno = aluno,
            dia_ponto = dia_hj,
        ).first()
        mensagem = f"Entrada registrada com sucesso!"

        if presente is None:
            presente = Presenca.objects.create(
                aluno = aluno,
                dia_ponto = dia_hj,
                status = 'P',
                hora_entrada = hora_agr
            )
            print(f"O {aluno} entrou as {hora_agr} Horas.")
        
        elif presente.hora_saida is None:
            atividade = request.POST.get('atividade_diaria','')
            presente.hora_saida = hora_agr
            presente.atividade_diaria = atividade
            presente.save()
            print(f"""
            O {aluno} fez:
            {atividade}
            """)
            mensagem = f"Saíada registrada com sucesso!"

    return presente, mensagem


#Consulta 
def grafico_presenca_hj(data=None):
    dia = data if data else timezone.localdate()
    presente_hj = Presenca.objects.all().filter(dia_ponto=dia)
    total_aluno = Aluno.objects.all()
    return presente_hj, total_aluno

def aluno_infor(user_id):
    aluno_inf = get_object_or_404(Aluno, id = user_id)
    presencas = aluno_inf.presencas.order_by("-dia_ponto")
    contexto = {
        'aluno_inf' : aluno_inf,
        'presencas' : presencas
    }
    return contexto

