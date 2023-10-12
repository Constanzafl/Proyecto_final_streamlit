import streamlit as st 


st.title('KANGAROO')
st.markdown('*****')
st.markdown('Tu APP web de Recomendación de Restaurants')

logo_path= 'logo.jpeg'
st.image(logo_path, width=300)


if st.checkbox('**Descubre la experiencia Kangaroo**'):
    st.write('Si viajaste a Florida y no sabes donde ir a comer, Kangaroo tiene la solución para vos')






