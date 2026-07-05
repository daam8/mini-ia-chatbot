"""
main.py
-------
Punto de entrada del proyecto "Mini IA - Chatbot Inteligente".

Este archivo se encarga de:
    1. Cargar la base de conocimiento y el historial guardado.
    2. Mostrar un mensaje de bienvenida.
    3. Mantener un ciclo de conversación con el usuario.
    4. Si el bot no entiende algo, ofrecer "enseñarle" una nueva respuesta.
    5. Guardar el historial y la base de conocimiento actualizada al salir.

Para ejecutar el proyecto:
    python main.py
"""

import os

from src.chatbot import generar_respuesta
from src.conocimiento import cargar_base_conocimiento, guardar_base_conocimiento, agregar_nuevo_conocimiento
from src.memoria import cargar_historial, guardar_historial, agregar_al_historial
from src.nlp_utils import normalizar_texto

# Rutas de los archivos de datos del proyecto.
RUTA_CONOCIMIENTO = os.path.join("data", "conocimiento.json")
RUTA_HISTORIAL = os.path.join("data", "historial.json")

# Palabras que el usuario puede escribir para cerrar el programa.
COMANDOS_SALIDA = {"salir", "exit", "terminar", "adios chao", "quit"}


def mostrar_bienvenida():
    """
    Imprime en pantalla un encabezado de bienvenida para el chatbot.

    Retorna:
        None
    """
    print("=" * 60)
    print("        MINI IA - CHATBOT INTELIGENTE")
    print("=" * 60)
    print("Bot: ¡Hola! Soy Mini IA 🤖. Puedo ayudarte con varias cosas:")
    print("Bot:  • Decirte la hora o la fecha")
    print("Bot:  • Resolver operaciones matemáticas (ej: 5 + 3)")
    print("Bot:  • Responder preguntas de cultura general (ej: ¿qué es el sol?)")
    print("Bot:  • Contarte un chiste")
    print("Bot:  • Aprender algo nuevo si me lo enseñas")
    print("Bot: Escribe 'salir' cuando quieras terminar la conversación.")
    print("Bot: ¿En qué te puedo ayudar hoy?\n")


def es_comando_de_salida(texto_normalizado):
    """
    Verifica si el mensaje del usuario es un comando para terminar el chat.

    Parámetros:
        texto_normalizado (str): mensaje del usuario ya normalizado.

    Retorna:
        bool: True si el usuario quiere salir del programa.
    """
    return texto_normalizado in COMANDOS_SALIDA


def modo_aprendizaje(mensaje_usuario, base_conocimiento):
    """
    Se activa cuando el bot NO entendió el mensaje del usuario.
    Le pregunta al usuario si quiere enseñarle una respuesta nueva
    para ese tipo de mensaje, y en caso afirmativo, la guarda.

    Parámetros:
        mensaje_usuario (str): mensaje original que el bot no entendió.
        base_conocimiento (dict): base de conocimiento actual.

    Retorna:
        tuple: (respuesta_para_mostrar (str), base_conocimiento (dict actualizado))
    """
    print("Bot: No estoy seguro de cómo responder a eso todavía.")
    quiere_ensenar = input("Bot: ¿Quieres enseñarme una respuesta? (si/no): ").strip().lower()

    if quiere_ensenar not in ("si", "sí"):
        return "Sin problema, sigamos conversando.", base_conocimiento

    categoria = input("Bot: ¿Cómo llamamos a esta categoría? (ej: 'clima'): ").strip().lower()
    nueva_respuesta = input("Bot: ¿Qué debería responder la próxima vez? ").strip()

    patron_normalizado = normalizar_texto(mensaje_usuario)
    base_conocimiento = agregar_nuevo_conocimiento(
        base_conocimiento, categoria, patron_normalizado, nueva_respuesta
    )

    return "¡Gracias! Ya aprendí algo nuevo.", base_conocimiento


def ciclo_conversacion(base_conocimiento, historial):
    """
    Ejecuta el ciclo principal de conversación: pide un mensaje al usuario,
    genera una respuesta y repite hasta que el usuario decida salir.

    Parámetros:
        base_conocimiento (dict): base de conocimiento cargada desde JSON.
        historial (list): historial de conversaciones cargado desde JSON.

    Retorna:
        tuple: (base_conocimiento actualizada, historial actualizado)
    """
    while True:
        mensaje_usuario = input("Tú: ").strip()

        if mensaje_usuario == "":
            print("Bot: Escribe algo para que pueda ayudarte :)")
            continue

        texto_normalizado = normalizar_texto(mensaje_usuario)

        if es_comando_de_salida(texto_normalizado):
            print("Bot: ¡Hasta luego! Fue un gusto conversar contigo.")
            historial = agregar_al_historial(historial, mensaje_usuario, "(fin de la conversación)")
            break

        respuesta = generar_respuesta(mensaje_usuario, base_conocimiento)

        if respuesta is None:
            respuesta, base_conocimiento = modo_aprendizaje(mensaje_usuario, base_conocimiento)

        print(f"Bot: {respuesta}")
        historial = agregar_al_historial(historial, mensaje_usuario, respuesta)

    return base_conocimiento, historial


def main():
    """
    Función principal del programa. Orquesta la carga de datos,
    la conversación y el guardado final de la información.

    Retorna:
        None
    """
    # Nos aseguramos de que la carpeta "data" exista antes de leer/escribir en ella.
    os.makedirs("data", exist_ok=True)

    base_conocimiento = cargar_base_conocimiento(RUTA_CONOCIMIENTO)
    historial = cargar_historial(RUTA_HISTORIAL)

    mostrar_bienvenida()

    base_conocimiento, historial = ciclo_conversacion(base_conocimiento, historial)

    # Guardamos todo lo aprendido y conversado antes de cerrar el programa.
    guardar_base_conocimiento(RUTA_CONOCIMIENTO, base_conocimiento)
    guardar_historial(RUTA_HISTORIAL, historial)

    print("\n(Se guardó el historial y el nuevo conocimiento aprendido. ¡Hasta la próxima!)")


if __name__ == "__main__":
    main()
