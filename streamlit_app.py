import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ColorMaster AI", page_icon="💇‍♀️")

st.title("💇‍♀️ ColorMaster AI")
st.markdown("---")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Licencia (API KEY):", type="password")
    st.divider()
    marca = st.selectbox("Marca con la que trabajas:", ["L'Oréal Pro", "Wella", "Schwarzkopf (Igora)", "Redken", "Sassoon", "Otra"])

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Probamos con el modelo más estable sin especificar versiones raras
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Escribe tu duda técnica aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Instrucciones directas
            prompt_final = f"Eres un experto colorista senior de la marca {marca}. Responde de forma técnica y profesional: {prompt}"
            
            response = model.generate_content(prompt_final)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("👈 Pega tu llave AIza... en la izquierda para empezar.")
