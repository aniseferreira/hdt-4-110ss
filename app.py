# app.py

import streamlit as st
import json
import random

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

if st.button("Corrigir"):

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

# =========================
# Reiniciar
# =========================

if st.button("Embaralhar novamente"):
    st.session_state.greek_order = random.sample(data, len(data))
    st.session_state.portuguese_order = random.sample(data, len(data))
    st.rerun()
