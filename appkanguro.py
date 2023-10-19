import streamlit as st 
import pandas as pd
import openai
import os
import requests
from geopy.distance import geodesic

st.title('🦘Kangaroo: la APP WEB de Recomendacion de Restaurantes en Florida🦘')

logo_path= 'logo.jpeg'
st.image(logo_path, width=200)


st.write('🏖️Si estás en Florida y no sabes donde ir a comer, Kangaroo tiene la solución para vos🏖️')


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
    

# Definir el radio de 2 km
radio_km = 2
resumen_dfcompleto= pd.read_csv('ResumenDFparaCHATopenai.csv')

# Interfaz de usuario con Streamlit
st.title("¡Te damos la bienvenida a nuestra APP interactiva!")

direccion = st.text_input("Primero ingresa tu dirección:")

if st.button("Click Aquí"):
    if direccion:
        resultado = obtener_latitud_longitud(direccion)
        if resultado:
            latitud, longitud = resultado
            st.write(f'Latitud: {latitud}, Longitud: {longitud}')   
        else:
            st.error('No se pudo geocodificar la dirección.')
    else:
        st.warning('Por favor ingresa una dirección antes de obtener la latitud y longitud.')
# Función para filtrar lugares dentro del radio especificado
def filtrar_lugares_cercanos(resumen_dfcompleto, lat_user, lon_user, radio_km):
    def calcular_distancia(row):
        lugar_lat = row['latitude_x']
        lugar_lon = row['longitude_x']
        distancia = geodesic((lat_user, lon_user), (lugar_lat, lugar_lon)).kilometers
        return distancia
    resumen_dfcompleto['distancia'] = resumen_dfcompleto.apply(calcular_distancia, axis=1)
    lugares_cercanos2 = resumen_dfcompleto[resumen_dfcompleto['distancia'] <= radio_km]

    return lugares_cercanos2

if 'latitud' in locals() and 'longitud' in locals():  

            st.title("Kanguro GPT!🤖")
            st.markdown('¡Ahora preguntame lo que quieras! Estoy para ayudarte 🤗')

            # Filtrar los lugares dentro del radio especificado
            lugares_cercanos2 = filtrar_lugares_cercanos(resumen_dfcompleto, latitud, longitud, radio_km)
            dataset = lugares_cercanos2
            
            dataset_message = dataset.to_string(index=False) #f"Este es el contenido del DataFrame:\n{}"
            st.session_state.messages.append({"role": "assistant", "content": dataset_message})
                        
if "messages" not in st.session_state:
    st.session_state.messages = []

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





















