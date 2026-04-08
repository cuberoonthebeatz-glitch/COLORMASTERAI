import streamlit as st
import google.generativeai as genai

# Configuración visual de la App
st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")

st.title("💇‍♀️ ColorMaster AI")
st.markdown("---")

# Barra lateral para configuración
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia (API KEY):", type="password")
    st.info("Esta es la llave AIza... que copiaste de Google.")
    
    st.divider()
    marca = st.selectbox("Marca con la que trabajas:", ["L'Oréal Pro", "Wella", "Schwarzkopf (Igora)", "Redken", "Sassoon", "Otra"])
    especialidad = st.radio("Función principal:", ["Colorimetría", "Gestión de Agenda", "Marketing RRSS"])

# Lógica de la IA
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.0-pro')

        # Instrucciones maestras (El cerebro)
        prompt_base = f"Eres ColorMaster AI, un experto colorista con 30 años de experiencia. " \
                      f"Tu marca principal es {marca}. Tu tono es profesional y técnico. " \
                      "Ayudas a peluqueros a evitar errores de oxidación y fondos de aclaración indeseados."

        # Chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe tu duda técnica aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            full_prompt = f"{prompt_base}. Contexto actual: {especialidad}. Consulta del peluquero: {prompt}"
            response = model.generate_content(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error con la llave: {e}")
else:
    st.warning("👈 Por favor, introduce tu llave AIza... en la barra lateral para activar a ColorMaster.")
