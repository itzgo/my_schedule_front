import streamlit as st
from utils.calendar_utils import render_calendar, handle_callback
from components.event_form import show_event_form
from utils.storage import load_events, save_events

st.set_page_config(page_title="Agenda Universitária", layout="centered")
st.title("Agenda Universitária")

# Inicialização
if "eventos" not in st.session_state:
    st.session_state.eventos = load_events()

# Renderiza o calendário e captura cliques
callback = render_calendar()

# Processa cliques (criar ou editar)
handle_callback(callback)

# Mostra formulário se estiver em modo criar/editar
if st.session_state.get("modo") in ["criar", "editar"]:
    show_event_form()

# Rodapé
st.markdown("---")
st.caption(f"Total de eventos: {len(st.session_state.eventos)} | "
           "Clique no dia → criar | Clique no evento → editar/excluir")