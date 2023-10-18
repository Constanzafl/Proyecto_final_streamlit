
import streamlit as st
import pandas as pd

df_content = pd.read_csv('df_content.csv')

# Definir una función para obtener recomendaciones
def get_recommendations(restaurant_name):
    # Encuentra la fila donde el nombre del restaurante coincida con la entrada
    restaurant_row = df_content[df_content['Restaurant_Name'] == restaurant_name]

    # Obtén las recomendaciones del restaurante
    recommendations = restaurant_row['Recommendations_content'].to_list()
    
    return recommendations

restaurants = df_content.Restaurant_Name
# Interfaz de usuario de Streamlit
st.title("Recomendaciones de Restaurantes")
restaurant_name = st.selectbox("Selecciona un restaurante:", restaurants)
if st.button("Obtener Recomendaciones"):
    if restaurant_name:
        recommendations = get_recommendations(restaurant_name)
        if recommendations:
            st.write(f"Recomendaciones para {restaurant_name}:")
            for recommendation in recommendations:
                st.write(recommendation)
        else:
            st.write(f"No se encontraron recomendaciones para {restaurant_name}")
    else:
        st.write("Por favor, ingresa el nombre del restaurante.")



