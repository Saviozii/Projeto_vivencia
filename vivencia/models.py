from django.db import models
from django.contrib.auth.models import User

class Turmas(models.Model):
    turma = models.CharField(max_length=100)

    def __str__(self):
        return self.turma

class Localizacao(models.Model):
    nome_do_local = models.CharField(max_length=100)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    raio_permitido = models.PositiveIntegerField(
        default=250,
        help_text="Raio em metros"
    )
    def __str__(self):
        return self.nome_do_local

    
class EmpresaVivencia(models.Model):

    responsavel_da_empresa = models.CharField(max_length=100)
    numero_responsavel = models.CharField(max_length=20)
    email_responsavel = models.EmailField()

    nome_empresa = models.CharField(max_length=100)

    local_da_empresa = models.OneToOneField(Localizacao,on_delete=models.CASCADE)

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    def __str__(self):
        return self.nome_empresa

class Turnos(models.Model):
    turno = models.CharField(max_length=10)

    def __str__(self):
        return self.turno

class Aluno(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="aluno")

    foto = models.ImageField(upload_to='fotos_alunos/',blank=True, null=True)

    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE, related_name="alunos")

    turno = models.ForeignKey(Turnos,on_delete=models.SET_NULL,null=True)

    empresa = models.ForeignKey(EmpresaVivencia,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.first_name

class Presenca(models.Model):
    
    STATUS = (
        ("P", "Presente"),
        ("F", "Falta"),)

    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE,related_name= "presencas",)

    latitude_registrada = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitude_registrada = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    
    status = models.CharField(max_length=1,choices=STATUS,default="F") 
    
    dia_ponto= models.DateField(db_index=True)

    hora_entrada= models.TimeField(null=True, blank=True)
    hora_saida= models.TimeField(null=True, blank=True)

    observacao_presenca= models.TextField(null=True,blank=True)
    atividade_diaria= models.TextField(null=True,blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["aluno", "dia_ponto"],
                name="unique_presenca_por_dia"
            )
        ]


class Relatorios(models.Model):

    relatorio_diario = models.TextField(null=True,blank=True)
    data = models.DateField(auto_now_add=True,null=True)