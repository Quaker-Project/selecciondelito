import streamlit as st
import random

# -----------------------
# CONFIGURACIÓN INICIAL
# -----------------------

st.set_page_config(page_title="Asignador de Categorías", page_icon="🎯", layout="centered")

categorias = [
    "🚗 Ladrón de vehículo",
    "👜 Carterista",
    "⚖️ Agresor sexual de mujeres"
]

TOTAL_ALUMNOS = 50

# -----------------------
# FUNCIONES
# -----------------------

def generar_asignaciones(num_alumnos, categorias):
    num_categorias = len(categorias)
    base = num_alumnos // num_categorias
    resto = num_alumnos % num_categorias

    asignaciones = []

    for i, categoria in enumerate(categorias):
        cantidad = base + (1 if i < resto else 0)
        asignaciones.extend([categoria] * cantidad)

    random.shuffle(asignaciones)
    return asignaciones

# -----------------------
# ESTADO
# -----------------------

if "asignaciones" not in st.session_state:
    st.session_state.asignaciones = generar_asignaciones(TOTAL_ALUMNOS, categorias)

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}  # nombre -> categoría

# -----------------------
# ESTILO VISUAL
# -----------------------

st.markdown("""
    <style>
    .titulo {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitulo {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }
    .resultado {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# INTERFAZ
# -----------------------

st.markdown('<div class="titulo">🎯 Asignador de Categorías</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Introduce tu nombre y recibe tu caso</div>', unsafe_allow_html=True)

nombre = st.text_input("Nombre del alumno")

# -----------------------
# BOTÓN DE ASIGNACIÓN
# -----------------------

if st.button("Obtener categoría"):
    
    if not nombre.strip():
        st.warning("Por favor, introduce tu nombre")
    
    elif nombre in st.session_state.usuarios:
        categoria = st.session_state.usuarios[nombre]
        st.markdown(f'<div class="resultado">Ya tienes asignado:<br>{categoria}</div>', unsafe_allow_html=True)
    
    elif len(st.session_state.asignaciones) == 0:
        st.error("No quedan categorías disponibles")
    
    else:
        categoria = st.session_state.asignaciones.pop()
        st.session_state.usuarios[nombre] = categoria
        
        st.markdown(f'<div class="resultado">Tu categoría es:<br>{categoria}</div>', unsafe_allow_html=True)

# -----------------------
# INFO EXTRA
# -----------------------

st.divider()

st.write(f"👥 Alumnos asignados: {len(st.session_state.usuarios)} / {TOTAL_ALUMNOS}")
st.write(f"📦 Categorías restantes: {len(st.session_state.asignaciones)}")

# Opcional: ver lista (solo profesor)
with st.expander("🔒 Ver asignaciones (profesor)"):
    st.write(st.session_state.usuarios)
