import streamlit as st
from datetime import datetime

def render_sidebar():
    """Renderiza o menu lateral personalizado"""
    
    with st.sidebar:
        st.markdown("""
            <style>
                .sidebar-title {
                    font-size: 22px !important;
                    font-weight: 600;
                }
            </style>
            <p class="sidebar-title">Menu</p>
        """, unsafe_allow_html=True)
        
    
        opcao = st.radio(
            "Navegação",  
            ["Calendário", "Resumo do Dia", "Minhas Disciplinas"],
            label_visibility="collapsed" 
        )

        if opcao != st.session_state.get("ultima_opcao_menu"):
                    st.session_state.ultima_opcao_menu = opcao
        if          st.session_state.get("pagina_atual") == "👤 Perfil":
                    st.session_state.pagina_atual = opcao
        st.markdown("---")
        
        #Notificações
        st.markdown("###  Notificações")
        
        tem_notificacao = False
        
        # Alertas faltas
        if "disciplinas" in st.session_state:
            for disc in st.session_state.disciplinas:
                if disc.get('faltas', 0) >= 5:
                    tem_notificacao = True
                    st.markdown(
                        f'<div style="background: #fff3cd; border-left: 4px solid #ffc107; '
                        f'padding: 10px; margin: 5px 0; border-radius: 5px; color: #856404;">'
                        f'⚠️ {disc["faltas"]} faltas em {disc["nome"]}</div>',
                        unsafe_allow_html=True
                    )
        
        # Eventos hoje
        hoje = datetime.now().strftime("%Y-%m-%d")
        if "eventos" in st.session_state:
            eventos_hoje = [e for e in st.session_state.eventos if e.get('data') == hoje]
            for evt in eventos_hoje:
                tem_notificacao = True
                st.info(f" {evt['titulo']} às {evt.get('hora_inicio', 'N/A')}")
        
        if not tem_notificacao:
            st.caption("Nenhuma notificação no momento")
        
        st.markdown("---")
        
        # Seção Perfil
        st.markdown("### 👤 Perfil")

        perfil_clicked = st.button("👤 Ver Meu Perfil", use_container_width=True, key="perfil_sidebar")

        if perfil_clicked:
         st.session_state.pagina_atual = "👤 Perfil"


        
        with st.expander("⚙️ Configurações", expanded=False):
            st.markdown("#### Acessibilidade")
            aumentar_fonte = st.checkbox("Aumentar fonte (Baixa visão)")
            if aumentar_fonte:
                st.session_state.tamanho_fonte = 20
            else:
                st.session_state.tamanho_fonte = 16
            
            st.markdown("---")
            
            st.markdown("####  Segurança")
            if st.button(" Mudar Senha", use_container_width=True):
                st.session_state.show_change_password = True
            
            st.markdown("---")
            
            if st.button(" Sair", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.success("Você saiu da conta!")
                st.rerun()
        
        return opcao