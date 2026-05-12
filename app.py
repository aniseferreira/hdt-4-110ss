
import streamlit as st
import json
import random
import pandas as pd
from datetime import datetime
import os
import io

st.set_page_config(
    page_title="Matching — Heródoto",
    layout="wide"
)

# =========================
# Carregar dados
# =========================

with open("data/herodoto_sauromatas.json", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# Embaralhamento
# =========================

if "greek_order" not in st.session_state:
    st.session_state.greek_order = random.sample(data, len(data))

if "portuguese_order" not in st.session_state:
    st.session_state.portuguese_order = random.sample(data, len(data))

greek = st.session_state.greek_order
portuguese = st.session_state.portuguese_order

# =========================
# Interface
# =========================

st.title("Heródoto — Exercício de Matching")
st.subheader("Identificação")

name = st.text_input("Nome")
email = st.text_input("Email")

st.markdown(
    """
Associe cada oração em grego antigo à sua tradução em português.
"""
)

left, right = st.columns(2)

# =========================
# Lista de traduções
# =========================

translation_options = {}

with right:
    st.subheader("Traduções")

    for idx, p in enumerate(portuguese, start=1):
        translation_options[f"{idx}. {p['portuguese']}"] = p["id"]
        st.markdown(f"**{idx}.** {p['portuguese']}")

# =========================
# Seleção
# =========================

answers = {}

with left:
    st.subheader("Orações Gregas")

    for letter_idx, g in enumerate(greek):
        letter = chr(65 + letter_idx)

        choice = st.selectbox(
            f"{letter}. {g['greek']}",
            options=list(translation_options.keys()),
            key=f"select_{g['id']}"
        )

        answers[g["id"]] = translation_options[choice]

# =========================
# Correção
# =========================

corrigir = st.button("Corrigir")

if corrigir:

    if not name or not email:
        st.warning("Preencha nome e email.")
        st.stop()

    st.divider()

    score = 0

    for letter_idx, g in enumerate(greek):

        correct = g["id"]
        chosen = answers[g["id"]]

        letter = chr(65 + letter_idx)

        if correct == chosen:
            score += 1
            st.success(f"{letter} — Correto")

        else:

            correct_text = next(
                x["portuguese"]
                for x in data
                if x["id"] == correct
            )

            chosen_text = next(
                x["portuguese"]
                for x in data
                if x["id"] == chosen
            )

            st.error(
                f"""
{letter} — Incorreto

Sua resposta:
{chosen_text}

Resposta correta:
{correct_text}
"""
            )

    st.subheader(f"Pontuação: {score}/{len(data)}")

    st.write(f"Aluno(a): {name}")
    st.write(f"Email: {email}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = {
        "nome": name,
        "email": email,
        "score": score,
        "total": len(data),
        "data": timestamp
    }

    df = pd.DataFrame([result])

    st.session_state.df_resultado = df
    
    st.success("Resultado gerado com sucesso.")
        
if "df_resultado" in st.session_state:

    csv_buffer = io.StringIO()

    st.session_state.df_resultado.to_csv(
        csv_buffer,
        index=False
    )

    st.download_button(
        label="Baixar resultado CSV",
        data=csv_buffer.getvalue(),
        file_name="resultado.csv",
        mime="text/csv"
    )
# =========================
# Reiniciar
# =========================

if st.button("Embaralhar novamente"):
    st.session_state.greek_order = random.sample(data, len(data))
    st.session_state.portuguese_order = random.sample(data, len(data))
    st.rerun()
