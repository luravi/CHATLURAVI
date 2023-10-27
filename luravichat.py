import streamlit as st
import openai
import numpy as np
import matplotlib.pyplot as plt
from streamlit.components.v1 import html
from streamlit_drawable_canvas import st_canvas

# Emojis
emoji_profesor = "👩‍🏫"
emoji_usuario = "🙋"
emoji_robo = "🤖"

# Clave API de OpenAI
openai.api_key = st.secrets["llaveOpenAI"]

# Función para procesar preguntas
def procesar_pregunta(pregunta):
    st.session_state.historial_conversacion.append({"role": "user", "content": pregunta})
    try:
        respuesta_openai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.historial_conversacion,
            max_tokens=15000,
            n=1
        )
        return respuesta_openai['choices'][0]['message']['content']
    except Exception as e:
        st.write(f"Error al obtener respuesta: {e}")
        return None

# Función para mostrar la conversación
def mostrar_conversacion():
    for mensaje in st.session_state.historial_conversacion:
        if mensaje['role'] == 'user':
            st.write(f"{emoji_usuario} Tú: " + mensaje['content'])
        else:
            st.write(f"{emoji_profesor} Profesor: " + mensaje['content'])

# Título y barra lateral
st.title(f'{emoji_profesor} Profesor Virtual de Ciencias')
st.sidebar.markdown(f"<h3 style='text-align: center; font-size: 20px; color: Red'>Profesor Virtual - 2023</h3>", unsafe_allow_html=True)

# Sección de Preguntas
st.write('***')
if 'historial_conversacion' not in st.session_state:
    st.session_state.historial_conversacion = []
pregunta = st.text_input('Escribe tu pregunta')
col1, col2 = st.columns(2)

with col1:
    btn_enviar = st.button("Enviar Pregunta")

with col2:
    btn_limpiar = st.button("Limpiar Conversación")

if btn_enviar:
    respuesta = procesar_pregunta(pregunta)
    if respuesta:
        st.session_state.historial_conversacion.append({"role": "assistant", "content": respuesta})

if btn_limpiar:
    st.session_state.historial_conversacion = []
mostrar_conversacion()

# Sección de Cuestionario
st.write('***')
st.subheader("Cuestionario de Ciencias")
preguntas_cuestionario = [
    {"pregunta": "¿Cuál es el símbolo químico del Oro?", "respuesta": "Au"},
    {"pregunta": "¿Cuántos electrones tiene un átomo de oxígeno?", "respuesta": "8"},
]
respuesta_cuestionario = st.selectbox("Selecciona una pregunta para responder:", [p["pregunta"] for p in preguntas_cuestionario])
respuesta_usuario = st.text_input("Escribe tu respuesta para el cuestionario:")
btn_responder = st.button("Responder")
if btn_responder:
    pregunta_seleccionada = [p for p in preguntas_cuestionario if p["pregunta"] == respuesta_cuestionario][0]
    if respuesta_usuario.lower().strip() == pregunta_seleccionada["respuesta"].lower():
        st.success("¡Correcto!")
    else:
        st.error("Incorrecto. Intenta de nuevo.")

# Sección de Dibujo
st.write('***')
st.subheader("Herramienta de Dibujo:")
canvas_result = st_canvas(fill_color="#000000", stroke_width=5, stroke_color="#FFFFFF", background_color="#000000", height=150, width=700, drawing_mode="freedraw", key="canvas")

# Sección de Gráficos
st.write('***')
st.subheader("Visualización de Gráficos:")
opcion_grafico = st.selectbox("Selecciona un tipo de gráfico:", ["Seno", "Coseno", "Tangente"])
x = np.linspace(0, 10, 100)
if opcion_grafico == "Seno":
    y = np.sin(x)
elif opcion_grafico == "Coseno":
    y = np.cos(x)
elif opcion_grafico == "Tangente":
    y = np.tan(x)
plt.plot(x, y)
st.pyplot(plt)

# Sección de Retroalimentación
st.write('***')
st.subheader("Retroalimentación:")
calificacion = st.slider("Califica la respuesta del profesor:", 0, 10, 5)
btn_calificar = st.button("Enviar Calificación")
if btn_calificar:
    st.write(f"Gracias por calificar la respuesta con un {calificacion}")

# Código para insertar el botón y la imagen en la barra lateral
button_css = """
<style>
    .btn-container {
        display: flex;
        justify-content: center; /* Centra el contenido horizontalmente */
    }
    .btn-custom {
        color: white;
        background-color: #4CAF50;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 1rem;
        margin: 0.25rem;
        cursor: pointer;
        border: none;
        border-radius: 4px;
        width: 90vw;  /* Ajusta según el ancho del dispositivo */
        max-width: 300px;  /* Máximo ancho */
    }
    .btn-custom:hover {
        background-color: #45a049;
    }
</style>
"""

button_html = """
<div class="btn-container">
    <a href="https://chat.openai.com/auth/login" target="_blank" class="btn-custom">Abrir Chat OpenAI</a>
</div>
"""

st.sidebar.markdown(button_css + button_html, unsafe_allow_html=True)

image_url = "https://raw.githubusercontent.com/luravi/CHATLURAVI/github/yo6.jpg"

st.sidebar.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='{image_url}' style='max-width: 100%; height: auto;'>
        <h3 style='font-size: 20px; color: Red; margin-top: 0.5rem;'>Luravi- 2023</h3>
    </div>
    """, 
    unsafe_allow_html=True
)
