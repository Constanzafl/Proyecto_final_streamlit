
import streamlit as st
import pandas as pd

df_content = pd.read_csv('df_content.csv')

# Definir una función para obtener recomendaciones
def get_recommendations(restaurant_name):
    restaurant_row = df_content[df_content['Restaurant_Name'] == restaurant_name]

    # Check if the restaurant was found
    if not restaurant_row.empty:
        recommendations = restaurant_row['Recommendations_content'].iloc[0]
        recommendations_df = pd.DataFrame({'Recommendations': recommendations})
        return recommendations_df
    else:
        return pd.DataFrame()

restaurants = df_content.Restaurant_Name
# Interfaz de usuario de Streamlit
st.title("Recomendaciones de Restaurantes")
restaurant_name = st.selectbox("Selecciona un restaurante:", restaurants)
if st.button("Obtener Recomendaciones"):
    if restaurant_name:
        recommendations_df = get_recommendations(restaurant_name)
        if recommendations_df:
            st.write(f"Recomendaciones para {restaurant_name}:")
            for recommendation_df in recommendations_df:
                st.write(recommendation_df)
        else:
            st.write(f"No se encontraron recomendaciones para {restaurant_name}")
    else:
        st.write("Por favor, ingresa el nombre del restaurante.")


