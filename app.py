import streamlit as st
from utils.calendar_utils import render_calendar, handle_callback
from components.event_form import show_event_form
from utils.storage import load_events, save_events

st.set_page_config(page_title="Agenda Universitária", layout="wide")
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

# CSS
st.markdown(
    """
    <style>
    /* Fundo e bordas do calendário */
    .fc {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Cabeçalho bonito */
    .fc-toolbar-title {
        color: #2c3e50;
        font-weight: bold;
        font-size: 1.5rem;
    }

    /* Dias da semana */
    .fc-col-header-cell-cushion {
        color: #34495e;
        font-weight: 600;
    }

    /* Eventos mais modernos */
    .fc-event {
        border-radius: 8px;
        padding: 4px 8px;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    .fc-event:hover {
        transform: scale(1.02);
    }

    /* Botão today destacado */
    .fc-today-button {
        background-color: #3498db !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
    }

    /* Dias vazios mais claros */
    .fc-daygrid-day-number {
        color: #95a5a6;
    }
    </style>
    """,
    unsafe_allow_html=True
)