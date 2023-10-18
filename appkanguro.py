import streamlit as st 
import pandas as pd
import openai
import os
import requests

st.title('KANGAROO')
st.markdown('*****')
st.markdown('Tu APP web de Recomendación de Restaurants')

logo_path= 'logo.jpeg'
st.image(logo_path, width=300)


if st.checkbox('**Descubre la experiencia Kangaroo**'):
    st.write('Si viajaste a Florida y no sabes donde ir a comer, Kangaroo tiene la solución para vos')


openai.api_key = st.secrets['OPENAI_API_KEY']

api_key= st.secrets['API_KEY']


# Crear una función para obtener la latitud y longitud
def obtener_latitud_longitud(direccion):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        latitud = data['results'][0]['geometry']['location']['lat']
        longitud = data['results'][0]['geometry']['location']['lng']
        return latitud, longitud
    else:
        return None

# Interfaz de usuario con Streamlit
st.title("Geocodificación de Direcciones")

direccion = st.text_input("Ingresa tu dirección:")

if st.button("Obtener Latitud y Longitud"):
    if direccion:
        resultado = obtener_latitud_longitud(direccion)
        if resultado:
            latitud, longitud = resultado
            st.write(f'Latitud: {latitud}, Longitud: {longitud}')
        else:
            st.error('No se pudo geocodificar la dirección.')
    else:
        st.warning('Por favor ingresa una dirección antes de obtener la latitud y longitud.')


st.title("Kanguro GPT!🤖")

dataset = pd.read_csv('mini.csv') 


if "messages" not in st.session_state:
    st.session_state.messages = []

# Agrega el contenido del DataFrame al historial de conversación solo una vez
if not st.session_state.get("data_added", False):
    dataset_message = dataset.to_string(index=False) #f"Este es el contenido del DataFrame:\n{}"
    st.session_state.messages.append({"role": "assistant", "content": dataset_message})
    st.session_state.data_added = True


# initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"


# user input
if user_prompt := st.chat_input("Tu consulta"):
    # Agregar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            if "role" not in response.choices[0].delta or response.choices[0].delta["role"] != "assistant":
                # No mostrar el mensaje del asistente si no tiene un rol o si el rol no es "assistant"
                message_placeholder.markdown(full_response + "▌")

        if "role" in response.choices[0].delta and response.choices[0].delta["role"] == "assistant":
            # Mostrar el mensaje del asistente al final
            message_placeholder.markdown(full_response)


















