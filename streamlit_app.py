import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL (GUMMY CHIC)
st.set_page_config(page_title="ColorMaster Pro", page_icon="🍭", layout="centered")

# CSS para el look "Esponjoso y Moderno"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif !important;
        background-color: #FEF9F9; /* Fondo rosa nube muy suave */
    }
    
    header, footer {visibility: hidden;}
    
    /* Efecto Esponjoso General */
    .gummy-element {
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(142, 91, 91, 0.1); /* Sombra suave y difuminada */
        border: 2px solid #FFF1F1;
        transition: transform 0.2s ease-in-out;
    }
    
    .gummy-element:hover {
        transform: translateY(-2px);
    }
    
    /* Login Box Gummy */
    .login-container {
        max-width: 400px;
        margin: 80px auto;
        padding: 30px;
        background: white;
        border-radius: 30px;
        box-shadow: 0 10px 20px rgba(142, 91, 91, 0.15);
        text-align: center;
        border: 3px solid #FADADD; /* Rosa palo suave */
    }
    
    /* Títulos Diferentes */
    .main-title {
        color: #8E5B5B;
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 5px;
    }
    
    .subtitle {
        color: #D4A373; /* Dorado suave */
        font-weight: 400;
        font-size: 18px;
        margin-bottom: 25px;
        font-style: italic;
    }
    
    /* Botones Gummy (Vibrantes pero soft) */
    .stButton>button {
        background: linear-gradient(135deg, #FFC0CB 0%, #FFB6C1 100%); /* Rosa chicle suave */
        color: #8E5B5B !important;
        border-radius: 25px !important;
        border: none;
        padding: 12px 30px !important;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 5px 10px rgba(255, 182, 193, 0.4);
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 7px 14px rgba(255, 182, 193, 0.5);
    }
    
    /* Inputs Rounded */
    .stTextInput>div>div>input {
        border-radius: 20px;
        border: 2px solid #FADADD;
        padding: 10px;
    }
    
    /* Chat Messages Gummy */
    .stChatMessage {
        border-radius: 20px !important;
        margin-bottom: 12px;
        border: 1px solid #FFF1F1 !important;
        box-shadow: 0 4px 8px rgba(142, 91, 91, 0.05);
    }
    
    /* Estilo barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #FFF1F1 !important;
        border-right: 2px solid #FADADD;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE ACCESO GUMMY
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3465/3465066.png", width=70)
    st.markdown("<p class='main-title'>ColorMaster Pro</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Tu rincón dulce de creatividad</p>", unsafe_allow
