from django import forms
from vivencia.models import Aluno, Turmas
from .models import EmpresaVivencia, Localizacao


class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields = ['nome_do_local', 'latitude', 'longitude', 'raio_permitido']
        widgets = {
            'nome_do_local': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'raio_permitido': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EmpresaVivenciaForm(forms.ModelForm):
    class Meta:
        model = EmpresaVivencia
        fields = [
            'nome_empresa',
            'responsavel_da_empresa',
            'numero_responsavel',
            'email_responsavel',
            'endereco',
        ]
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel_da_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'email_responsavel': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Add_Turma(forms.ModelForm):
    class Meta:
        model = Turmas
        fields = ["turma"]

class Add_Aluno(forms.Form):
    foto = forms.ImageField()
    username = forms.CharField(max_length=200)
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)

    empresa = forms.ModelChoiceField(
    queryset=EmpresaVivencia.objects.all())

    turma = forms.ModelChoiceField(
        queryset=Turmas.objects.all()
    )
