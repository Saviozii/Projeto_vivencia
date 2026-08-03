#Atividades pro celery
from celery import shared_task
from django.utils import timezone

from .models import Aluno, Presenca


@shared_task
def registrar_faltas_do_dia():
    dia = timezone.localdate()
    criadas = 0

    for aluno in Aluno.objects.all():
        _, criado = Presenca.objects.get_or_create(
            aluno=aluno,
            dia_ponto=dia,
            defaults={"status": "F"},
        )
        if criado:
            criadas += 1

    return f"{criadas} faltas registradas em {dia}"
