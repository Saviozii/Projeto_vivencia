from django.db import models
from django.contrib.auth.models import User

class Turmas(models.Model):
    turma = models.CharField(max_length=100)

    def __str__(self):
        return self.turma


class Aluno(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="aluno")

    foto = models.ImageField(upload_to='fotos_alunos/',blank=True, null=True)
    
    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE, related_name="alunos")

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Presenca(models.Model):
    
    STATUS = (
        ("P", "Presente"),
        ("F", "Falta"),)

    aluno = models.ForeignKey(Aluno,on_delete=models.CASCADE,related_name= "presencas",)
    
    status = models.CharField(max_length=1,choices=STATUS,null=True,blank=True) 
    
    dia_ponto= models.DateField()

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