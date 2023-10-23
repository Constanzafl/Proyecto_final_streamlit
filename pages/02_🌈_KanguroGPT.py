import streamlit as st 
import pandas as pd
import openai
import requests
from geopy.distance import geodesic
from utils.chatfuncions import get_response, check_memory_tokens, num_tokens, system_role

st.title("¡CHARLEMOS!")

logo_path= 'logo.jpeg'
st.image(logo_path, width=200)
st.title("Kanguro GPT!🤖")
st.markdown('¡Ahora preguntame lo que quieras! Estoy para ayudarte 🤗')

openai.api_key = st.secrets['OPENAI_API_KEY']

api_key= st.secrets['API_KEY']



resumen_dfcompleto= pd.read_csv('ResumenDFparaCHATopenai.csv')

# Inicializa st.session_state con una estructura de datos que contenga las conversaciones

direccion = st.text_input("Ingresa tu dirección:")
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

if direccion:
        resultado = obtener_latitud_longitud(direccion)
        if resultado:
            latitud, longitud = resultado
            st.write(f'Latitud: {latitud}, Longitud: {longitud}')
        else:
            st.error('No se pudo geocodificar la dirección.')

# Definir el radio de 2 km
radio_km = 3

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
    # Filtrar los lugares dentro del radio especificado
    lugares_cercanos2 = filtrar_lugares_cercanos(resumen_dfcompleto, latitud, longitud, radio_km)
    # Ahora puedes continuar con el procesamiento de 'lugares_cercanos2'
else:
    # Indicar al usuario que primero debe ingresar la dirección y obtener la latitud y longitud.
    st.warning('Por favor, ingresa una dirección y obtén la latitud y longitud antes de continuar.')


if "messages" not in st.session_state:
    st.session_state.messages = []

# Agrega el contenido del DataFrame al historial de conversación solo una vez
if not st.session_state.get("data_added", False)and 'lugares_cercanos2' in locals():
    dataset_message = f"Este es el contenido del DataFrame:\n{lugares_cercanos2.to_string(index=False)}"
    st.session_state.messages.append({"role": "assistant", "content": dataset_message})
    st.session_state.data_added = True

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
        
        
         # Consultamos al chat
        full_response = get_response(st.session_state.messages)

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # chequeamos la cantidad de tokens en la memoria
    st.session_state.messages = check_memory_tokens(st.session_state.messages)
        
        
        
        
        #full_response = ""

        #for response in openai.ChatCompletion.create(
            #model=st.session_state.model,
            #messages=[
                #{"role": m["role"], "content": m["content"]}
                #for m in st.session_state.messages
            #],
            #stream=True,
        #):
            #full_response += response.choices[0].delta.get("content", "")
            #if "role" not in response.choices[0].delta or response.choices[0].delta["role"] != "assistant":
                # No mostrar el mensaje del asistente si no tiene un rol o si el rol no es "assistant"
                #message_placeholder.markdown(full_response + "▌")

        #if "role" in response.choices[0].delta and response.choices[0].delta["role"] == "assistant":
            # Mostrar el mensaje del asistente al final
            #message_placeholder.markdown(full_response)







