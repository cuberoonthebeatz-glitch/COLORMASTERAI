import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL (ESTÉTICA CHIC)
st.set_page_config(page_title="ColorMaster & Beauty AI", page_icon="✨", layout="centered")

# CSS para personalizar el diseño (Colores pastel, bordes suaves y fuentes elegantes)
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #FFF9F9;
    }
    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #F8E8E8 !important;
    }
    /* Títulos y textos */
    h1, h2, h3 {
        color: #8E5B5B !important;
        font-family: 'Inter', sans-serif;
    }
    /* Botones y inputs */
    .stButton>button {
        background-color: #D4A373;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 25px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #B5835A;
        border: none;
    }
    /* Estilo de los globos de chat */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABECERA CON ESTILO
st.title("✨ ColorMaster & Beauty AI")
st.markdown("<p style='color: #B5835A; font-style: italic;'>Donde la ciencia del color se encuentra con el arte de la belleza.</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. PANEL DE CONTROL (SIDEBAR)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌸 Menú Beauty</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3465/3465066.png", width=100)
    
    api_key = st.text_input("🔑 Tu Licencia Digital:", type="password", placeholder="Pega tu clave aquí...")
    
    st.divider()
    
    # Selector de especialidad
    especialidad = st.radio("🎯 ¿En qué trabajamos hoy?", ["Colorimetría Capilar", "Estética y Piel", "Tratamientos Premium"])
    
    marca = st.selectbox("💄 Marca o Línea:", 
                         ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken", "Casmara", "Natura Bissé", "Otra"])
    
    st.divider()
    st.caption("© 2024 ColorMaster Pro - Elegancia & Tecnología")

# 4. LÓGICA DE FUNCIONAMIENTO
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": f"¡Hola Pedro! Bienvenida a tu espacio de trabajo. ¿Qué reto de {especialidad} tenemos con {marca}?"}]

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Escribe tu consulta..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Contexto ultra-detallado para la IA
            contexto = f"Eres un consultor experto en {especialidad} trabajando con la marca {marca}. Tu tono es profesional, amable, servicial y elegante (estética chic). Ayuda al profesional con fórmulas, consejos técnicos o soluciones: {prompt}"
            
            response = model.generate_content(contexto)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error("✨ Estamos preparando tu sesión... Google está activando tu llave.")
        if "404" in str(e):
            st.info("💡 Consejo: Tómate un café. Google tarda unos 30 min en activar llaves nuevas. ¡En nada estará lista!")
else:
    # Pantalla de bienvenida cuando no hay clave
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Bienvenida al futuro del salón
        Esta herramienta te ayuda a:
        - Crear fórmulas de color perfectas.
        - Analizar tipos de piel y tratamientos.
        - Resolver dudas técnicas al instante.
        """)
    with col2:
        st.image("https://img.freepik.com/vector-gratis/ilustracion-concepto-maquillaje_114360-2135.jpg", width=200)
    
    st.warning("👈 Para empezar, introduce tu Licencia Digital en el panel izquierdo.")
