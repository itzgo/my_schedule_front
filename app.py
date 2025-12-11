import streamlit as st
import requests

from utils.calendar_utils import render_calendar, handle_callback
from components.event_form import show_event_form
from utils.storage import load_events, save_events

# URLs da API
URL_BASE = "https://backend-641903750804.southamerica-east1.run.app"
URL_EVENTOS = "/api/admin/events/public"

st.set_page_config(page_title="Agenda Universitária", layout="centered")
st.title("Agenda Universitária")

# ----------------------------------------------------------
# 1) Função para buscar eventos da API
# ----------------------------------------------------------
def fetch_eventos():
    try:
        resp = requests.get(URL_BASE + URL_EVENTOS)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Erro ao buscar eventos da API: {e}")
        return []

# ----------------------------------------------------------
# 2) Inicialização do session_state
# ----------------------------------------------------------
if "eventos" not in st.session_state:
    st.session_state.eventos = fetch_eventos()

# ----------------------------------------------------------
# 3) Renderiza o calendário (SEM argumentos!)
# ----------------------------------------------------------
callback = render_calendar()

# ----------------------------------------------------------
# 4) Processa clique em datas ou eventos
# ----------------------------------------------------------
handle_callback(callback)

# ----------------------------------------------------------
# 5) Exibe formulário de criar/editar evento
# ----------------------------------------------------------
if st.session_state.get("modo") in ["criar", "editar"]:
    show_event_form()

# ----------------------------------------------------------
# 6) Rodapé
# ----------------------------------------------------------
st.markdown("---")
st.caption(
    f"Total de eventos: {len(st.session_state.eventos)} | "
    "Clique no dia → criar | Clique no evento → editar/excluir"
)
