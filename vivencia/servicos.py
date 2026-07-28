from django.utils import timezone
from .models import Presenca
import json

def dados_de_hj():

    hoje = timezone.localdate()

    dados = Presenca.objects.filter(
        dia_ponto = hoje
    ).select_related(
        "aluno",)

    dados_hj = []

    for registro in dados:

        dados_hj.append({
            "aluno": registro.aluno.user.get_full_name() 
                     or registro.aluno.user.username,

            "email": registro.aluno.user.email,

            "turma": registro.aluno.turma.turma,

            "status": registro.get_status_display(),

            "data": str(registro.dia_ponto),

            "entrada": str(registro.hora_entrada)
                       if registro.hora_entrada 
                       else "Não registrado",

            "saida": str(registro.hora_saida)
                     if registro.hora_saida 
                     else "Não registrado",

            "atividade": registro.atividade_diaria
                         or "Não informado",

            "observacao": registro.observacao_presenca
                          or "Não informado",
        })


    return json.dumps(
        dados_hj,
        ensure_ascii=False,
        indent=2
    )
