import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE MARCA Y ESTÉTICA
st.set_page_config(page_title="ColorMaster Pro AI", page_icon="✨", layout="centered")

# CSS Avanzado para estética "Chic & Minimal"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #FCF7F7;
    }
    
    /* Login Box */
    .login-box {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 50px;
    }
    
    /* Botones dorados */
    .stButton>button {
        background: linear-gradient(135deg, #D4A373 0%, #B5835A 100%);
        color: white !important;
        border-radius: 30px !important;
        border: none;
        padding: 10px 30px !important;
        font-weight: 600;
        width: 100%;
    }
    
    /* Ocultar barra de arriba de Streamlit */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE INICIO DE SESIÓN (LOGIN)
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # PANTALLA DE BIENVENIDA / LOGIN
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3465/3465066.png", width=80)
    st.markdown("<h1 style='color: #8E5B5B;'>ColorMaster Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B5835A;'>Bienvenida al espacio exclusivo para profesionales de la belleza</p>", unsafe_allow_html=True)
    
    api_key_input = st.text_input("Introduce tu Licencia Digital para acceder:", type="password")
    
    if st.button("Iniciar Sesión"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Por favor, introduce una licencia válida.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 3. INTERFAZ DE LA APLICACIÓN (YA LOGUEADO)
    
    # Barra lateral más limpia
    with st.sidebar:
        st.markdown("<h2 style='color: #8E5B5B;'>🌸 Panel Principal</h2>", unsafe_allow_html=True)
        st.divider()
        marca = st.selectbox("Línea de trabajo:", ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken", "Casmara", "Otra"])
        especialidad = st.radio("Especialidad:", ["Colorimetría", "Estética Corporal/Facial", "Tricología"])
        
        if st.button("Cerrar Sesión"):
            st.session_state.auth = False
            st.rerun()

    # Título del Chat
    st.markdown(f"<h3 style='color: #8E5B5B;'>✨ Consultoría: {marca}</h3>", unsafe_allow_html=True)
    
    try:
        genai.configure(api_key=st.session_state.api_key)
        # Ajuste a modelo Flash para mayor velocidad
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Sesión iniciada. Soy tu experto personal, ¿qué reto tenemos hoy?"}]

        # Mostrar historial
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Entrada de chat
        if prompt := st.chat_input("Escribe tu consulta técnica..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Petición a la IA
            contexto = f"Eres un colorista y experto en estética de alto nivel. Usas la marca {marca}. Responde de forma técnica y elegante: {prompt}"
            response = model.generate_content(contexto)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        if st.button("Reintentar"):
            st.rerun()
