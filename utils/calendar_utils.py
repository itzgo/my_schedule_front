from streamlit_calendar import calendar
import streamlit as st
import uuid

CORES = {
    "Aula": "#e74c3c",
    "Evento": "#3498db",
    "Evento Universitário": "#2ecc71"
}

OPTIONS = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth",
    "selectable": False,
    "locale": "pt-br",
    "height": 850,
    "contentHeight": 800,
    "aspectRatio": 2.0,
    "expandRows": True,
    "dayMaxEvents": True,
    "eventMinWidth": 100,
    "eventShortHeight": 30,
    # Melhorias estéticas
    "eventBorderColor": "transparent",  # Remove bordas duras
    "eventBackgroundColor": "#ffffff",  # Fundo branco para eventos (ou customize por cor)
    "eventTextColor": "#333333",        # Texto escuro para legibilidade
    "eventDisplay": "block",            # Eventos em bloco bonito
    "moreLinkText": "+ mais",           # Texto em português para "+X mais"
    "editable": False,                  # Desativa drag/drop (opcional)
    "themeSystem": "standard",          # Tema padrão mais clean
    "views": {
        "dayGridMonth": {
            "dayHeaderFormat": { "weekday": "short", "day": "numeric" },  # Cabeçalho curto e bonito
            "weekNumbers": False
        }
    }
}

pOPTIONS = {
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "initialView": "dayGridMonth",
    "selectable": False,
    "locale": "pt-br",
    "height": 800,              # ← Calendário bem maior
    "contentHeight": 750,       # ← Mais espaço interno
    "aspectRatio": 1.8,         # ← Proporção perfeita
    "expandRows": True,         # ← Linhas se expandem
    "dayMaxEvents": True,       # ← Mostra "+X mais" se necessário
    "eventMinWidth": 100,
    "eventShortHeight": 30,
}

def to_calendar_events():
    eventos_cal = []
    for ev in st.session_state.eventos:
        # Garante ID válido
        if "id" not in ev or not ev["id"]:
            ev["id"] = str(uuid.uuid4())
        eventos_cal.append({
            "id": ev["id"],
            "title": f"{ev['titulo']} ({ev['hora_inicio']}–{ev['hora_fim']})",
            "start": f"{ev['data']}T{ev['hora_inicio']}:00",
            "end": f"{ev['data']}T{ev['hora_fim']}:00",
            "backgroundColor": ev.get("cor", "#95a5a6"),
            "textColor": "white",
        })
    return eventos_cal

def render_calendar():
    return calendar(events=to_calendar_events(), options=OPTIONS, key="calendario")

def handle_callback(callback):
    if not callback:
        return

    data_clicada = None
    evento_id_clicado = None

    if callback.get("callback") == "dateClick":
        info = callback.get("dateClick", {})
        date_str = info.get("dateStr") or (info.get("date") or "").split("T")[0]
        if date_str:
            data_clicada = date_str

    elif callback.get("callback") == "eventClick":
        event = callback["eventClick"]["event"]
        evento_id_clicado = event["id"]
        start = event.get("start", "")
        if start:
            data_clicada = start.split("T")[0]

    if data_clicada:
        if evento_id_clicado:
            st.session_state.modo = "editar"
            st.session_state.evento_id_selecionado = evento_id_clicado
        else:
            st.session_state.modo = "criar"
            st.session_state.data_temp = data_clicada