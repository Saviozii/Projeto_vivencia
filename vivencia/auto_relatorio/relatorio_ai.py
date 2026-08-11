import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
import json
from langchain_core.prompts import ChatPromptTemplate
from .servicos import dados_de_hj
from vivencia.models import relatorios

load_dotenv()

prompt_template = ChatPromptTemplate.from_template("""
Você é responsável por gerar um relatório diário da vivência.

Analise os dados abaixo.

Escreva um relatório contendo:

- resumo do dia;
- quantidade de presentes e faltas;
- principais atividades;
- observações importantes.

Dados:

{dados}
"""
)


model = GoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    google_api_key = os.getenv("GEMINI_API_KEY"),
)

dados = dados_de_hj()

def relatorio(dados):
    prompt = prompt_template.format(dados = dados)
    resposta = model.invoke(prompt)
    return resposta

relatorio_diario_ai = relatorio(dados)

def enviar_ao_banco(i):
    enviar = relatorios.objects.create(
        relatorio_diario = i
    )
    enviar.save()
    return 

enviar_ao_banco(relatorio_diario_ai)    

def funcao_relatorio():
    dados = dados_de_hj()
    relatorio_diario_ai = relatorio(dados)
    print("CHEGUEI AQUI 2")
    print(relatorio_diario_ai)
    enviar_ao_banco(relatorio_diario_ai)
    print("Dados foi enviado ao banco com sucesso.")

    
