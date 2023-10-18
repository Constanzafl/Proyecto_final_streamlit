import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pydeck as pdk

# Define el usuario agente para Geopy
geolocator = Nominatim(user_agent="mi_app_geopy")

# Carga los datos del parquet y el parquet con los restaurantes mejor puntuados (?)
#ruta = "FINAL_FLORIDA.parquet"
#df = pd.read_parquet(ruta)

ruta2 = "df_only_ubication.csv"
df = pd.read_csv(ruta2)

#mejores_por_tendencia = "predicciontendencia.parquet"
#df_tendencia = pd.read_parquet(mejores_por_tendencia)

#df_tendencia_unico = df_tendencia.drop_duplicates(subset="business_name", keep='first')

mejores_por_tendencia = "predicciontendencia2.parquet"
df_tendencia = pd.read_parquet(mejores_por_tendencia)
df_tendencia_unico = df_tendencia

# Asegurémonos de que las columnas sean números
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# Crea un DataFrame con restaurantes y sus coordenadas
data = df
data = data.drop_duplicates(subset='business_name', keep='first')
restaurantes_df = pd.DataFrame(data)

# Título de la aplicación
st.title('Geocodificación y búsqueda de restaurantes cercanos')

# Entrada de usuario para ingresar una dirección
address = st.text_input('Ingrese una dirección:')

# Variables de estado para rastrear si se ha realizado el primer cálculo y la dirección ingresada
primer_calculo = False
address_inicial = ""


# Botón para geocodificar la dirección
if st.button('Geocodificar'):
    address_inicial = address
    if address:
        location = geolocator.geocode(address)
        if location:
            lat_usuario, lon_usuario = location.latitude, location.longitude

            # Calcular la distancia entre la ubicación del usuario y todos los restaurantes
            restaurantes_df['Distancia'] = restaurantes_df.apply(lambda row: geodesic((lat_usuario, lon_usuario), (row['latitude'], row['longitude'])).meters, axis=1)

            # Ordenar por distancia y seleccionar los 5 más cercanos
            restaurantes_cercanos = restaurantes_df.sort_values(by='Distancia').head(5)

            # Mostrar los 5 restaurantes más cercanos
            st.write('Los 5 restaurantes más cercanos a tu ubicación:')
            st.dataframe(restaurantes_cercanos[['business_name', 'Distancia']])


            # Lo mismo, pero con el de mejor tendencia
            df_tendencia_unico['Distancia'] = df_tendencia_unico.apply(lambda row: geodesic((lat_usuario, lon_usuario), (row['latitude'], row['longitude'])).meters, axis=1)

            # Ordenar por distancia y seleccionar los 5 más cercanos
            tendencia_unico = df_tendencia_unico.sort_values(by='Distancia').head(2)

            # Mostrar los 5 restaurantes más cercanos
            st.write('El restaurante Tendencia mas cercano, es:')
            st.dataframe(tendencia_unico[['business_name', 'Distancia', "longitude", "latitude"]])


            usuario_df = pd.DataFrame({
                "latitude": [lat_usuario],
                "longitude": [lon_usuario]
            })

            st.dataframe(df_tendencia_unico)

            st.dataframe(restaurantes_cercanos)

            st.write(df_tendencia_unico.dtypes)
            st.write(restaurantes_cercanos.dtypes)

            # Crear el mapa
            st.title("Mapa Personalizado")

            view_state = pdk.ViewState(
                latitude=lat_usuario,
                longitude=lon_usuario,
                zoom=10,
            )

            # Capa user
            layer_user = pdk.Layer(
                type="ScatterplotLayer",
                data = usuario_df,
                get_position=["longitude", "latitude"],
                get_radius=300,
                get_fill_color=[0, 0, 255], 
                pickable=True,
                auto_highlight=True,
            )

            # Capa para los restaurantes
            layer_restaurantes = pdk.Layer(
                type="ScatterplotLayer",
                data=restaurantes_cercanos,
                get_position=["longitude", "latitude"],
                get_radius=300,
                get_fill_color=[0, 255, 0],  
                pickable=True,
                auto_highlight=True,
            )



            data = pd.DataFrame({
                "latitude": [40.7228, 40.7129, 40.7130, 40.6931],
                "longitude": [-74.0060, -74.0061, -74.0062, -74.0163],
                "location_name": ["Ubicación 1", "Ubicación 2", "Ubicación 3", "Ubicación 4"],
            })


            # Capa el rest tendencia unico
            # layer_restaurante_unico = pdk.Layer(
            #     type="ScatterplotLayer",
            #     data=tendencia_unico,
            #     get_position=["longitude", "latitude"],
            #     get_radius=300,
            #     get_fill_color=[0, 255, 0],  
            #     pickable=True,
            #     auto_highlight=True,
            # )

            # Mostrar el mapa

            # Crear el mapa PyDeck principal y agregar la capa de restaurantes
            mapa_pydeck = pdk.Deck(
                layers=[layer_restaurantes, layer_user], #layer_restaurante_unico],
                initial_view_state=view_state
            )

            # Mostrar el mapa
            st.pydeck_chart(mapa_pydeck)

        else:
            st.error('No se encontraron coordenadas para la dirección ingresada.')
    else:
        st.warning('Ingrese una dirección válida.')



#direccion de prueba: 935 W Okeechobee Rd, Hialeah, FL 33010, Estados Unidos