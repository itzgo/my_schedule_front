import streamlit as st
from datetime import date

SEMESTRES = [
    "1º Semestre", "2º Semestre", "3º Semestre", "4º Semestre",
    "5º Semestre", "6º Semestre", "7º Semestre", "8º Semestre",
    "9º Semestre", "10º Semestre"
]

def render_perfil_page():
    """Renderiza página completa de perfil do usuário"""

    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "id": st.session_state.get("userId"),
            "nome": st.session_state.get("username", ""),
            "email": st.session_state.get("email", ""),
            "role": (
                st.session_state.get("Role")
                or st.session_state.get("role")
                or "Aluno"
            ),
            "telefone": "",
            "matricula": "",
            "curso": "",
            "instituicao": "",
            "semestre": None,
            "data_ingresso": None
        }

    user = st.session_state.user_data

    st.title("👤 Meu Perfil")

    if st.button("← Voltar ao Calendário"):
        st.session_state.pagina_atual = "📅 Calendário"
        st.rerun()

    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 Informações Pessoais", "🎓 Informações Acadêmicas"])

    # ================= TAB 1 =================
    with tab1:
        st.markdown("### Dados Pessoais")

        with st.form("form_dados_pessoais"):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome Completo *", value=user["nome"])
                email = st.text_input("Email *", value=user["email"], disabled=True)
                st.caption("💡 Email não pode ser alterado.")

            with col2:
                telefone = st.text_input("Telefone", value=user["telefone"])
                st.text_input(
                    "Perfil", 
                    value=user.get("role") or user.get("Role") or "Aluno", 
                    disabled=True
                )

            c1, c2 = st.columns(2)
            with c1:
                salvar = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
            with c2:
                cancelar = st.form_submit_button("Cancelar", use_container_width=True)

            if salvar:
                user["nome"] = nome
                user["telefone"] = telefone
                st.success("Dados pessoais atualizados!")

            if cancelar:
                st.rerun()

    # ================= TAB 2 =================
    with tab2:
        st.markdown("### Informações Acadêmicas")

        with st.form("form_dados_academicos"):
            curso = st.text_input("Curso", value=user["curso"])
            instituicao = st.text_input("Instituição", value=user["instituicao"])

            semestre_atual = user.get("semestre")
            semestre_index = SEMESTRES.index(semestre_atual) if semestre_atual in SEMESTRES else 0

            semestre = st.selectbox("Semestre Atual", SEMESTRES, index=semestre_index)

            data_ingresso = st.date_input(
                "Data de Ingresso",
                value=user["data_ingresso"] or date.today()
            )

            salvar = st.form_submit_button(
                "💾 Salvar Alterações",
                type="primary",
                use_container_width=True
            )

            cancelar = st.form_submit_button(
                "Cancelar",
                use_container_width=True
            )

            if salvar:
                user["curso"] = curso
                user["instituicao"] = instituicao
                user["semestre"] = semestre
                user["data_ingresso"] = data_ingresso
                st.success("Dados acadêmicos atualizados!")

            if cancelar:
                st.rerun()

    # ================= Resumo =================
    st.markdown("---")
    st.markdown("### 📊 Resumo da Conta")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_eventos = len(st.session_state.get("eventos", []))
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">{total_eventos}</h2>
                <p style="margin: 5px 0 0 0;">Eventos Cadastrados</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        disciplinas = st.session_state.get("disciplinas", [])
        total_disciplinas = len(disciplinas)

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">{total_disciplinas}</h2>
                <p style="margin: 5px 0 0 0;">Disciplinas Ativas</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        if disciplinas:
            media_faltas = sum(d.get("faltas", 0) for d in disciplinas) / len(disciplinas)
        else:
            media_faltas = 0

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">{media_faltas:.1f}</h2>
                <p style="margin: 5px 0 0 0;">Média de Faltas</p>
            </div>
            """,
            unsafe_allow_html=True
        )
