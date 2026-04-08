import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE IMPACTO
st.set_page_config(page_title="ColorMaster X", page_icon="🔥", layout="wide")

# 2. ESTÉTICA RADICAL (NEO-POP INDUSTRIAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Space+Grotesk:wght@300;500;700&display=swap');
    
    /* Fondo con Personalidad */
    .stApp {
        background-color: #0F0F0F;
        background-image: radial-gradient(#1a1a1a 2px, transparent 2px);
        background-size: 30px 30px;
        font-family: 'Space Grotesk', sans-serif;
        color: white;
    }

    header, footer {visibility: hidden;}

    /* Logo Explosivo */
    .logo-vanguard {
        font-family: 'Syncopate', sans-serif;
        font-size: 80px;
        line-height: 0.8;
        background: linear-gradient(135deg, #FF0055, #FF5500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    /* Paneles de Neón */
    .neon-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.1);
    }

    /* Botones que "Explotan" */
    .stButton>button {
        background: #FF0055 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Syncopate', sans-serif !important;
        font-size: 14px !important;
        padding: 20px !important;
        width: 100% !important;
        transition: 0.3s !important;
    }

    .stButton>button:hover {
        background: #FF5500 !important;
        box-shadow: 0 0 30px #FF0055 !important;
        transform: scale(1.02);
    }

    /* Chat Estilo Cyberpunk */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #FF0055 !important;
        border-radius: 10px !important;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DATOS
if 'auth' not in st.session_state: st.session_state.auth = False
if 'clientes' not in st.session_state: st.session_state.clientes = []

# 4. LOGIN RADICAL
if not st.session_state.auth:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div style='margin-top:10vh;'>", unsafe_allow_html=True)
        st.markdown("<p class='logo-vanguard'>COLOR<br>MASTER<br>X</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FF0055;'>FUTURE OF BEAUTY. NOW.</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='neon-panel' style='margin-top:15vh;'>", unsafe_allow_html=True)
        api_key = st.text_input("ENTER API KEY", type="password")
        if st.button("UNLOCK SYSTEM"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.auth = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # 5. WORKSPACE DINÁMICO
    st.markdown("<p class='logo-vanguard' style='font-size:30px;'>CMX</p>", unsafe_allow_html=True)
    
    c_side, c_main = st.columns([1, 2.5])

    with c_side:
        with st.container(border=True):
            st.markdown("### 🎚️ CONTROL")
            marca = st.selectbox("MARCA", ["L'Oréal", "Wella", "Schwarzkopf", "Redken"])
            
            with st.expander("👤 AGENDAR CLIENTE"):
                n = st.text_input("NOMBRE")
                h = st.text_area("HISTORIAL")
                if st.button("GUARDAR"):
                    st.session_state.clientes.append({"n": n, "h": h})
            
            st.divider()
            for cli in st.session_state.clientes:
                st.markdown(f"🔴 **{cli['n']}**")
            
            if st.button("LOGOUT"):
                st.session_state.auth = False
                st.rerun()

    with c_main:
        st.markdown("<div class='neon-panel'>", unsafe_allow_html=True)
        st.markdown("#### 💬 CONEXIÓN IA ACTIVA")
        
        # Intentar respuesta forzada
        try:
            genai.configure(api_key=st.session_state.api_key)
            # USAMOS EL MODELO FLASH POR DEFECTO
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "msgs" not in st.session_state: st.session_state.msgs = []
            
            for m in st.session_state.msgs:
                with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("¿Qué caso vamos a destruir hoy?"):
                st.session_state.msgs.append({"role": "user", "content": p})
                with st.chat_message("user"): st.markdown(p)
                
                # Respuesta de la IA
                response = model.generate_content(f"Actúa como el mejor colorista del mundo. Marca {marca}. Respuesta corta y técnica: {p}")
                
                if response:
                    st.session_state.msgs.append({"role": "assistant", "content": response.text})
                    with st.chat_message("assistant"): st.markdown(response.text)
                else:
                    st.error("La IA no ha podido generar respuesta. Revisa tu clave.")
                    
        except Exception as e:
            st.error(f"ERROR DE CONEXIÓN: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
