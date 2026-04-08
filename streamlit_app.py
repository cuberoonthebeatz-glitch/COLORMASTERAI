import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")
st.title("💇‍♀️ ColorMaster AI")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia:", type="password")
    marca = st.selectbox("Marca:", ["L'Oréal", "Schwarzkopf", "Wella", "Otra"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # OBLIGAMOS AL SISTEMA A NO USAR LA VERSIÓN v1beta
        # Usamos gemini-1.5-flash que es el más potente ahora
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe tu consulta..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # ESTA LÍNEA ES LA MAGIA: forzamos la versión v1
            response = model.generate_content(
                f"Experto en {marca}: {prompt}",
                request_options=RequestOptions(api_version='v1')
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Lo estamos intentando: {e}")
else:
    st.warning("👈 Pega tu llave nueva a la izquierda.")
