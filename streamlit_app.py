import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE ÉLITE
st.set_page_config(page_title="ColorMaster Royale", page_icon="✨", layout="wide")

# 2. EL MOTOR DE DISEÑO (CSS DE DISEÑADOR TOP)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Fondo Seda Líquida */
    .stApp {
        background: radial-gradient(circle at top right, #FFF5F7, #F8E1E7, #FDFCFB);
        font-family: 'Outfit', sans-serif;
    }

    /* Ocultar elementos basura de Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    .block-container {padding: 1.5rem 3rem !important;}

    /* El Logo Royale */
    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 75px;
        background: linear-gradient(135deg, #8E5B5B 0%, #D4A373 50%, #B5835A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-style: italic;
        margin-bottom: 0px;
        line-height: 1;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.05));
    }

    /* Tarjetas "Gummy Glass" (Esponjosas pero de cristal) */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 35px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 25px 50px -12px rgba(142, 91, 91, 0.15);
        margin-bottom: 25px;
    }

    /* Botón Maestro */
    .stButton>button {
        background: linear-gradient(135deg, #2D3436 0%, #000000 100%) !important;
        color: #D4A373 !important;
        border-radius: 20px !important;
        border: 1px solid #D4A373 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 1.2rem 2.5rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-5px) !important;
        box-shadow: 0 20px 30px rgba(0,0,0,0.2) !important;
        background: #D4A373 !important;
        color: black !important;
    }

    /* Chat Bubbles Estilizadas */
    .stChatMessage {
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.02) !important;
        background: white !important;
        padding: 15px !important;
    }

    /* Etiquetas de Clientes */
    .client-chip {
        background: white;
        padding: 20px;
        border-radius: 25px;
        border-left: 8px solid #D4A373;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE PERSISTENCIA
if 'auth' not in st.session_state: st.session_state.auth = False
if 'mezclas' not in st.session_state: st.session_state.mezclas = []
if 'clientes' not in st.session_state: st.session_state.clientes = {}

# 4. PANTALLA DE ACCESO "THE CLUB"
if not st.session_state.auth:
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.markdown("<p class='logo-text'>ColorMaster</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:16px; letter-spacing:4px; color:#8E5B5B; margin-top:-10px;'>ROYALE EDITION</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align:center; color:#2D3436;'>SISTEMA DE GESTIÓN INTELIGENTE</h4>", unsafe_allow_html=True)
        api_key = st.text_input("LICENSE KEY", type="password", placeholder="•••• •••• ••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESBLOQUEAR ACCESO"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.auth = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; opacity:0.5; font-size:12px;'>DESARROLLADO PARA ARTISTAS DEL CABELLO v3.0</p>", unsafe_allow_html=True)

else:
    # 5. EL DASHBOARD PROFESIONAL
    st.markdown("<p class='logo-text' style='font-size:40px; text-align:left;'>ColorMaster</p>", unsafe_allow_html=True)
    
    tab_ia, tab_agenda, tab_lab = st.tabs(["⚡ INTELIGENCIA TÉCNICA",
