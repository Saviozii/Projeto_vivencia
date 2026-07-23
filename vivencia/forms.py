from django import forms
from vivencia.models import Aluno, Turmas

class Add_Turma(forms.ModelForm):
    class Meta:
        model = Turmas
        fields = ["turma"]

class Add_Aluno(forms.Form):
    username = forms.CharField(max_length=200)
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)

    turma = forms.ModelChoiceField(
        queryset=Turmas.objects.all()
    )