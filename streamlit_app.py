import streamlit as st
import google.generativeai as genai
import os

# CONFIGURACIÓN PARA FORZAR LA VERSIÓN CORRECTA
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"

st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")
st.title("💇‍♀️ ColorMaster AI")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia:", type="password")
    marca = st.selectbox("Marca:", ["L'Oréal", "Schwarzkopf", "Wella", "Redken", "Otra"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # PROBAMOS CON ESTA RUTA ESPECÍFICA QUE SE SALTA EL ERROR 404
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Escribe aquí tu duda técnica..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Respuesta
            response = model.generate_content(f"Eres experto colorista de {marca}. {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Si ves un error 404, espera 5 minutos. Google está activando tu nueva clave.")
else:
    st.warning("👈 Introduce la clave para arrancar.")
