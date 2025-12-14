import streamlit as st
from utils.calendar_utils import render_calendar, handle_callback
from components.event_form import show_event_form
from components.sidebar_menu import render_sidebar
from pages.perfil import render_perfil_page  
from datetime import datetime
from pages.url import USER_ID_FIXO
from pages.login import render_login_page
from utils.api_events import listar_eventos_por_usuario, listar_eventos_publicos
from utils.event_loader import merge_eventos


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    render_login_page()
    st.stop()

if "user_id" not in st.session_state:
    st.session_state.user_id = USER_ID_FIXO


if "user_id" not in st.session_state:
    st.session_state.user_id = USER_ID_FIXO

# Configuracoes
st.set_page_config(
    page_title="Agenda Universitária", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { 
            display: none; 
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Aumenta o espaço no topo da página */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)
# CSS para esconder menu padrão e ajustar layout
st.markdown("""
    <style>
        /* Esconder menu padrão do Streamlit */
        [data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Ajustar layout */
        .block-container {
            padding-top: 2rem !important;
        }
        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            margin-bottom: 1.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

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

# Função para buscar eventos da API
if "eventos" not in st.session_state:
    try:
        eventos_usuario = listar_eventos_por_usuario(
            st.session_state.user_id
        )

        eventos_publicos = listar_eventos_publicos()

        st.session_state.eventos = merge_eventos(eventos_usuario, eventos_publicos)
    except Exception as e:
        st.error(f"Erro ao carregar eventos: {e}")
        st.session_state.eventos = []

# Disciplinas Mockadas
if "disciplinas" not in st.session_state:
    st.session_state.disciplinas = [
        {'nome': 'Matemática', 'faltas': 3, 'total': 40},
        {'nome': 'História', 'faltas': 6, 'total': 40},
    ]

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Calendário"

# Renderizar sidebar e capturar opção selecionada
opcao_menu = render_sidebar()

if st.session_state.get("pagina_atual") == "👤 Perfil":
    render_perfil_page()
else:
    st.session_state.pagina_atual = opcao_menu
    
    # Conteúdo do Calendário
    if opcao_menu == "Calendário":
        # Botões etc só do calendário
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("Agenda Universitária")
        with col2:
            if st.button("➕ Adicionar Evento"):
                st.session_state.modo = "criar"
                st.session_state.data_temp = datetime.now().strftime("%Y-%m-%d")
        
        # Renderiza o calendário
        callback = render_calendar()
        handle_callback(callback)
        
        # Mostra formulário se estiver em modo criar/editar
        if st.session_state.get("modo") in ["criar", "editar"]:
            titulo_expander = "➕ Novo Evento" if st.session_state.get("modo") == "criar" else "✏️ Editar Evento"
            with st.expander(titulo_expander, expanded=True):
                show_event_form()

    # Conteúdo do Resumo do Dia
    elif opcao_menu == "Resumo do Dia":
        st.title("Resumo do Dia")
        
        hoje = datetime.now().strftime("%Y-%m-%d")
        eventos_hoje = [e for e in st.session_state.eventos if e.get('date') == hoje]
        
        st.markdown("###  Eventos de Hoje")
        if eventos_hoje:
            for evt in eventos_hoje:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     padding: 15px; border-radius: 10px; margin: 10px 0; color: white;">
                    <h4 style="margin: 0;">{evt['title']}</h4>
                    <p style="margin: 5px 0;"> {evt.get('start_time')} - {evt.get('end_time')}</p>
                    <p style="margin: 0;"> {evt.get('local', 'Sem local definido')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum evento para hoje")
        
        st.markdown("###  Aulas de Hoje")
        for disc in st.session_state.disciplinas[:3]:
            porcentagem = (disc['faltas'] / disc['total']) * 100
            cor_borda = "#e74c3c" if porcentagem > 20 else "#2ecc71"
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; 
                 margin: 8px 0; border-left: 4px solid {cor_borda}; color: #212529;">
                <p style="margin: 0; color: #495057;"><strong>{disc['nome']}</strong> - Faltas: {disc['faltas']}/{disc['total']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Conteúdo de Minhas Disciplinas
    elif opcao_menu == "Minhas Disciplinas":
        st.title("Minhas Disciplinas")
        
        for disc in st.session_state.disciplinas:
            porcentagem = (disc['faltas'] / disc['total']) * 100
            cor = "🔴" if porcentagem > 20 else "🟢"
            cor_borda = "#e74c3c" if porcentagem > 20 else "#2ecc71"
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; 
                 margin: 12px 0; border-left: 5px solid {cor_borda}; color: #212529;">
                <h3 style="color: #343a40; margin-top: 0;">{cor} {disc['nome']}</h3>
                <p style="color: #495057; font-size: 18px; margin-bottom: 0;">
                    Faltas: <strong>{disc['faltas']}/{disc['total']}</strong> ({porcentagem:.1f}%)
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Rodapé
    st.markdown("---")
    st.caption(
        f"Total de eventos: {len(st.session_state.eventos)} | "
        "Clique no dia → criar | Clique no evento → editar/excluir"
    )

