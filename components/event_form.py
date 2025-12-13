import streamlit as st
from datetime import datetime, time
import uuid

from utils.calendar_utils import CORES
from utils.api_events import (
    criar_evento,
    atualizar_evento,
    excluir_evento
)


# --------------------------------------------------
# Utilitário
# --------------------------------------------------
def get_event_by_id(event_id):
    target = str(event_id)
    for ev in st.session_state.eventos:
        if str(ev.get("id")) == target:
            return ev
    return None


# --------------------------------------------------
# Formulário principal
# --------------------------------------------------
def show_event_form():
    modo = st.session_state.modo

    # ----------------------------------------------
    # Carrega evento (editar) ou prepara novo
    # ----------------------------------------------
    if modo == "editar":
        evento = get_event_by_id(st.session_state.evento_id_selecionado)
        if not evento:
            st.error("Evento não encontrado.")
            st.rerun()

        data_iso = evento["date"]
        data_br = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
        st.subheader(f"✏️ Editar evento – {data_br}")

    else:
        data_iso = st.session_state.data_temp
        data_br = datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
        st.subheader(f"➕ Novo evento – {data_br}")

        evento = {
            "date": data_iso,
            "start_time": "08:00",
            "end_time": "10:00",
            "local": "",
            "cor": list(CORES.values())[0]
        }

    # ----------------------------------------------
    # FORM
    # ----------------------------------------------
    with st.form("form_evento", clear_on_submit=False):

        titulo = st.text_input(
            "Título *",
            value=evento.get("titulo", evento.get("title", ""))
        )

        col1, col2 = st.columns(2)
        inicio = col1.time_input(
            "Início *",
            value=time.fromisoformat(evento.get("start_time", "08:00"))
        )
        fim = col2.time_input(
            "Fim *",
            value=time.fromisoformat(evento.get("end_time", "10:00"))
        )

        local = st.text_input(
            "Local",
            value=evento.get("local", "")
        )

        cor_atual = evento.get("cor", list(CORES.values())[0])

        tipo_evento = st.selectbox(
            "Tipo de evento",
            options=list(CORES.keys()),
            index=list(CORES.values()).index(cor_atual)
            if cor_atual in CORES.values() else 0
        )

        # 🎨 Color picker livre
        cor_escolhida = st.color_picker(
            "Cor do evento",
            value=cor_atual
        )

        c1, c2 = st.columns(2)
        salvar = c1.form_submit_button("Salvar", type="primary")
        cancelar = c2.form_submit_button("Cancelar")

    # ----------------------------------------------
    # CANCELAR
    # ----------------------------------------------
    if cancelar:
        _reset_form_state()
        st.rerun()

    # ----------------------------------------------
    # SALVAR
    # ----------------------------------------------
    if salvar:

        if not titulo.strip():
            st.error("Título é obrigatório.")
            return

        if inicio >= fim:
            st.error("Horário inválido.")
            return

        payload = {
            "id": evento.get("id") or str(uuid.uuid4()),
            "titulo": titulo.strip(),
            "date": evento["date"],
            "start_time": inicio.strftime("%H:%M"),
            "end_time": fim.strftime("%H:%M"),
            "local": local.strip(),
            "cor": cor_escolhida
        }

        # ------------------------------------------
        # CRIAR
        # ------------------------------------------
        if modo == "criar":
            try:
                criado = criar_evento(payload)
                st.session_state.eventos.append(criado)
                st.success("✅ Evento criado com sucesso!")
                _reset_form_state()
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao criar evento: {e}")
                return

        # ------------------------------------------
        # EDITAR
        # ------------------------------------------
        if modo == "editar":
            try:
                atualizado = atualizar_evento(
                    st.session_state.evento_id_selecionado,
                    payload
                )

                for i, ev in enumerate(st.session_state.eventos):
                    if str(ev.get("id")) == str(atualizado.get("id")):
                        st.session_state.eventos[i] = atualizado
                        break

                st.success("✏️ Evento atualizado!")
                _reset_form_state()
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao atualizar evento: {e}")
                return

    # ----------------------------------------------
    # EXCLUIR
    # ----------------------------------------------
    if modo == "editar":
        st.markdown("---")
        if st.button("🗑️ Excluir evento", type="secondary"):
            if st.checkbox("Sim, desejo excluir este evento permanentemente"):
                try:
                    excluir_evento(st.session_state.evento_id_selecionado)

                    st.session_state.eventos = [
                        e for e in st.session_state.eventos
                        if str(e.get("id")) != str(st.session_state.evento_id_selecionado)
                    ]

                    st.success("🗑️ Evento excluído!")
                    _reset_form_state()
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro ao excluir evento: {e}")
                    return


# --------------------------------------------------
# Reset de estado
# --------------------------------------------------
def _reset_form_state():
    st.session_state.modo = None
    st.session_state.evento_id_selecionado = None
    if "data_temp" in st.session_state:
        del st.session_state.data_temp
