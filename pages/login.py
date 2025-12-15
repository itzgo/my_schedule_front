import streamlit as st
import requests
from pages.url import URL_BASE, AUTH_LOGIN

def render_login_page():

    # ======================================================
    # CSS GLOBAL (mantido)
    # ======================================================
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }

            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            header[data-testid="stHeader"] {
                display: none;
            }

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            .stApp {
                background: #0a0e12;
            }

            .login-title {
                color: #ffffff;
                font-size: 2.5rem;
                font-weight: 600;
                text-align: center;
                margin-bottom: 1rem;
                letter-spacing: -0.5px;
            }

            .login-divider {
                border: none;
                height: 1px;
                background: #2a3038;
                margin: 1.5rem 0 2rem 0;
            }

            .stTextInput > label {
                color: #e0e0e0 !important;
                font-size: 0.95rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem !important;
            }

            .stTextInput > div > div > input {
                background: #2a3038 !important;
                border: 1px solid #3a4048 !important;
                border-radius: 8px !important;
                color: #ffffff !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
            }

            .stTextInput > div > div > input:focus {
                border-color: #4a88ff !important;
                box-shadow: 0 0 0 2px rgba(74, 136, 255, 0.1) !important;
            }

            .stTextInput {
                margin-bottom: 1.5rem;
            }

            .stButton > button {
                background: #4a88ff !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.75rem 1.5rem !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                width: 100% !important;
                margin-top: 1rem !important;
                transition: all 0.2s ease !important;
            }

            .stButton > button:hover {
                background: #3a78ef !important;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(74, 136, 255, 0.3) !important;
            }

            .forgot-password {
                text-align: right;
                margin-top: 0.75rem;
                margin-bottom: 0.5rem;
            }

            .forgot-password a {
                color: #4a88ff;
                text-decoration: none;
                font-size: 0.9rem;
            }

            .forgot-password a:hover {
                color: #3a78ef;
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # ======================================================
    # CONTEÚDO
    # ======================================================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<h1 class="login-title">Login</h1>', unsafe_allow_html=True)
        st.markdown('<hr class="login-divider">', unsafe_allow_html=True)

        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        st.markdown("""
            <div class="forgot-password">
                <a href="#" onclick="return false;">Esqueci minha senha</a>
            </div>
        """, unsafe_allow_html=True)

        # ======================================================
        # BOTÃO LOGIN
        # ======================================================
        if st.button("Entrar", use_container_width=True):

            if not email or not senha:
                st.warning(" Preencha email e senha")
                return

            try:
                with st.spinner("Autenticando..."):
                    response = requests.post(
                        f"{URL_BASE}{AUTH_LOGIN}",
                        json={
                            "email": email,
                            "password": senha
                        },
                        timeout=10
                    )

                # ----------------------------------------------
                # SUCESSO
                # ----------------------------------------------
                if response.status_code == 200:
                    data = response.json()

                    # ------------------------------------------
                    # AUTH
                    # ------------------------------------------
                    st.session_state.authenticated = True
                    st.session_state.token = data.get("token")

                    # ------------------------------------------
                    # USER BÁSICO
                    # ------------------------------------------
                    st.session_state.userId = data.get("userId")
                    st.session_state.email = data.get("email")
                    st.session_state.username = data.get(
                        "name",
                        email.split("@")[0]
                    )

                    # ------------------------------------------
                    # PERFIL (para página de perfil)
                    # ------------------------------------------
                    st.session_state.user_data = {
                        "nome": data.get("name"),
                        "email": data.get("email"),
                        "telefone": data.get("phone", ""),
                        "matricula": data.get("matricula", ""),
                        "curso": data.get("curso", ""),
                        "instituicao": data.get("instituicao", ""),
                        "semestre": data.get("semestre", ""),
                        "data_ingresso": data.get("dataIngresso")
                    }

                    # ------------------------------------------
                    # ROLE (importante p/ eventos recorrentes)
                    # ------------------------------------------
                    st.session_state.role = data.get("role", "Aluno")

                    st.success("Login realizado com sucesso!")
                    st.rerun()

                # ----------------------------------------------
                # ERROS
                # ----------------------------------------------
                elif response.status_code == 401:
                    st.error(" Email ou senha inválidos")

                elif response.status_code == 404:
                    st.error(" Usuário não encontrado")

                else:
                    st.error(f" Erro no servidor: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error(" Erro de conexão com o servidor")

            except requests.exceptions.Timeout:
                st.error(" Tempo de resposta excedido")

            except Exception as e:
                st.error(f" Erro inesperado: {str(e)}")
