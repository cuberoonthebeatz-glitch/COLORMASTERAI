import streamlit as st
import google.generativeai as genai
import random

# 1. CONFIGURACIÓN VISUAL (GUMMY CHIC v2)
st.set_page_config(page_title="ColorMaster Pro", page_icon="🍭", layout="centered")

# CSS para el look "Esponjoso, Moderno y con Contenido"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&family=Quicksand:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif !important;
        background-color: #FEF9F9;
    }
    
    header, footer {visibility: hidden;}
    
    /* Contenedor de Login */
    .login-card {
        background: white;
        padding: 40px;
        border-radius: 40px;
        box-shadow: 0 15px 35px rgba(142, 91, 91, 0.1);
        border: 4px solid #FFF1F1;
        text-align: center;
        margin-top: 20px;
    }

    /* Tipografías Especiales */
    .brand-title {
        font-family: 'Rubik', sans-serif;
        color: #8E5B5B;
        font-size: 45px;
        font-weight: 700;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }

    .welcome-text {
        color: #D4A373;
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 30px;
    }

    .phrase-box {
        background-color: #FFF8F0;
        padding: 15px;
        border-radius: 20px;
        border-left: 5px solid #FFC0CB;
        margin-bottom: 25px;
        font-style: italic;
        color: #6D4C41;
    }

    .news-badge {
        background-color: #E0F2F1;
        color: #00796B;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Botón Gummy */
    .stButton>button {
        background: linear-gradient(135deg, #FFC0CB 0%, #FFB6C1 100%);
        color: #8E5B5B !important;
        border-radius: 30px !important;
        border: none;
        padding: 15px 30px !important;
        font-weight: 700;
        font-size: 18px;
        box-shadow: 0 10px 20px rgba(255, 182, 193, 0.4);
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(255, 182, 193, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE ACCESO Y CONTENIDO DINÁMICO
if 'auth' not in st.session_state:
    st.session_state.auth = False

# Lista de frases curiosas
frases = [
    "“El color es el teclado, los ojos son las armonías, el alma es el piano con muchas cuerdas”.",
    "¿Sabías que el cabello crece unos 1.25 cm al mes? ¡Dales color con cabeza!",
    "La vida es demasiado corta para llevar un pelo aburrido.",
    "Un buen colorista no solo aplica tinte, crea confianza.",
    "El secreto de un rubio perfecto está en el fondo de aclaración, no en el matiz."
]

if not st.session_state.auth:
    # DISEÑO DEL LOGIN REFORM
