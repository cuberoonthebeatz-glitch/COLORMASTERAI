import streamlit as st
import google.generativeai as genai

# 1. SETUP DE ALTO RENDIMIENTO
st.set_page_config(page_title="ColorMaster Pro 2026", page_icon="💄", layout="wide", initial_sidebar_state="collapsed")

# 2. MOTOR ESTRÉMICO DE DISEÑO (Identidad Visual Única)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    :root {
        --primary: #FF85A1;
        --accent: #D4A373;
        --dark: #1A1A1A;
        --bg: #FDFBFA;
    }

    .stApp {
        background: var(--bg);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* OCULTAR INTERFAZ NATIVA */
    header, footer, [data-testid="stSidebarNav"] {display: none !important;}
    .block-container {padding: 1rem 3rem !important;}

    /* LOGIN SOFISTICADO */
    .auth-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 40px;
        padding: 50px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.05);
        text-align: center;
        max-width: 450px;
        margin: 10vh auto;
    }

    /* BOTONES NEUMÓRFICOS (Efecto Chuchería/Esponjoso) */
    .stButton>button {
        background: var(--dark) !important;
        color: white !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 18px 40px !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        background: var(--primary) !important;
        box-shadow: 0 15px 30px rgba(255, 133, 161, 0.3) !important;
    }

    /* TARJETAS DINÁMICAS (Glassmorphism) */
    .panel {
        background: white;
        border-radius: 32px;
        padding: 24px;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
    }
    
    .panel:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.06);
        border-color: var(--primary);
    }

    /* CHAT DE NUEVA GENERACIÓN */
    .stChatMessage {
        background: #F9F9F9 !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }

    /* TITULOS IDENTIDAD */
    .brand {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -2px;
        color: var(--dark);
        margin-bottom: 0px;
    }
    
    .dot { color: var(--primary); }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE ESTADO
if 'auth' not in st.session_state: st.session_state.auth = False
if 'clientes' not in st.session_state: st.session_state.clientes = []

# 4. PANTALLA DE ACCESO (Vibe 2026)
if not st.session_state.auth:
    st.markdown("""
        <div class='auth-card'>
            <div class='brand'>ColorMaster<span class='dot'>.</span></div>
            <p style='color:#888; margin-bottom:40px;'>Inteligencia Creativa para el Salón Moderno</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        api_key = st.text_input("LICENSE_KEY", type="password", placeholder="Acceso VIP")
        if st.button("ENTRAR AL ECOSISTEMA"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.auth = True
                st.rerun()

else:
    # 5. DASHBOARD INTEGRADO (MÁXIMA UTILIDAD)
    st.markdown("<div class='brand' style='font-size:28px;'>CM<span class='dot'>.</span></div>", unsafe_allow_html=True)
    
    col_nav, col_main = st.columns([1, 3.5], gap="large")

    with col_nav:
        st.markdown("### 🛠️ Herramientas")
        marca = st.selectbox("Marca", ["L'Oréal", "Wella", "Schwarzkopf", "Redken", "Otra"])
        
        with st.expander("👤 NUEVA CLIENTE", expanded=False):
            nombre = st.text_input("Nombre")
            notas = st.text_area("Notas (Alergias/Historial)")
            if st.button("Guardar Ficha"):
                st.session_state.clientes.append({"n": nombre, "h": notas})
                st.toast("Cliente Registrada")

        st.markdown("---")
        st.markdown("### 📋 Agenda")
        for c in st.session_state.clientes:
            st.markdown(f"**{c['n']}**")
            st.caption(c['h'])
            
        if st.button("SALIR"):
            st.session_state.auth = False
            st.rerun()

    with col_main:
        # SISTEMA DE IA INTEGRADO
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("#### 🤖 Asistente de Diagnóstico")
        
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "msgs" not in st.session_state: st.session_state.msgs = []
            
            # Área de chat con scroll controlado para evitar lag
            chat_container = st.container(height=450, border=False)
            with chat_container:
                for m in st.session_state.msgs:
                    with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("¿Qué técnica vamos a aplicar hoy?"):
                st.session_state.msgs.append({"role": "user", "content": p})
                with chat_container:
                    with st.chat_message("user"): st.markdown(p)
                
                contexto = f"Eres una IA de élite en peluquería. Marca: {marca}. Responde rápido y con estilo profesional. {p}"
                response = model.generate_content(contexto)
                
                st.session_state.msgs.append({"role": "assistant", "content": response.text})
                with chat_container:
                    with st.chat_message("assistant"): st.markdown(response.text)
                    
        except Exception as e:
            st.error(f"Error de sistema: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

        # SECCIÓN DE MEZCLAS RÁPIDAS (Debajo del chat)
        st.markdown("<br>", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("<div class='panel'><b>🧪 Mezcla del Momento</b><br>Usa el chat para pedir fórmulas y anótalas aquí.</div>", unsafe_allow_html=True)
        with col_m2:
            st.markdown("<div class='panel'><b>📢 Novedades 2026</b><br>Tendencias: 'Butter Gloss' y 'Mushroom Blonde'.</div>", unsafe_allow_html=True)
