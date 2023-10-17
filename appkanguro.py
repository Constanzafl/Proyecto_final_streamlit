import streamlit as st 


st.title('KANGAROO')
st.markdown('*****')
st.markdown('Tu APP web de Recomendación de Restaurants')

logo_path= 'logo.jpeg'
st.image(logo_path, width=300)


if st.checkbox('**Descubre la experiencia Kangaroo**'):
    st.write('Si viajaste a Florida y no sabes donde ir a comer, Kangaroo tiene la solución para vos')


import streamlit as st
import openai
import os

openai.api_key = st.secrets['OPENAI_API_KEY']
#openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("Kanguro ChatGPT!🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

# user input
if user_prompt := st.chat_input("Tu consulta"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})



