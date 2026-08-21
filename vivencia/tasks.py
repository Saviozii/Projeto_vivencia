from django.utils import timezone
from .models import Aluno, Presenca
from celery import shared_task


@shared_task
def registrar_faltas_do_dia():
    dia = timezone.localdate()
    falta = 0

    for aluno in Aluno.objects.all():
        _, i = Presenca.objects.get_or_create(
            aluno=aluno,
            dia_ponto=dia,
            defaults={"status": "F"},
        )
        if i:
            falta += 1

    return f"{falta} faltas registradas em {dia}"


def registra_o_cara_faltou():
    ...