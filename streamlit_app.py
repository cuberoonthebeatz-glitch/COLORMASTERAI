import streamlit as st
import google.generativeai as genai
import random

# 1. CONFIGURACIÓN DE ALTO NIVEL
st.set_page_config(page_title="ColorMaster Ultra Pro", page_icon="🎨", layout="wide")

# CSS: ENERGÍA, EMOCIÓN Y CERO ESPACIOS BLANCOS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Quicksand:wght@400;600&display=swap');
    
    /* Fondo con energía */
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #FDE2E4 100%);
    }
    
    /* Adiós espacios muertos */
    .block-container {padding: 1rem 2rem !important;}
    header {visibility: hidden;}
    
    /* Títulos con CHICHA */
    .hero-title {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(to right, #D4A373, #8E5B5B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
    }
    
    /* Tarjetas Esponjosas y con Volumen */
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 25px;
        border: 2px solid #FFFFFF;
        box-shadow: 0 15px 35px rgba(255, 182, 193, 0.3);
        margin-bottom: 20px;
    }
    
    /* Botones con Energía */
    .stButton>button {
        background: linear-gradient(135deg, #FF99AC 0%, #FF6B8B 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        padding: 15px 40px !important;
        box-shadow: 0 10px 20px rgba(255, 107, 139, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 15px 25px rgba(255, 107, 139, 0.4) !important;
    }

    /* Estilo de las fichas */
    .client-card {
        background: #FFFFFF;
        border-left: 10px solid #FF99AC;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS (Mezclas y Clientes)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'mezclas' not in st.session_state: st.session_state.mezclas = []
if 'clientes' not in st.session_state: st.session_state.clientes = {}

# 3. PANTALLA DE LOGIN (IDENTIDAD TOTAL)
if not st.session_state.auth:
    st.markdown("<h1 class='hero-title'>COLORMASTER ULTRA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px; color:#8E5B5B;'>La herramienta definitiva para el artista del color</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🔑 Iniciar Sesión Prof")
        api_input = st.text_input("Introduce tu Licencia:", type="password")
        if st.button("ACCEDER AL PODER ✨"):
            if api_input:
                st.session_state.api_key = api_input
                st.session_state.auth = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style='text-align:center; margin-top:30px;'>
                <span style='background:#FFD1DC; padding:10px 20px; border-radius:20px; color:#C71585; font-weight:700;'>
                    🔥 NOVEDAD: ¡Gestión de Clientes y Mezclas ya disponible!
                </span>
            </div>
        """, unsafe_allow_html=True)

else:
    # 4. INTERFAZ DE TRABAJO (TRES SECCIONES)
    tab1, tab2, tab3 = st.tabs(["💬 CONSULTORÍA IA", "🧪 LABORATORIO MEZCLAS", "👤 AGENDA CLIENTES"])

    # --- TAB 1: CONSULTORÍA ---
    with tab1:
        col_side, col_main = st.columns([1, 3])
        with col_side:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            marca = st.selectbox("Marca:", ["L'Oréal Pro", "Wella", "Schwarzkopf", "Redken", "Casmara", "Otra"])
            modo = st.radio("Enfoque:", ["Colorimetría", "Estética", "Tricología"])
            if st.button("Cerrar Sesión"):
                st.session_state.auth = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col_main:
            st.markdown(f"## 🪄 Modo {modo}")
            try:
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                if "msg" not in st.session_state: st.session_state.msg = []
                
                for m in st.session_state.msg:
                    with st.chat_message(m["role"]): st.markdown(m["content"])

                if p := st.chat_input("Pregúntale a tu experto..."):
                    st.session_state.msg.append({"role": "user", "content": p})
                    with st.chat_message("user"): st.markdown(p)
                    
                    with st.spinner("Creando tu fórmula perfecta..."):
                        r = model.generate_content(f"Experto en {marca} y {modo}: {p}")
                    
                    with st.chat_message("assistant"):
                        st.markdown(r.text)
                        st.session_state.msg.append({"role": "assistant", "content": r.text})
            except Exception as e:
                st.error(f"Error: {e}")

    # --- TAB 2: MEZCLAS ---
    with tab2:
        st.markdown("## 🧪 Mis Fórmulas Maestras")
        c1, c2 = st.columns(2)
        with c1:
            nombre_mezcla = st.text_input("Nombre de la Mezcla (ej: Rubio Nórdico Pepita)")
            formula = st.text_area("Escribe la fórmula aquí...")
            if st.button("Guardar Mezcla"):
                st.session_state.mezclas.append({"nombre": nombre_mezcla, "formula": formula})
                st.success("¡Fórmula guardada!")
        with c2:
            st.markdown("### Historial de Mezclas")
            for m in st.session_state.mezclas:
                with st.expander(m['nombre']):
                    st.write(m['formula'])

    # --- TAB 3: CLIENTES ---
    with tab3:
        st.markdown("## 👤 Agenda de Clientes VIP")
        with st.form("nuevo_cliente"):
            c_nom = st.text_input("Nombre de la Cliente")
            c_ale = st.text_input("Alergias / Sensibilidades")
            c_gus = st.text_area("Gustos y Notas Especiales (ej: No le gusta el dorado)")
            if st.form_submit_button("Añadir a la Agenda"):
                st.session_state.clientes[c_nom] = {"alergias": c_ale, "notas": c_gus}
                st.success(f"{c_nom} añadida con éxito.")
        
        st.markdown("---")
        st.markdown("### Mis Clientes")
        for nombre, datos in st.session_state.clientes.items():
            st.markdown(f"""
            <div class='client-card'>
                <h4>🌸 {nombre}</h4>
                <p><b>⚠️ Alergias:</b> {datos['alergias']}</p>
                <p><b>📝 Notas:</b> {datos['notas']}</p>
            </div>
            """, unsafe_allow_html=True)
