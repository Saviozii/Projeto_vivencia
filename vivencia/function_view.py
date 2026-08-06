#function_view.py:
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import Add_Turma, Add_Aluno
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Aluno, Turmas, Presenca, Localizacao
from django.utils import timezone
from .local import calcular_distancia
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .forms import LocalizacaoForm, EmpresaVivenciaForm

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

            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    first_name=form.cleaned_data["nome"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["senha"]
                )

                aluno = Aluno.objects.create(
                    user=user,
                    turma=form.cleaned_data["turma"],
                    empresa=form.cleaned_data["empresa"],
                    foto=form.cleaned_data["foto"]
                )

            mensagem = (
                f"O aluno {aluno.user.first_name} "
                f"da turma {aluno.turma} foi adicionado")

            form = Add_Aluno()
    else:
        form = Add_Aluno()

    return form, mensagem

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


def bater_ponto(request):
    aluno = request.user.aluno
    empresa = aluno.empresa

    if not empresa:
        return None, "Aluno sem empresa cadastrada."

    if request.method != 'POST':
        return None, ''

    local = empresa.local_da_empresa
    if not local:
        return None, "Empresa sem local cadastrado."

    latitude_aluno = request.POST.get("latitude")
    longitude_aluno = request.POST.get("longitude")

    try:
        latitude_aluno = Decimal(latitude_aluno)
        longitude_aluno = Decimal(longitude_aluno)
    except (TypeError, InvalidOperation):
        return None, "Localização inválida. Ative o GPS e tente novamente."

    distancia = calcular_distancia(
        local.latitude,
        local.longitude,
        latitude_aluno,
        longitude_aluno,
    )

    if distancia > local.raio_permitido:
        return None, f"Você está fora da área permitida ({round(distancia, 2)}m)."

    dia_hj = timezone.localdate()
    hora_agr = timezone.localtime().time()

    presente = Presenca.objects.filter(
        aluno=aluno,
        dia_ponto=dia_hj,
    ).first()

    if presente is None:
        presente = Presenca.objects.create(
            aluno=aluno,
            dia_ponto=dia_hj,
            status='P',
            hora_entrada=hora_agr,
            latitude_registrada=latitude_aluno,
            longitude_registrada=longitude_aluno,
        )
        mensagem = "Entrada registrada com sucesso!"
        print(f"O {aluno} entrou às {hora_agr} horas.")

    elif presente.hora_saida is None:
        atividade = request.POST.get('atividade_diaria', '')
        presente.hora_saida = hora_agr
        presente.atividade_diaria = atividade
        presente.latitude_registrada = latitude_aluno
        presente.longitude_registrada = longitude_aluno
        presente.save()
        mensagem = "Saída registrada com sucesso!"
        print(f"""
        O {aluno} fez:
        {atividade}
        """)

    else:
        mensagem = "Você já registrou entrada e saída hoje."

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

