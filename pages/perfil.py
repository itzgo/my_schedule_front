import streamlit as st

st.title("👤 Meu Perfil")

user = {
    "name": "Pedro Muniz", 
    "email": "pedro@email.com",
    "user_type": "student",
    "institution": "Universidade Federal"
}

with st.form("profile_form"):
    st.text_input("Nome Completo", value=user["name"])
    st.text_input("Email", value=user["email"], disabled=True)
    st.text_input("Instituição", value=user["institution"])
    
    if st.form_submit_button("💾 Salvar Alterações"):
        st.success("Perfil atualizado com sucesso!")