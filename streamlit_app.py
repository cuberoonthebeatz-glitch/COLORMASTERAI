import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE ÉLITE
st.set_page_config(page_title="ColorMaster Royale", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

# 2. EL MOTOR DE IDENTIDAD (CSS RADICAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    
    :root {
        --accent: #FF4D80;
        --gold: #D4A373;
        --glass: rgba(255, 255, 255, 0.85);
    }

    /* Fondo Animado (Para que no sea triste/estático) */
    .stApp {
        background: linear-gradient(-45deg, #FFF5F7, #FDFCFB, #F8E1E7, #FFFFFF);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    header, footer, [data-testid="stSidebarNav"] {display: none !important;}

    /* Logo con Personalidad */
    .brand-header {
        font-family: 'Playfair Display', serif;
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(90deg, #1A1A1A, #FF4D80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }

    /* Tarjetas "Esponjosas" con Brillo de Cristal */
    .card-royale {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-radius: 35px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 20px 40px rgba(255, 77, 128, 0.08);
        margin-bottom: 20px;
    }

    /* Botones Neumórficos / Chuchería */
    .stButton>button {
        background: #1A1A1A !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 1.2rem 2rem !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
    }

    .stButton>button:hover {
        transform: scale(1.05) translateY(-5px) !important;
        background: var(--accent) !important;
        box-shadow: 0 15px 30px rgba(255, 77, 128, 0.4) !important;
    }

    /* Chat Estilo Burbuja Suave */
    .stChatMessage {
        border-radius: 30px !important;
        border: none !important;
        background: white !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02) !important;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE PERSISTENCIA
if 'auth' not in st.session_state: st.session_state.auth = False
if 'clientes' not in st.session_state: st.session_state.clientes = []

# 4. LOGIN CON "CHICHA"
if not st.session_state.auth:
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.markdown("<div style='text-align:center; margin-top:15vh;'>", unsafe_allow_html=True)
        st.markdown("<p class='brand-header'>ColorMaster</p>", unsafe_allow_html=True)
        st.markdown("<p style='letter-spacing:5px; color:#8E5B5B; font-weight:700; margin-top:-15px;'>ULTRA ROYALE</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='card-royale'>", unsafe_allow_html=True)
        api_key = st.text_input("LICENSE_KEY", type="password", placeholder="•••• •••• ••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESBLOQUEAR ACCESO ✨"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.auth = True
                st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

else:
    # 5. DASHBOARD DINÁMICO
    st.markdown("<p class='brand-header' style='font-size:35px;'>ColorMaster</p>", unsafe_allow_html=True)
    
    col_nav, col_main = st.columns([1.2, 3], gap="large")

    with col_nav:
        st.markdown("<div class='card-royale'>", unsafe_allow_html=True)
        st.markdown("### 🛠️ Workspace")
        marca = st.selectbox("Línea técnica:", ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken", "Otra"])
        
        with st.expander("➕ NUEVA CLIENTE", expanded=False):
            nombre = st.text_input("Nombre")
            notas = st.text_area("Notas Técnicas")
            if st.button("REGISTRAR"):
                if nombre:
                    st.session_state.clientes.append({"n": nombre, "h": notas})
                    st.rerun()
        
        st.divider()
        st.markdown("### 📋 Agenda")
        for c in st.session_state.clientes:
            st.markdown(f"**{c['n']}**")
            st.caption(f"📝 {c['h']}")
            
        if st.button("SALIR"):
            st.session_state.auth = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        # SISTEMA DE IA INTEGRADO
        st.markdown("<div class='card-royale' style='height: 700px; display: flex; flex-direction: column;'>", unsafe_allow_html=True)
        st.markdown("#### 🤖 Consulta IA Senior")
        
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "msgs" not in st.session_state: st.session_state.msgs = []
            
            chat_box = st.container(height=500, border=False)
            with chat_box:
                for m in st.session_state.msgs:
                    with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("¿Qué mezcla o diagnóstico hacemos?"):
                st.session_state.msgs.append({"role": "user", "content": p})
                with chat_box:
                    with st.chat_message("user"): st.markdown(p)
                
                res = model.generate_content(f"Mejor experto colorista del mundo. Marca {marca}. Responde pro: {p}")
                
                st.session_state.msgs.append({"role": "assistant", "content": res.text})
                with chat_box:
                    with st.chat_message("assistant"): st.markdown(res.text)
                    
        except Exception as e:
            st.error(f"Sistema: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        
