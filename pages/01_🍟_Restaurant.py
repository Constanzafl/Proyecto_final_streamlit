
import streamlit as st
import pandas as pd


# Define la función colaborativa del filtro
cosine_sim = pd.read_csv('cosine_sim.csv', delimiter=',', header=None)
df4_final = pd.read_parquet("df4_final.parquet")
indices = pd.read_parquet("indices.parquet")

def content_based_recommendations(restaurant, cosine_sim=cosine_sim):
    
    recommended_restaurants = []
    
    idx = indices[indices == restaurant].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    for i in top_10_indexes:
        recommended_restaurants.append(list(df4_final.index)[i])
        
    return recommended_restaurants

restaurants = df4_final.index
# Crear la aplicación de Streamlit
st.title("Sistema de Recomendación de Restaurantes")
st.markdown('Recomienda restaurantes a partir de poner el nombre de un Restaurant')

# Input para seleccionar un restaurante
selected_restaurant = st.selectbox("Selecciona un restaurante:", restaurants)


if st.button("Obtener Recomendaciones"):
    recommendations_content = content_based_recommendations(selected_restaurant)
    st.subheader(f"Recomendaciones basadas en contenido para {selected_restaurant}:")
    

    # Formatea la lista de restaurantes recomendados en Markdown
    formatted_recommendations = "\n".join([f"{i+1}. {restaurant}" for i, restaurant in enumerate(recommendations_content)])
    
    st.markdown(formatted_recommendations)