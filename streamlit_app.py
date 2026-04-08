import streamlit as st
import google.generativeai as genai

# 1. ESTÉTICA DE LA PÁGINA
st.set_page_config(page_title="ColorMaster Pro AI", page_icon="✨", layout="centered")

# CSS personalizado para cambiar colores (Peluquería de lujo)
st.markdown("""
    <style>
    .main {
        background-color: #fcfaf8;
    }
    .stButton>button {
        background-color: #d4af37;
        color: white;
        border-radius: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABECERA
st.title("✨ ColorMaster Pro AI")
st.subheader("Asistente Avanzado para Coloristas")
st.markdown("---")

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3465/3465066.png", width=100)
    st.header("Panel de Control")
    api_key = st.text_input("🔑 Licencia Digital:", type="password", help="Introduce tu clave AIza para activar.")
    
    st.divider()
    
    marca = st.selectbox("🛠️ Línea de Color:", 
                         ["L'Oréal Professionnel", "Wella Professionals", "Schwarzkopf Igora", "Redken Shades EQ", "Sassoon", "Otra"])
    
    st.divider()
    st.info("💡 **Consejo:** Si acabas de crear tu clave, Google puede tardar hasta 30-60 min en activarla. ¡Paciencia, maestro!")

# 4. CUERPO DEL CHAT
st.write(f"🟢 **Sistema configurado para:** {marca}")

if not api_key:
    st.warning("⚠️ Esperando conexión... Introduce tu licencia en el panel izquierdo para empezar a trabajar.")
    
    # Simulación de cómo se vería un consejo
    with st.expander("Ver ejemplo de consulta"):
        st.write("¿Cómo consigo un 10.21 sobre una base naranja persistente?")
else:
    try:
        genai.configure(api_key=api_key)
        # Usamos la ruta más compatible
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": f"¡Hola Pedro! Soy tu asistente de {marca}. ¿Qué caso técnico tenemos hoy en el salón?"}]

        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        if prompt := st.chat_input("Escribe aquí tu duda técnica..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Llamada a la IA
            response = model.generate_content(f"Eres experto colorista senior de {marca}. Responde: {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        # Mostramos un error más elegante
        st.error("🚀 El motor de Google se está calentando. Prueba de nuevo en unos minutos.")
        if "404" in str(e):
            st.info("Confirmado: Google aún no ha activado tu clave. Vamos a esperar un poco.")
