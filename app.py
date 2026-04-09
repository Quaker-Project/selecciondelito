import streamlit as st
import random

# -----------------------
# CONFIG
# -----------------------

st.set_page_config(page_title="Asignador", page_icon="🎯")

CATEGORIAS = [
    "🚗 Ladrón de vehículo",
    "👜 Carterista",
    "⚖️ Agresor sexual de mujeres"
]

MAX_ALUMNOS = 60
PASSWORD = "profe123"  # 🔑 cámbiala

# -----------------------
# ESTADO
# -----------------------

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {}

if "conteo" not in st.session_state:
    st.session_state.conteo = {cat: 0 for cat in CATEGORIAS}

if "admin" not in st.session_state:
    st.session_state.admin = False

# -----------------------
# FUNCIONES
# -----------------------

def asignar_categoria():
    conteo = st.session_state.conteo
    
    min_valor = min(conteo.values())
    candidatas = [cat for cat, c in conteo.items() if c == min_valor]
    
    categoria = random.choice(candidatas)
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
# LOGIN PROFESOR (OCULTO)
# -----------------------

with st.sidebar:
    st.markdown("### 🔐 Acceso profesor")
    pwd = st.text_input("Contraseña", type="password")
    
    if st.button("Entrar"):
        if pwd == PASSWORD:
            st.session_state.admin = True
            st.success("Modo profesor activado")
        else:
            st.error("Contraseña incorrecta")

# -----------------------
# UI ALUMNO
# -----------------------

st.markdown('<div class="titulo">🎯 Asignación</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Introduce tu nombre y pulsa el botón</div>', unsafe_allow_html=True)

nombre = st.text_input("Nombre")

if st.button("Obtener asignación"):
    
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
        st.error("Se alcanzó el máximo")
    
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
# PANEL PROFESOR
# -----------------------

if st.session_state.admin:
    st.divider()
    st.subheader("📊 Panel del profesor")

    st.write("### Reparto:")
    for cat, num in st.session_state.conteo.items():
        st.write(f"- {cat}: {num}")

    st.write("### Alumnos:")
    st.write(st.session_state.usuarios)

    if st.button("🔄 Resetear todo"):
        st.session_state.usuarios = {}
        st.session_state.conteo = {cat: 0 for cat in CATEGORIAS}
        st.success("Reiniciado")
