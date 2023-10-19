import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import pydeck as pdk
import requests

api_key= st.secrets['API_KEY']

ruta2 = "df_only_ubication.csv"
df = pd.read_csv(ruta2)

df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

mejores_por_tendencia = "predicciontendencia.csv"
df_tendencia = pd.read_csv(mejores_por_tendencia)
df_tendencia_unico = df_tendencia

data = df
data = data.drop_duplicates(subset='business_name', keep='first')
restaurantes_df = pd.DataFrame(data)

# Título de la aplicación
st.title('🧐¡Te facilitamos la búsqueda de los Restaurantes mas cercanos!🧐')

logo_path= 'logo.jpeg'
st.image(logo_path, width=200)
# Variables de estado para rastrear si se ha realizado el primer cálculo y la dirección ingresada
primer_calculo = False
address_inicial = ""
    
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
    
direccion = st.text_input("Primero ingresa tu dirección:")

if st.button("Click Aquí"):

    if direccion:
        resultado = obtener_latitud_longitud(direccion)
        if resultado:
            latitud, longitud = resultado
            st.write(f'Latitud: {latitud}, Longitud: {longitud}')   

            lat_usuario, lon_usuario = latitud, longitud

            # Calcular la distancia entre la ubicación del usuario y todos los restaurantes
            restaurantes_df['Distancia'] = restaurantes_df.apply(lambda row: geodesic((lat_usuario, lon_usuario), (row['latitude'], row['longitude'])).meters, axis=1)

            # Ordenar por distancia y seleccionar los 5 más cercanos
            restaurantes_cercanos = restaurantes_df.sort_values(by='Distancia').head(5)

            # Lo mismo, pero con el de mejor tendencia
            df_tendencia_unico['Distancia'] = df_tendencia_unico.apply(lambda row: geodesic((lat_usuario, lon_usuario), (row['latitude'], row['longitude'])).meters, axis=1)

            # Ordenar por distancia y seleccionar los 5 más cercanos
            tendencia_unico = df_tendencia_unico.sort_values(by='Distancia').head(1)

            usuario_df = pd.DataFrame({
                "latitude": [lat_usuario],
                "longitude": [lon_usuario],
                "business_name":["Mi Ubicacion"]
            })

            # Crear el mapa
            st.title("Ubicación de los Restaurantes")

            view_state = pdk.ViewState(
                latitude=lat_usuario,
                longitude=lon_usuario,
                zoom=11,
            )

            # Capa user
            layer_user = pdk.Layer(
                type="ScatterplotLayer",
                data = usuario_df,
                get_position=["longitude", "latitude"],
                get_radius=30,
                get_fill_color=[0, 0, 255], 
                pickable=True,
                auto_highlight=True,
    
            )

            # Capa para los restaurantes
            layer_restaurantes = pdk.Layer(
                type="ScatterplotLayer",
                data=restaurantes_cercanos,
                get_position=["longitude", "latitude"],
                get_radius=30,
                get_fill_color=[0, 255, 0],  
                pickable=True,
                auto_highlight=True, 
            )


            #Carga el rest tendencia unico
            layer_restaurante_unico = pdk.Layer(
                type="ScatterplotLayer",
                data=tendencia_unico,
                get_position=["longitude", "latitude"],
                get_radius=30,
                get_fill_color=[255, 0, 0],  
                pickable=True,
                auto_highlight=True,
            )

            tooltip = {
                "html": "Restaurant: <b>{business_name}</b>",
                "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
            }
            # Mostrar el mapa

            # Crear el mapa PyDeck principal y agregar la capa de restaurantes
            mapa_pydeck = pdk.Deck(
                layers=[layer_restaurantes, layer_user, layer_restaurante_unico],
                initial_view_state=view_state,
                tooltip=tooltip,
                    views=[
                        pdk.View(type="MapView", controller=True, legend="Restaurantes Cercanos")
                    ]
            )

            # Mostrar el mapa
            st.pydeck_chart(mapa_pydeck)

            def mostrar_leyenda():
                st.markdown("#### Leyenda")
                st.write(":large_blue_circle: Tu ubicación")
                st.write(":large_green_circle: Restaurantes cercanos")
                st.write(":red_circle: Restaurante recomendado")

            mostrar_leyenda()

            lat_usuario = usuario_df["latitude"].values[0]
            lon_usuario = usuario_df["longitude"].values[0]

            # Función para calcular la distancia y generar el enlace de Google Maps
            def calculate_distance_and_generate_link(row):
                lat_restaurante = row['latitude']
                lon_restaurante = row['longitude']
                enlace = f"https://www.google.com/maps/dir/{lat_usuario},{lon_usuario}/{lat_restaurante},{lon_restaurante}"
                return enlace

            restaurantes_cercanos['Enlace a Google Maps'] = restaurantes_cercanos.apply(calculate_distance_and_generate_link, axis=1)

            enlaces_html = restaurantes_cercanos['Enlace a Google Maps'].apply(lambda enlace: f'<a target="_blank" href="{enlace}">Ver en Google Maps</a>')

            restaurantes_cercanos['Enlace HTML'] = enlaces_html

            restaurantes_cercanos_googlemaps = restaurantes_cercanos.loc[:,["business_name", "Distancia", "Enlace HTML"]]
            restaurantes_cercanos_googlemaps = restaurantes_cercanos_googlemaps.rename(columns={'business_name': 'Nombre Restaurant', 'Distancia':'Distancia en Metros','Enlace HTML':'Indicaciones'})

            st.header("Restaurantes Cercanos")
            st.write(restaurantes_cercanos_googlemaps.to_html(escape=False, index=False), unsafe_allow_html=True)

            #codigo para rest unico
            tendencia_unico['Enlace a Google Maps'] = tendencia_unico.apply(calculate_distance_and_generate_link, axis=1)

            enlaces_html_unico = tendencia_unico['Enlace a Google Maps'].apply(lambda enlace: f'<a target="_blank" href="{enlace}">Ver en Google Maps</a>')

            tendencia_unico['Enlace HTML'] = enlaces_html_unico

            df_tendencia_unico_googlemaps = tendencia_unico.loc[:,["business_name", "Distancia", "Enlace HTML"]]
            df_tendencia_unico_googlemaps = df_tendencia_unico_googlemaps.rename(columns={'business_name': 'Nombre Restaurant', 'Distancia':'Distancia en Metros','Enlace HTML':'Indicaciones'})

            st.header("")
            st.header("")
            st.header("Lo que se viene:")
            st.write("Aqui podras ver cual Restaurant tiene una tendencia positiva")
            st.write(df_tendencia_unico_googlemaps.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.error('No se encontraron coordenadas para la dirección ingresada.')
    else:
        st.warning('Ingrese una dirección válida.')