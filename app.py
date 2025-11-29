import streamlit as st
import datetime
from datetime import date, timedelta
import calendar as py_calendar

# Configuração da página
st.set_page_config(
    page_title="MySchedule",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado melhorado
st.markdown("""
<style>
    /* Estilos gerais */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Cards dos dias - MELHORADO */
    .day-card {
        background: #252440;
        border-radius: 12px;
        padding: 12px;
        margin: 2px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        height: 140px; /* Aumentado para melhor visualização */
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .day-card:hover {
        border-color: #4ECDC4;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .day-card.today {
        border-color: #FF6B6B;
        background: #252440;
    }
    
    .day-card.weekend {
        background: #252440;
    }
    
    .day-card.empty {
        background: #252440;
        border: 2px dashed #dee2e6;
    }
    
    .day-number {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
        color: #495057;
    }
    
    .day-number.today {
        color: #FF6B6B;
        font-weight: 800;
    }
    
    .day-number.weekend {
        color: #6c757d;
    }
    
    /* Eventos - MELHORADO */
    .events-container {
        flex-grow: 1;
        overflow-y: auto;
        max-height: 80px;
        margin-bottom: 8px;
    }
    
    .event-item {
        font-size: 11px; /* Aumentado para melhor legibilidade */
        margin: 3px 0;
        padding: 4px 6px;
        border-radius: 6px;
        background: #070a1a;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .event-privado {
        border-left-color: #4ECDC4;
        background: #252440;
    }
    
    .event-aula {
        border-left-color: #FFD166;
        background: #252440;
    }
    
    .event-público {
        border-left-color: #06D6A0;
        background: #252440;
    }
    
    .empty-state {
        font-size: 11px;
        color: #252440;
        text-align: center;
        margin-top: 15px;
        font-style: italic;
    }
    
    .more-events {
        font-size: 10px;
        color: #4ECDC4;
        text-align: center;
        margin: 4px 0;
        font-weight: 600;
    }
    
    /* Botão de adicionar evento - MELHORADO */
    .add-event-btn {
        background: transparent;
        border: 1px dashed #dee2e6;
        border-radius: 6px;
        color: #6c757d;
        padding: 4px;
        font-size: 12px;
        width: 100%;
        transition: all 0.2s ease;
        margin-top: auto;
    }
    
    .add-event-btn:hover {
        background: #f8f9fa;
        border-color: #4ECDC4;
        color: #4ECDC4;
    }
    
    /* Header do mês */
    .month-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Dias da semana */
    .weekday-header {
        background: #495057;
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        border-radius: 8px;
        margin: 2px;
    }
    
    /* Modal styling melhorado */
    .modal-container {
        background: rgba(0,0,0,0.5);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .modal-content {
        background: white;
        border-radius: 12px;
        padding: 24px;
        width: 90%;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* Melhorar os botões do Streamlit */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    .stButton button[kind="secondary"] {
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'show_event_modal' not in st.session_state:
    st.session_state.show_event_modal = False
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.datetime.now().date()
if 'current_month' not in st.session_state:
    st.session_state.current_month = datetime.datetime.now().month
if 'current_year' not in st.session_state:
    st.session_state.current_year = datetime.datetime.now().year
if 'events' not in st.session_state:
    st.session_state.events = [
        {
            "title": "Reunião FLJP Systems",
            "start": datetime.datetime(2024, 1, 15, 14, 0),
            "end": datetime.datetime(2024, 1, 15, 15, 0),
            "type": "private",
            "color": "#4ECDC4"
        },
        {
            "title": "Aula de Python - Programação Avançada",
            "start": datetime.datetime(2024, 1, 16, 9, 0),
            "end": datetime.datetime(2024, 1, 16, 11, 0),
            "type": "class",
            "color": "#FFD166"
        },
        {
            "title": "Workshop de Desenvolvimento Web",
            "start": datetime.datetime(2024, 1, 20, 10, 0),
            "end": datetime.datetime(2024, 1, 20, 12, 0),
            "type": "public",
            "color": "#06D6A0"
        }
    ]

def get_current_user():
    return {
        "name": "Pedro Muniz",
        "email": "pedro@email.com",
        "user_type": "student",
        "user_id": "user_001"
    }

def get_events_for_date(target_date):
    """Retorna eventos para uma data específica"""
    events = []
    for event in st.session_state.events:
        if event['start'].date() == target_date:
            events.append(event)
    return events

def render_sidebar():
    user = get_current_user()
    
    with st.sidebar:
        st.title(f"👋 Olá, {user['name']}!")
        st.caption(f"📧 {user['email']}")
        st.divider()
        
        st.page_link("app.py", label="📅 Calendário Principal", icon="🏠")
        st.page_link("pages/perfil.py", label="👤 Meu Perfil", icon="👤")
        st.page_link("pages/notificacoes.py", label="🔔 Notificações", icon="🔔")
        
        st.divider()
        
        # Eventos próximos dinâmicos
        st.subheader("📅 Eventos Próximos")
        today = datetime.datetime.now().date()
        upcoming_events = []
        
        for event in st.session_state.events:
            if event['start'].date() >= today:
                upcoming_events.append(event)
        
        # Ordenar por data e mostrar apenas os próximos 5
        upcoming_events.sort(key=lambda x: x['start'])
        for event in upcoming_events[:5]:
            event_date = event['start'].strftime('%d/%m')
            event_time = event['start'].strftime('%H:%M')
            
            # Definir ícone baseado no tipo
            event_icon = "🔵" if event['type'] == 'private' else "🟡" if event['type'] == 'class' else "🟢"
            st.caption(f"{event_icon} {event['title']} - {event_date} {event_time}")
        
        if not upcoming_events:
            st.caption("Nenhum evento próximo")
        
        st.divider()
        
        if st.button("➕ Criar Evento", use_container_width=True, type="primary"):
            st.session_state.show_event_modal = True
            st.session_state.selected_date = datetime.datetime.now().date()

def event_modal():
    """Modal de criar evento - Versão Corrigida"""
    if st.session_state.get('show_event_modal', False):
        # Usar columns para criar um overlay
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Container do modal
            with st.container():
                st.markdown(
                    """
                    <div style='
                        background: white; 
                        border-radius: 12px; 
                        padding: 24px; 
                        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                        border: 2px solid #e9ecef;
                    '>
                    """, 
                    unsafe_allow_html=True
                )
                
                st.header("📝 Criar Novo Evento")
                
                selected_date = st.session_state.get('selected_date', datetime.datetime.now().date())
                
                # Formulário corrigido
                with st.form("event_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        title = st.text_input(
                            "Título do Evento*", 
                            placeholder="Ex: Reunião de Projeto",
                            help="Nome descritivo do evento"
                        )
                        start_date = st.date_input(
                            "Data Início*", 
                            value=selected_date,
                            help="Data de início do evento"
                        )
                        start_time = st.time_input(
                            "Hora Início*", 
                            value=datetime.time(9, 0),
                            help="Hora de início"
                        )
                        
                    with col2:
                        event_type = st.selectbox(
                            "Tipo de Evento*", 
                            ["Privado", "Aula", "Público"],
                            help="Privado: só você vê | Aula: alunos convidados | Público: todos"
                        )
                        end_date = st.date_input(
                            "Data Fim*", 
                            value=selected_date,
                            help="Data de término do evento"
                        )
                        end_time = st.time_input(
                            "Hora Fim*", 
                            value=datetime.time(10, 0),
                            help="Hora de término"
                        )
                    
                    # Recorrência
                    recurrence = st.selectbox(
                        "Recorrência", 
                        ["Nenhuma", "Diária", "Semanal", "Mensal"],
                        help="Frequência de repetição do evento"
                    )
                    
                    # Descrição
                    description = st.text_area(
                        "Descrição", 
                        placeholder="Detalhes do evento...",
                        help="Informações adicionais sobre o evento"
                    )
                    
                    # Campos específicos por tipo de usuário
                    user = get_current_user()
                    if user['user_type'] == 'teacher':
                        st.multiselect(
                            "Convidar Alunos", 
                            ["Ana Silva", "Carlos Santos", "Maria Oliveira", "João Pereira"],
                            help="Selecione os alunos para esta aula"
                        )
                    
                    # Botões lado a lado
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                    
                    with col_btn1:
                        submitted = st.form_submit_button(
                            "💾 Salvar Evento", 
                            use_container_width=True,
                            type="primary"
                        )
                    
                    with col_btn2:
                        # Botão de cancelar dentro do formulário
                        if st.form_submit_button(
                            "❌ Cancelar", 
                            use_container_width=True
                        ):
                            st.session_state.show_event_modal = False
                            st.rerun()
                    
                    # Validação e salvamento
                    if submitted:
                        if not title:
                            st.error("📝 O título do evento é obrigatório!")
                        else:
                            # Adicionar evento à lista
                            new_event = {
                                "title": title,
                                "start": datetime.datetime.combine(start_date, start_time),
                                "end": datetime.datetime.combine(end_date, end_time),
                                "type": event_type.lower(),
                                "description": description,
                                "recurrence": recurrence
                            }
                            
                            st.session_state.events.append(new_event)
                            st.success("🎉 Evento criado com sucesso!")
                            st.session_state.show_event_modal = False
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

def render_beautiful_calendar():
    """Calendário bonito e funcional - VERSÃO MELHORADA"""
    # Header do mês com gradiente
    month_name = py_calendar.month_name[st.session_state.current_month]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀️ Mês Anterior", use_container_width=True):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="month-header">
            <h2 style="text-align: center; margin: 0; font-size: 28px;">{month_name} {st.session_state.current_year}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("Próximo Mês ▶️", use_container_width=True):
            if st.session_state.current_month == 12:
                st.session_state.current_month = 1
                st.session_state.current_year += 1
            else:
                st.session_state.current_month += 1
            st.rerun()
    
    # Dias da semana
    days_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    cols = st.columns(7)
    for i, day in enumerate(days_pt):
        with cols[i]:
            st.markdown(f'<div class="weekday-header">{day}</div>', unsafe_allow_html=True)
    
    # Calendário
    cal = py_calendar.monthcalendar(st.session_state.current_year, st.session_state.current_month)
    today = datetime.date.today()
    
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown('<div class="day-card empty"></div>', unsafe_allow_html=True)
                else:
                    current_date = date(st.session_state.current_year, st.session_state.current_month, day)
                    day_events = get_events_for_date(current_date)
                    
                    # Determinar classes CSS
                    css_class = "day-card"
                    if current_date == today:
                        css_class += " today"
                    if i >= 5:  # Fim de semana
                        css_class += " weekend"
                    
                    # Card do dia
                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                    
                    # Número do dia
                    day_class = "day-number today" if current_date == today else "day-number weekend" if i >= 5 else "day-number"
                    st.markdown(f'<div class="{day_class}">{day}</div>', unsafe_allow_html=True)
                    
                    # Container de eventos
                    st.markdown('<div class="events-container">', unsafe_allow_html=True)
                    
                    # Eventos do dia
                    if day_events:
                        for event in day_events[:3]:  # Mostrar até 3 eventos
                            event_class = f"event-item event-{event['type']}"
                            # Truncar título se necessário, mas manter mais caracteres
                            event_title = event['title'][:20] + "..." if len(event['title']) > 20 else event['title']
                            st.markdown(f'<div class="{event_class}" title="{event["title"]}">• {event_title}</div>', unsafe_allow_html=True)
                        
                        # Indicador de mais eventos
                        if len(day_events) > 3:
                            st.markdown(f'<div class="more-events">+{len(day_events)-3} mais</div>', unsafe_allow_html=True)
                    else:
                        # Estado vazio melhorado
                        st.markdown('<div class="empty-state">Sem eventos</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Fecha events-container
                    
                    # Botão para adicionar evento - MELHORADO
                    if st.button("＋ Adicionar", key=f"add_{day}", help=f"Criar evento em {day}/{st.session_state.current_month}", use_container_width=True):
                        st.session_state.selected_date = current_date
                        st.session_state.show_event_modal = True
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)  # Fecha day-card

def main():
    render_sidebar()
    
    if not st.session_state.show_event_modal:
        st.title("📅 MySchedule - Calendário")
        
        # Estatísticas rápidas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            today_events = len(get_events_for_date(datetime.datetime.now().date()))
            st.metric("Eventos Hoje", today_events)
        with col2:
            total_events = len(st.session_state.events)
            st.metric("Total de Eventos", total_events)
        with col3:
            this_month = len([e for e in st.session_state.events 
                            if e['start'].month == st.session_state.current_month 
                            and e['start'].year == st.session_state.current_year])
            st.metric("Eventos Este Mês", this_month)
        with col4:
            upcoming = len([e for e in st.session_state.events 
                          if e['start'].date() >= datetime.datetime.now().date()])
            st.metric("Eventos Futuros", upcoming)
        
        render_beautiful_calendar()
        
        # Legenda melhorada
        st.markdown("---")
        st.markdown("""
        **🎨 Legenda:** 
        🔵 **Privado** - Apenas você vê | 🟡 **Aula** - Alunos convidados | 🟢 **Público** - Todos veem
        """)
        
    else:
        # Quando o modal está aberto, mostramos apenas o modal centralizado
        event_modal()
        
        # Botão para voltar (abaixo do modal)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Voltar ao Calendário", use_container_width=True):
                st.session_state.show_event_modal = False
                st.rerun()

if __name__ == "__main__":
    main()