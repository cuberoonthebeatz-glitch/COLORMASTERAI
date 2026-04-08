import streamlit as st
import google.generativeai as genai

# 1. SETUP DE ALTO RENDIMIENTO
st.set_page_config(page_title="ColorMaster Pro", page_icon="💄", layout="wide", initial_sidebar_state="collapsed")

# 2. IDENTIDAD VISUAL (GUMMY LUXURY 2026)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    :root {
        --primary: #FF85A1;
        --gold: #D4A373;
        --dark: #121212;
    }

    .stApp { background-color: #FDFBFA; font-family: 'Plus Jakarta Sans', sans-serif; }
    header, footer, [data-testid="stSidebarNav"] {display: none !important;}

    /* LOGIN CARD */
    .auth-card {
        background: white;
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        text-align: center;
        max-width: 400px;
        margin: 10vh auto;
        border: 1px solid #F0F0F0;
    }

    /* BOTONES ESPONJOSOS (GUMMY) */
    .stButton>button {
        background: var(--dark) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100%;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1) !important;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        background: var(--primary) !important;
        box-shadow: 0 12px 25px rgba(255, 133, 161, 0.3) !important;
    }

    /* PANELES DE TRABAJO */
    .panel-glass {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 30px;
        padding: 25px;
        border: 1px solid #F0F0F0;
        margin-bottom: 20px;
    }

    .brand-logo {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -2px;
        color: var(--dark);
        margin-bottom: 5px;
    }
    .brand-dot { color: var(--primary); }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE ESTADO (CORRECCIÓN DE ERROR)
if 'auth' not in st.session_state: st.session_state.auth = False
# Forzamos que sea una lista desde el principio
if 'clientes' not in st.session_state or isinstance(st.session_state.clientes, dict):
    st.session_state.clientes = []

# 4. PANTALLA DE ACCESO
if not st.session_state.auth:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='brand-logo'>ColorMaster<span class='brand-dot'>.</span></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;'>Creative Intelligence System</p>", unsafe_allow_html=True)
    
    api_key = st.text_input("LICENSE_KEY", type="password", placeholder="Introduce tu acceso...")
    if st.button("ACCEDER AL ECOSISTEMA"):
        if api_key:
            st.session_state.api_key = api_key
            st.session_state.auth = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 5. DASHBOARD PROFESIONAL
    st.markdown("<div class='brand-logo' style='font-size:24px; padding-left:20px;'>CM<span class='brand-dot'>.</span></div>", unsafe_allow_html=True)
    
    col_nav, col_main = st.columns([1, 3.5], gap="medium")

    with col_nav:
        st.markdown("### 🛠️ Herramientas")
        marca = st.selectbox("Línea", ["L'Oréal", "Wella", "Schwarzkopf", "Redken", "Otra"])
        
        with st.expander("👤 NUEVA CLIENTE", expanded=False):
            nombre = st.text_input("Nombre")
            notas = st.text_area("Notas (Alergias/Historial)")
            if st.button("Guardar Ficha"):
                if nombre:
                    st.session_state.clientes.append({"n": nombre, "h": notas})
                    st.success("Guardado")
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📋 Agenda")
        for idx, c in enumerate(st.session_state.clientes):
            with st.container():
                st.markdown(f"**{c['n']}**")
                st.caption(f"📝 {c['h']}")
        
        if st.button("SALIR"):
            st.session_state.auth = False
            st.rerun()

    with col_main:
        # CHAT DINÁMICO
        st.markdown("<div class='panel-glass'>", unsafe_allow_html=True)
        st.markdown("#### 🤖 Consulta Técnica")
        
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "msgs" not in st.session_state: st.session_state.msgs = []
            
            chat_container = st.container(height=500, border=False)
            with chat_container:
                for m in st.session_state.msgs:
                    with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("¿Qué caso vamos a resolver hoy?"):
                st.session_state.msgs.append({"role": "user", "content": p})
                with chat_container:
                    with st.chat_message("user"): st.markdown(p)
                
                contexto = f"Eres una IA de élite en peluquería y estética. Marca: {marca}. Responde de forma técnica y brillante. {p}"
                response = model.generate_content(contexto)
                
                st.session_state.msgs.append({"role": "assistant", "content": response.text})
                with chat_container:
                    with st.chat_message("assistant"): st.markdown(response.text)
                    
        except Exception as e:
            st.error(f"Sistema en mantenimiento: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
