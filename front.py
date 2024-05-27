# Frontend del chatbot
# Importamos librerias necesarias
import streamlit as st
from chatbot import predict_class, get_response, intents
from database import get_data_orders
import re

# Configuración de la página
st.set_page_config(page_title="Aidly Chatbot", page_icon="🤖", layout="wide")
st.title("Soporte :blue[Dtech]")
st.header("¡Hola! Soy _Aidly_, tu asistente virtual 👩🏻‍💻. :blue[¿Charlamos?]", divider = 'rainbow')

# Inicialización de variables de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True 

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("¡Hola!, ¿Cómo puedo ayudarte hoy?")
    
    st.session_state.messages.append({"role": "assistant", "content": "¡Hola!, ¿Cómo puedo ayudarte hoy?"})
    st.session_state.first_message = False

if prompt := st.chat_input("Escribe aquí tu mensaje..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if re.search(r"pedido\s+(\d+)", prompt, re.IGNORECASE):
        id_pedido = re.findall(r"pedido\s+(\d+)", prompt, re.IGNORECASE)[0]
        res = get_data_orders(int(id_pedido))
        st.session_state.messages.append({"role": "assistant", "content": res})

    else:
        ints = predict_class(prompt)
        res = get_response(ints, intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

