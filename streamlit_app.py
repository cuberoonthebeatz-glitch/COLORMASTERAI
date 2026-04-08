import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")

st.title("💇‍♀️ ColorMaster AI")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia:", type="password")
    marca = st.selectbox("Marca:", ["L'Oréal", "Wella", "Schwarzkopf (Igora)", "Redken", "Otra"])

if api_key:
    try:
        # CONFIGURACIÓN FORZADA PARA EVITAR EL ERROR 404
        options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com")
        genai.configure(api_key=api_key, client_options=options)
        
        # Intentamos con el modelo Pro que es el más compatible
        model = genai.GenerativeModel('gemini-1.5-pro')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe aquí tu consulta..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = model.generate_content(f"Eres un experto en peluquería de {marca}. Responde: {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error detectado: {e}")
else:
    st.warning("👈 Introduce la clave para activar el sistema.")
