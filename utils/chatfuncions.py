import streamlit as st
import tiktoken
import openai


openai.api_key = st.secrets['OPENAI_API_KEY']



GPT_MODEL = "gpt-3.5-turbo"
TOKEN_BUDGET = 3000

# configuracion del system
system = """ Eres un asistente especializado en recomendacion de restaurantes en el estado de Florida, especificamente en la direccion que ingresa el usuario.
    - Responde sobre sitios que aparecen unicamente en el dataframe que se obtiene luego de colocar la direccion y filtrar por latitud y longitud los datos.
    Se le proporcionarán consultas sobre que sitios son mejores para comer cierto tipo de alimento. 
    - Si la comida que el usuario busca no se encuentra dentro de los datos proporcionados, responder que no se encuentra la informacion solicitada y brindar la opcion de preguntar sobre otro tipo de comida. 
    - Si la respuesta no esta en la información proporcionada, responde: "No tengo datos para responder su pregunta"
    - Si el usuario pregunta por algo que no esta relacionado a restaurantes, responde: "soy un asistente para responder preguntas de restaurantes, no tengo la información solicitada en mi base de datos" 
    - No repitas dos veces la misma informacion, excepto que el usuario te vuelva a preguntar lo mismo. 
      
     """

system_role = [{"role": "system", "content":system}]

# Para calcular el numero de tokens
def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def get_response(memory:list):
    response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages= system_role + memory,
            temperature = 0.2)
    return response.choices[0].message["content"]

def check_memory_tokens(memory:list):
    # Verificar la cantidad de tokens en los mensajes acumulados

    total_tokens = sum(num_tokens(message['content']) for message in memory) + num_tokens(system)
    # Comparamos el total de tokens con el budget
    if total_tokens > TOKEN_BUDGET:
        # Borrar las primeras interacciones hasta reducir el número de tokens
        while total_tokens > TOKEN_BUDGET:
            removed_message = memory.pop(0)
            total_tokens -= num_tokens(removed_message['content'])
    
    return memory
    