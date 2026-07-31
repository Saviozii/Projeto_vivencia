from django.utils import timezone
from ..models import Presenca
import json

def dados_de_hj():

    hoje = timezone.localdate()

    dados = Presenca.objects.filter(
        dia_ponto = hoje
    ).select_related(
        "aluno",)

    dados_hj = []

    for i in dados:

        dados_hj.append({
            "aluno": i.aluno.user.get_full_name() 
                     or i.aluno.user.username,

            "email": i.aluno.user.email,

            "turma": i.aluno.turma.turma,

            "status": i.get_status_display(),

            "data": str(i.dia_ponto),

            "entrada": str(i.hora_entrada)
                       if i.hora_entrada 
                       else "Não registrado",

            "saida": str(i.hora_saida)
                     if i.hora_saida 
                     else "Não registrado",

            "atividade": i.atividade_diaria
                         or "Não informado",

            "observacao": i.observacao_presenca
                          or "Não informado",
        })


    return json.dumps(
        dados_hj,
        ensure_ascii=False,
        indent=2
    )

