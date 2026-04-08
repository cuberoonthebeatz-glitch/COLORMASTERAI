import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN TÉCNICA
st.set_page_config(page_title="ColorMaster Pro", page_icon="🎨", layout="wide")

# CSS para maximizar el espacio y dar estilo profesional
st.markdown("""
    <style>
    /* Eliminar espacios blancos superiores */
    .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 95%;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Fondo y texto */
    .stApp {background-color: #f8f9fa;}
    
    /* Input de login más profesional */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Chat más ancho y limpio */
    .stChatMessage {background-color: white !important; border: 1px solid #eee !important;}
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE ACCESO
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.subheader("🔐 Acceso ColorMaster Pro")
    api_key_input = st.text_input("Licencia:", type="password", placeholder="Introduce tu API Key...")
    if st.button("ENTRAR"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.auth = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 3. INTERFAZ DE TRABAJO (MAXIMIZADA)
    with st.sidebar:
        st.title("⚙️ Ajustes")
        marca = st.selectbox("Marca:", ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken", "Casmara", "Otra"])
        especialidad = st.radio("Modo:", ["Colorimetría", "Estética", "Tricología"])
        st.divider()
        if st.button("Cerrar Sesión"):
            st.session_state.auth = False
            st.rerun()

    # Título directo
    st.markdown(f"### 🤖 Asistente {especialidad} | {marca}")
    
    try:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostrar chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Entrada de texto (Chat)
        if prompt := st.chat_input("Escribe tu caso técnico..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Prompt técnico optimizado
            contexto = f"Eres un experto colorista y esteticista de alto nivel. Marca: {marca}. Especialidad: {especialidad}. Responde de forma técnica, precisa y breve. {prompt}"
            
            # Generar respuesta
            with st.spinner("Analizando..."):
                response = model.generate_content(contexto)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
