import streamlit as st
import google.generativeai as genai

# 1. ENGINE CONFIG
st.set_page_config(page_title="ColorMaster Black", page_icon="🖤", layout="wide")

# 2. EL ADN VISUAL (CSS DE ÉLITE)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200;800&family=Instrument+Sans:wght@400;600&display=swap');
    
    :root {
        --bg-color: #050505;
        --card-bg: #0f0f0f;
        --accent: #FF3366;
        --text: #ffffff;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text);
        font-family: 'Instrument Sans', sans-serif;
    }

    header, footer {visibility: hidden;}

    /* LOGO IMPACTO */
    .hero-text {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: clamp(40px, 8vw, 100px);
        font-weight: 800;
        line-height: 0.9;
        letter-spacing: -4px;
        background: linear-gradient(to bottom, #fff 30%, #444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* CONTENEDORES TIPO APP */
    .app-panel {
        background: var(--card-bg);
        border: 1px solid #222;
        border-radius: 24px;
        padding: 24px;
        transition: border 0.3s ease;
    }
    .app-panel:hover {
        border-color: var(--accent);
    }

    /* BOTONES LUXURY */
    .stButton>button {
        background: white !important;
        color: black !important;
        border-radius: 100px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        background: var(--accent) !important;
        color: white !important;
        transform: scale(0.98);
    }

    /* CHAT MINIMALISTA */
    .stChatMessage {
        background: #151515 !important;
        border: 1px solid #222 !important;
        border-radius: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SESIÓN
if 'auth' not in st.session_state: st.session_state.auth = False
if 'db' not in st.session_state: st.session_state.db = []

# 4. ACCESO EXCLUSIVO
if not st.session_state.auth:
    st.markdown("<div style='margin-top:10vh; text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-text'>COLOR<br>MASTER.</h1>", unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        key = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if key:
                st.session_state.api_key = key
                st.session_state.auth = True
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 5. WORKSPACE PROFESIONAL
    st.markdown("<h2 style='font-family:Bricolage Grotesque; letter-spacing:-1px;'>DASHBOARD.</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 2.5], gap="medium")

    with c1:
        st.markdown("<div class='app-panel'>", unsafe_allow_html=True)
        marca = st.selectbox("LABORATORIO:", ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken"])
        
        with st.expander("📝 FICHA CLIENTE"):
            nom = st.text_input("Nombre")
            obs = st.text_area("Notas")
            if st.button("GUARDAR"):
                st.session_state.db.append({"n": nom, "o": obs})
                st.rerun()
        
        st.markdown("---")
        for item in st.session_state.db:
            st.markdown(f"**{item['n']}**")
            st.caption(item['o'])
        
        if st.button("CERRAR SESIÓN"):
            st.session_state.auth = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='app-panel'>", unsafe_allow_html=True)
        
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if "chat" not in st.session_state: st.session_state.chat = []
            
            for m in st.session_state.chat:
                with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("Escribe tu consulta técnica..."):
                st.session_state.chat.append({"role": "user", "content": p})
                with st.chat_message("user"): st.markdown(p)
                
                # LLAMADA A LA IA
                response = model.generate_content(f"Eres el mejor peluquero del mundo. Marca {marca}. Responde técnico y directo: {p}")
                
                st.session_state.chat.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"): st.markdown(response.text)
                    
        except Exception as e:
            st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
