import streamlit as st
import random

# -----------------------
# CONFIG
# -----------------------

st.set_page_config(page_title="Asignador de Categorías", page_icon="🎯")

categorias = [
    "🚗 Ladrón de vehículo",
    "👜 Carterista",
    "⚖️ Agresor sexual de mujeres"
]

MAX_ALUMNOS = 60

# -----------------------
# ESTADO
# -----------------------

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}

if "conteo" not in st.session_state:
    st.session_state.conteo = {cat: 0 for cat in categorias}

# -----------------------
# FUNCIONES
# -----------------------

def asignar_categoria():
    conteo = st.session_state.conteo
    
    # Encontrar mínimo
    min_valor = min(conteo.values())
    
    # Categorías menos usadas
    candidatas = [cat for cat, c in conteo.items() if c == min_valor]
    
    # Elegir aleatoriamente entre las menos usadas
    categoria = random.choice(candidatas)
    
    # Actualizar conteo
    st.session_state.conteo[categoria] += 1
    
    return categoria


def color_categoria(cat):
    if "vehículo" in cat:
        return "#2563eb"
    elif "Carterista" in cat:
        return "#059669"
    else:
        return "#dc2626"

# -----------------------
# ESTILO
# -----------------------

st.markdown("""
<style>
.titulo {
    text-align:center;
    font-size:36px;
    font-weight:bold;
}
.subtitulo {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# UI
# -----------------------

st.markdown('<div class="titulo">🎯 Asignador de Categorías</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Cada alumno solo puede obtener una</div>', unsafe_allow_html=True)

nombre = st.text_input("Introduce tu nombre")

if st.button("Obtener categoría"):
    
    if not nombre.strip():
        st.warning("Introduce tu nombre")
    
    elif nombre in st.session_state.usuarios:
        categoria = st.session_state.usuarios[nombre]
        
        color = color_categoria(categoria)
        st.markdown(f"""
        <div style="background:{color};padding:25px;border-radius:14px;color:white;text-align:center;font-size:26px;">
        Ya tienes asignado:<br>{categoria}
        </div>
        """, unsafe_allow_html=True)
    
    elif len(st.session_state.usuarios) >= MAX_ALUMNOS:
        st.error("Se alcanzó el máximo de alumnos")
    
    else:
        categoria = asignar_categoria()
        st.session_state.usuarios[nombre] = categoria
        
        color = color_categoria(categoria)
        st.markdown(f"""
        <div style="background:{color};padding:25px;border-radius:14px;color:white;text-align:center;font-size:26px;">
        Tu categoría es:<br>{categoria}
        </div>
        """, unsafe_allow_html=True)

# -----------------------
# INFO
# -----------------------

st.divider()

st.write(f"👥 Asignados: {len(st.session_state.usuarios)} / {MAX_ALUMNOS}")

st.write("📊 Reparto actual:")
for cat, num in st.session_state.conteo.items():
    st.write(f"- {cat}: {num}")
