import streamlit as st
from datetime import datetime, time
from streamlit_calendar import calendar
import json
import os

st.set_page_config(page_title="Agenda Universitária", layout="centered")
st.title("Agenda Universitária")

DATA_FILE = "eventos.json"

# --- Persistência ---
def load_events():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_events():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.eventos, f, ensure_ascii=False, indent=4)

if "eventos" not in st.session_state:
    st.session_state.eventos = load_events()
if "modo" not in st.session_state:
    st.session_state.modo = None
if "data_selecionada" not in st.session_state:
    st.session_state.data_selecionada = None

# --- Converter eventos ---
def to_calendar_events():
    cores = ["#e74c3c", "#2ecc71", "#3498db", "#9b59b6", "#f1c40f"]
    return [
        {
            "title": f"{e['titulo']} ({e['hora_inicio']}–{e['hora_fim']})",
            "start": f"{e['data']}T{e['hora_inicio']}:00",
            "end": f"{e['data']}T{e['hora_fim']}:00",
            "backgroundColor": cores[i % len(cores)],
            "textColor": "white",
        }
        for i, e in enumerate(st.session_state.eventos)
    ]

# --- Configuração do calendário ---
options = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth",
    "selectable": False,        # ← fundamental para dateClick funcionar
    "locale": "pt-br",
    "height": "auto",
}

events = to_calendar_events()
callback = calendar(events=events, options=options, key="calendario_unico")

# ======================= DETECÇÃO DO CLIQUE (versão 1.4.0 CORRIGIDA) =======================
data_clicada = None

if callback:
    # Formato da versão 1.4.0 - usa .get() para segurança
    if callback.get("callback") == "dateClick":
        date_click_info = callback.get("dateClick", {})
        # Usa 'dateStr' se existir, senão usa 'date' e extrai
        data_clicada = date_click_info.get("dateStr") or date_click_info.get("date", "").split("T")[0]

    elif callback.get("callback") == "eventClick":
        event_info = callback.get("eventClick", {}).get("event", {})
        start = event_info.get("start", "")
        data_clicada = start.split("T")[0]

# Atualiza o estado SEM rerun imediato → formulário aparece na hora
if data_clicada:
    st.session_state.data_selecionada = data_clicada
    st.session_state.modo = "criar"

# ======================= FORMULÁRIO DE CRIAÇÃO =======================
if st.session_state.modo == "criar" and st.session_state.data_selecionada:
    data = st.session_state.data_selecionada
    data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

    st.subheader(f"Novo evento – {data_br}")

    with st.form("form_novo"):
        titulo = st.text_input("Título *", placeholder="Ex: Prova de Cálculo III")
        col1, col2 = st.columns(2)
        inicio = col1.time_input("Início *", value=time(8, 0))
        fim = col2.time_input("Fim *", value=time(10, 0))
        local = st.text_input("Local (opcional)")

        c1, c2 = st.columns(2)
        salvar = c1.form_submit_button("Salvar", type="primary")
        cancelar = c2.form_submit_button("Cancelar")

        if cancelar:
            st.session_state.modo = None
            st.session_state.data_selecionada = None
            st.rerun()

        if salvar:
            if not titulo.strip():
                st.error("Preencha o título!")
            elif inicio >= fim:
                st.error("Horário inválido!")
            else:
                novo = {
                    "titulo": titulo.strip(),
                    "data": data,
                    "hora_inicio": inicio.strftime("%H:%M"),
                    "hora_fim": fim.strftime("%H:%M"),
                    "local": local.strip()
                }
                st.session_state.eventos.append(novo)
                save_events()
                st.success("Evento criado!")
                st.session_state.modo = None
                st.rerun()

# ======================= RODAPÉ =======================
st.caption(f"Total de eventos: {len(st.session_state.eventos)}")

if st.button("Apagar todos os eventos"):
    if st.checkbox("Tem certeza?"):
        st.session_state.eventos = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()