
import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"

COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "convenio",
    "prioridade",
    "motivo"
]


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):

    # Validar o nome
    if not nome or not nome.strip():
        return "Erro: informe o nome do paciente.", pd.DataFrame(columns=COLUNAS)

    if idade is None:
        return "Erro: informe a idade do paciente.", pd.DataFrame(columns=COLUNAS)

    # Criar registro
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo
    }

    novo = pd.DataFrame([linha])

    # Salvar no CSV
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(
            ARQUIVO_CSV,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8"
        )
    else:
        novo.to_csv(
            ARQUIVO_CSV,
            index=False,
            encoding="utf-8"
        )

    # Carregar os últimos cinco registros
    tabela = pd.read_csv(ARQUIVO_CSV, encoding="utf-8").tail(5)

    return "Paciente cadastrado com sucesso!", tabela


# Construção da interface
with gr.Blocks() as demo:

    gr.Markdown("# Cadastro de Pacientes")
    gr.Markdown("Sistema de registro de pacientes do consultório médico.")

    nome = gr.Textbox(
        label="Nome do paciente",
        placeholder="Digite o nome completo"
    )

    idade = gr.Number(
        label="Idade",
        minimum=0,
        maximum=120,
        precision=0
    )

    convenio = gr.Dropdown(
        choices=[
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ],
        label="Convênio",
        value="Particular"
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        step=1,
        value=3,
        label="Prioridade do atendimento (5 = urgente)"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        placeholder="Descreva o motivo da consulta...",
        lines=3
    )

    botao = gr.Button("Cadastrar", variant="primary")

    saida_msg = gr.Textbox(
        label="Status",
        interactive=False
    )

    tabela = gr.Dataframe(
        label="Últimos pacientes cadastrados",
        headers=COLUNAS,
        interactive=False
    )

    botao.click(
        fn=cadastrar_paciente,
        inputs=[
            nome,
            idade,
            convenio,
            prioridade,
            motivo
        ],
        outputs=[
            saida_msg,
            tabela
        ]
    )


# Executar aplicação
demo.launch()