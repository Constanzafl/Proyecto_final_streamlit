
import streamlit as st
import pandas as pd


# Define la función colaborativa del filtro
cosine_sim = pd.read_csv('cosine_simpeq.csv', delimiter=',', header=None)
df4_final = pd.read_parquet("df4_final.parquet")
df4_final.reset_index(inplace=True)


# Definir tu función content_based_recommendations
def content_based_recommendations(restaurant, cosine_sim, df):
    recommended_restaurants = []
    
    idx = df[df['name_y'] == restaurant].index[0]
    top_10_indexes = cosine_sim[idx].argsort()[-10:-1]
    recommended_restaurants = df.iloc[top_10_indexes]['name_y'].tolist()
    
    return recommended_restaurants

restaurants = df4_final.name_y
# Crear la aplicación de Streamlit
st.title("Sistema de Recomendación de Restaurantes")
st.markdown('Recomienda restaurantes a partir de poner el nombre de un Restaurant')

# Input para seleccionar un restaurante
selected_restaurant = st.selectbox("Selecciona un restaurante:", restaurants)

if st.button("Obtener Recomendaciones"):
    recommendations_content = content_based_recommendations(selected_restaurant, cosine_sim, df4_final)
    st.subheader(f"Recomendaciones basadas en contenido para {selected_restaurant}:")
    

    # Formatea la lista de restaurantes recomendados en Markdown
    formatted_recommendations = "\n".join([f"{i+1}. {restaurant}" for i, restaurant in enumerate(recommendations_content)])
    
    st.markdown(formatted_recommendations)
    
