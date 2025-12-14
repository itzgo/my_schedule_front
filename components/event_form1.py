
import streamlit as st
from datetime import datetime, time
from utils.api_events import criar_evento, atualizar_evento, excluir_evento
from utils.calendar_utils import CORES
import uuid

# Utilitário
def get_event_by_id(event_id):
    target = str(event_id)
    for ev in st.session_state.eventos:
        if str(ev.get("id")) == target:
            return ev
    return None

# Formulário principal
def show_event_form():
    modo = st.session_state.modo

    # Configurações iniciais do formulário
    if modo == "editar":
        evento = get_event_by_id(st.session_state.evento_id_selecionado)
        if not evento:
            st.error("Evento não encontrado. Recarregando IDs...")
            st.rerun()
        data_br = datetime.strptime(evento["date"], "%Y-%m-%d").strftime("%d/%m/%Y")
        st.subheader(f"Editar evento – {data_br}")
    else:
        data = st.session_state.data_temp
        data_br = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        st.subheader(f"Novo evento – {data_br}")
        evento = {"date": data}

    # Formulário
    with st.form("form_evento"):
        titulo = st.text_input("Título *", value=evento.get("titulo", ""))
        col1, col2 = st.columns(2)
        inicio = col1.time_input("Início *", value=time.fromisoformat(evento.get("start_time", "08:00")))
        fim = col2.time_input("Fim *", value=time.fromisoformat(evento.get("end_time", "10:00")))
        local = st.text_input("Local", value=evento.get("local", ""))

        cor_atual = evento.get("cor", list(CORES.values())[0])
        tipo_evento = st.selectbox(
            "Tipo de evento", 
            options=list(CORES.keys()),
            index=next((i for i, v in enumerate(CORES.values()) if v == cor_atual), 0)
        )

        c1, c2 = st.columns(2)
        salvar = c1.form_submit_button("Salvar", type="primary")
        cancelar = c2.form_submit_button("Cancelar")

        if cancelar:
            st.session_state.modo = None
            st.session_state.evento_id_selecionado = None
            if "data_temp" in st.session_state:
                del st.session_state.data_temp
            st.rerun()

        if salvar:
            if not titulo.strip():
                st.error("Título obrigatório.")
            elif inicio >= fim:
                st.error("Horário inválido.")
            else:
                novo = {
                    "id": evento.get("id") or str(uuid.uuid4()),
                    "titulo": titulo.strip(),
                    "date": evento["date"],
                    "start_time": inicio.strftime("%H:%M"),
                    "end_time": fim.strftime("%H:%M"),
                    "local": local.strip(),
                    "cor": CORES[tipo_evento]
                }

                if modo == "editar":
                    try:
                        atualizado = atualizar_evento(st.session_state.evento_id_selecionado, novo)

                        for i, e in enumerate(st.session_state.eventos):
                            if str(e.get("id")) == str(st.session_state.evento_id_selecionado):
                                st.session_state.eventos[i] = atualizado
                                break

                        st.success("Evento atualizado!")
                    except Exception as e:
                        st.error(f"Erro ao atualizar evento: {e}")
                        return

                else:
                    try:
                        criado = criar_evento(novo)
                        st.session_state.eventos.append(criado)
                        st.success("Evento criado!")
                    except Exception as e:
                        st.error(f"Erro ao criar evento: {e}")
                        return

                save_events(st.session_state.eventos)
                st.session_state.modo = None
                st.session_state.evento_id_selecionado = None
                if "data_temp" in st.session_state:
                    del st.session_state.data_temp
                st.session_state.show_add_evento = False 
                st.rerun()

    # EXCLUSÃO
    if modo == "editar":
        st.markdown("---")
        if st.button("EXCLUIR EVENTO", type="secondary"):
            if st.checkbox("Sim, eu quero apagar este evento permanentemente"):
                target_id = str(st.session_state.evento_id_selecionado)
                antes = len(st.session_state.eventos)
                try:
                    excluir_evento(target_id)

                    st.session_state.eventos = [
                        e for e in st.session_state.eventos
                        if str(e.get("id")) != target_id
                    ]

                    st.success("Evento excluído!")
                except Exception as e:
                    st.error(f"Erro ao excluir evento: {e}")
                    return
