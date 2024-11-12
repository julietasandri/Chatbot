import streamlit as st
from groq import Groq

#titulo de la pestaña web
st.set_page_config(page_title="Mi chatbot de AI", page_icon="🎶")

#titulo de la pagina
st.title("Chatbot AI con streamlit")

#ingreso de datos
nombre = st.text_input("Ingresa tu nombre")

#boton con funcion
if st.button("saludar") :
    st.write(f"Hola {nombre}, gracias")

#opciones del selectbox
MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#va a conectar a la api
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #obtener la clave
    return Groq(api_key = clave_secreta) #crear el usuario

#configurar el modelo de IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada): 
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

#historial del chat
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]): st.markdown(mensaje["content"])

#contenedor del chat
def area_chat(): 
    contenedorChat= st.container(height = 400, border = True, )
    with contenedorChat: mostrar_historial()
        

#funcion - diseño de pagina
def configurar_web():
    st.title("Chatbot de AI")
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegi una opcion", MODELO, index= 0
    )
    return seleccion 

#generar las respuestas
def generar_respuestas(chat_completo):
    respuesta_comp = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content : 
            respuesta_comp += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_comp 

#funcion principal
def main():
    #llamado de funciones
    modelo = configurar_web()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Ingresa tu mensaje")
    #Verificar si el mensaje no esta vacio
    if mensaje:
        actualizar_historial("user", mensaje, "🎡") #visualizar el mensaje del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo: 
            with st.chat_message("assistant"):
                respuesta_comp = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_comp, "🌌")
    st.rerun()

if __name__ == "__main__":
    main()