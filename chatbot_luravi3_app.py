# app.py
import streamlit as st 
import os 
import openai

emoji_robo = "🤖"
emoji_usuario = "🙋"

# Carga la clave API de OpenAI desde una variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title(f'{emoji_robo} Pregunta a Luravi')
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
    st.session_state.historial_conversacion.append({"role": "user", "content": pregunta})
    retorno_openai = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = st.session_state.historial_conversacion,
        max_tokens = 15000,
        n=1
    )
    st.session_state.historial_conversacion.append(
        {"role": "assistant", 
         "content": retorno_openai['choices'][0]['message']['content']})
    
if btn_limpiar: 
    st.session_state.historial_conversacion = []
    pregunta = ''

if len(st.session_state.historial_conversacion) > 0:
    for i in range(len(st.session_state.historial_conversacion)):
        if i % 2 == 0:
            with st.container():
                st.write(f"{emoji_usuario} Tú: " + st.session_state.historial_conversacion[i]['content'])
        else:
            with st.container():
                st.write(f"{emoji_robo} Respuesta del IA: " + st.session_state.historial_conversacion[i]['content'])

# Código para insertar el iframe
iframe_code = """
<iframe width="100%" height="600px" src="https://chat.openai.com/auth/login" frameborder="0" allowfullscreen scrolling="yes"></iframe>
"""
st.markdown(iframe_code, unsafe_allow_html=True)

# Información en la barra lateral
st.sidebar.markdown("<h3 style='text-align: center; font-size: 20px; color: Red'>Por by LURAVI- 2023</h3>", unsafe_allow_html=True)

