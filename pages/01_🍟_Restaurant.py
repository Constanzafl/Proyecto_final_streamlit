
import streamlit as st
import pandas as pd

df_content = pd.read_csv('df_content.csv')

# Definir una función para obtener las recomendaciones
def get_recommendations(restaurant_name):
    restaurant_row = df_content[df_content['Restaurant_Name'] == restaurant_name]

    if not restaurant_row.empty:
        recommendations = restaurant_row['Recommendations_content'].iloc[0]# Cambia el separador según corresponda
        recommendations_df = pd.DataFrame({'Recommendations': recommendations}, index=False)
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