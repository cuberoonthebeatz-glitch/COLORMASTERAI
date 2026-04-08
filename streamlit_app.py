import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")
st.title("💇‍♀️ ColorMaster AI")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia:", type="password")
    marca = st.selectbox("Marca:", ["L'Oréal", "Schwarzkopf", "Wella", "Redken", "Otra"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo 'gemini-1.5-flash' que es el actual
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe tu consulta aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = model.generate_content(f"Eres experto en peluquería de {marca}. {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("👈 Pega tu nueva clave a la izquierda.")
