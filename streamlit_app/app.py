
import streamlit as st
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

# Configuração da página
st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Cadastro de Pacientes")
st.write("Sistema de cadastro e atendimento de pacientes.")

# Inicializar sessão
if "pacientes" not in st.session_state:

    st.session_state.pacientes = pd.DataFrame(
        columns=COLUNAS
    )

# Formulário
with st.form("cadastro", clear_on_submit=True):

    nome = st.text_input("Nome do paciente")

    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        step=1
    )

    convenio = st.selectbox(
        "Convênio",
        [
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Outro"
        ]
    )

    prioridade = st.slider(
        "Prioridade do atendimento (5 = urgente)",
        min_value=1,
        max_value=5,
        value=3
    )

    motivo = st.text_area(
        "Motivo da consulta / observações"
    )

    enviado = st.form_submit_button("Cadastrar")

# Processar cadastro
if enviado:

    if not nome.strip():

        st.error("Informe o nome do paciente.")

    else:

        nova_linha = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": prioridade,
            "motivo": motivo
        }

        novo = pd.DataFrame([nova_linha])

        st.session_state.pacientes = pd.concat(
            [
                st.session_state.pacientes,
                novo
            ],
            ignore_index=True
        )

        # Salvar também no arquivo CSV
        st.session_state.pacientes.to_csv(
            ARQUIVO_CSV,
            index=False,
            encoding="utf-8"
        )

        st.success("Paciente cadastrado com sucesso!")

# Mostrar registros
st.subheader("Últimos pacientes cadastrados")

if not st.session_state.pacientes.empty:

    st.dataframe(
        st.session_state.pacientes.tail(5),
        use_container_width=True
    )

else:

    st.info("Nenhum paciente cadastrado ainda.")

# Gerar arquivo CSV para download
csv = st.session_state.pacientes.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="📥 Baixar CSV",
    data=csv,
    file_name="pacientes.csv",
    mime="text/csv"
)
