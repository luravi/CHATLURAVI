import streamlit as st
import openai

emoji_robo = "🤖"
emoji_usuario = "🙋"

# Carga la clave API de OpenAI desde los secretos de Streamlit 
openai.api_key = st.secrets["llaveOpenAI"]

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

def mostrar_conversacion():
    for mensaje in st.session_state.historial_conversacion:
        if mensaje['role'] == 'user':
            st.write(f"{emoji_usuario} Tú: " + mensaje['content'])
        else:
            st.write(f"{emoji_robo} Respuesta del IA: " + mensaje['content'])

st.title(f'{emoji_robo} Pregunta a luravi')
st.write('***')

# Si no existe un historial de conversación, lo inicializamos
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

# Código para insertar el iframe
iframe_code = """
<iframe width="100%" height="600px" src="https://chat.openai.com/auth/login" frameborder="0" allowfullscreen scrolling="yes"></iframe>
"""
st.markdown(iframe_code, unsafe_allow_html=True)

# Información en la barra lateral
st.sidebar.markdown("<h3 style='text-align: center; font-size: 20px; color: Red'>Por luravi- 2023</h3>", unsafe_allow_html=True)
