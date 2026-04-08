import streamlit as st
import google.generativeai as genai

# Configuración de la página (Título y Emoji en la pestaña)
st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")

# Título principal de tu aplicación
st.title("💇‍♀️ ColorMaster AI")
st.markdown("---")

# Barra lateral para configuración
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia (API KEY):", type="password")
    st.divider()
    marca = st.selectbox("Marca con la que trabajas:", ["L'Oréal Pro", "Wella", "Schwarzkopf (Igora)", "Redken", "Sassoon", "Otra"])
    st.info("Esta herramienta usa IA para asesoramiento en colorimetría.")

# Lógica principal de la App
if api_key:
    try:
        # Configuramos la llave de Google
        genai.configure(api_key=api_key)
        
        # Seleccionamos el motor de inteligencia artificial
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Historial del chat para que no se borren los mensajes
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostrar los mensajes anteriores
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Cuadro de texto para que tú escribas
        if prompt := st.chat_input("Escribe tu duda técnica aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Preparamos la orden para la IA
            contexto = f"Actúa como un experto colorista senior de la marca {marca}. Responde de forma técnica, profesional y clara: {prompt}"
            
            # Generamos la respuesta
            response = model.generate_content(contexto)
            
            # Mostramos la respuesta de la IA
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # Por si algo falla, que nos diga qué es
        st.error(f"Hubo un pequeño problema técnico: {e}")
else:
    # Mensaje si no has puesto la clave todavía
    st.warning("👈 Por favor, introduce tu llave AIza... en la barra lateral para activar a ColorMaster.")
