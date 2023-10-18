
import streamlit as st
import pandas as pd

df_content = pd.read_csv('df_content.csv')

# Definir una función para obtener las recomendaciones
def get_recommendations(restaurant_name):
    restaurant_row = df_content[df_content['Restaurant_Name'] == restaurant_name]

    if not restaurant_row.empty:
        recommendations = restaurant_row['Recommendations_content'].iloc[0]
        # Dividir las recomendaciones por líneas o cualquier otro separador
        recommendations_list = recommendations.split('\n')  # Cambia el separador según corresponda

        # Crear una lista de diccionarios
        recommendations_dict_list = [{'Recommendations': rec} for rec in recommendations_list]

        recommendations_df = pd.DataFrame(recommendations_dict_list)
        return recommendations_df
    else:
        return pd.DataFrame()
       
restaurants = df_content.Restaurant_Name

st.title('Recomendaciones de Restaurantes')


restaurant_name = st.selectbox("Selecciona un restaurante:", restaurants)
recommendations_df1 = get_recommendations(restaurant_name)

if not recommendations_df1.empty:
    st.write('Recomendaciones para el restaurante:', restaurant_name)
    st.write(recommendations_df1)
else:
    st.write('No se encontraron recomendaciones para el restaurante especificado.')