import streamlit as st

def render_perfil_page():
    """Renderiza página completa de perfil do usuário"""
    
    # Inicializar dados do user
    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "nome": "Pedro Muniz",
            "email": "pedro@email.com",
            "telefone": "(85) 98765-4321",
            "matricula": "2024001234",
            "curso": "Ciência da Computação",
            "instituicao": "Universidade Federal do Ceará",
            "semestre": "5º Semestre",
            "data_ingresso": "2022-02-01"
        }
    
        st.title("👤 Meu Perfil")
    
    # voltar
    if st.button("← Voltar ao Calendário"):
        st.session_state.pagina_atual = "📅 Calendário"
        st.rerun()
    
        st.markdown("---")
    
    # Tabs p/ organizar informações
    tab1, tab2 = st.tabs(["📋 Informações Pessoais", "🎓 Informações Acadêmicas"])
    
    with tab1:
        st.markdown("### Dados Pessoais")
        
        with st.form("form_dados_pessoais"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", value=st.session_state.user_data["nome"])
                email = st.text_input("Email Institucional *", value=st.session_state.user_data["email"], disabled=True)
                st.caption("💡 Email não pode ser alterado. Entre em contato com a secretaria.")
            
            with col2:
                telefone = st.text_input("Telefone", value=st.session_state.user_data["telefone"])
                matricula = st.text_input("Matrícula", value=st.session_state.user_data["matricula"], disabled=True)
            
            col_salvar, col_cancelar = st.columns([1, 1])
            
            with col_salvar:
                salvar_pessoal = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            
            with col_cancelar:
                cancelar_pessoal = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            if salvar_pessoal:
                st.session_state.user_data["nome"] = nome
                st.session_state.user_data["telefone"] = telefone
                st.success("✅ Dados pessoais atualizados com sucesso!")
            
            if cancelar_pessoal:
                st.rerun()
    
    with tab2:
        st.markdown("### Informações Acadêmicas")
        
        with st.form("form_dados_academicos"):
            curso = st.text_input("Curso", value=st.session_state.user_data["curso"])
            instituicao = st.text_input("Instituição", value=st.session_state.user_data["instituicao"])
            
            col1, col2 = st.columns(2)
            with col1:
                semestre = st.selectbox(
                    "Semestre Atual",
                    ["1º Semestre", "2º Semestre", "3º Semestre", "4º Semestre", 
                     "5º Semestre", "6º Semestre", "7º Semestre", "8º Semestre", 
                     "9º Semestre", "10º Semestre"],
                    index=4  # 5º Semestre
                )
            
            with col2:
                data_ingresso = st.date_input("Data de Ingresso", value=None)
            
            col_salvar2, col_cancelar2 = st.columns([1, 1])
            
            with col_salvar2:
                salvar_academico = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            
            with col_cancelar2:
                cancelar_academico = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            if salvar_academico:
                st.session_state.user_data["curso"] = curso
                st.session_state.user_data["instituicao"] = instituicao
                st.session_state.user_data["semestre"] = semestre
                if data_ingresso:
                    st.session_state.user_data["data_ingresso"] = str(data_ingresso)
                st.success("✅ Dados acadêmicos atualizados com sucesso!")
            
            if cancelar_academico:
                st.rerun()
    
    # Card de resumo
    st.markdown("---")
    st.markdown("### 📊 Resumo da Conta")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0;">{len(st.session_state.get('eventos', []))}</h2>
            <p style="margin: 5px 0 0 0;">Eventos Cadastrados</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_disciplinas = len(st.session_state.get('disciplinas', []))
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
             padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0;">{total_disciplinas}</h2>
            <p style="margin: 5px 0 0 0;">Disciplinas Ativas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Calcular média de faltas
        if st.session_state.get('disciplinas'):
            media_faltas = sum(d['faltas'] for d in st.session_state.disciplinas) / len(st.session_state.disciplinas)
        else:
            media_faltas = 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
             padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0;">{media_faltas:.1f}</h2>
            <p style="margin: 5px 0 0 0;">Média de Faltas</p>
        </div>
        """, unsafe_allow_html=True)