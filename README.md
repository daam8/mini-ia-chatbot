# Mini IA - Chatbot Inteligente 🤖

## Estructura del proyecto, Profesora no supe como subir todos los archivos como la estructura, asi que por eso le subi el zip donde estan todas las carpetas.

```
mini-ia-chatbot/
├── main.py                  # Punto de entrada: ejecuta el chatbot
├── requirements.txt          # Dependencias (ninguna externa)
├── .gitignore
├── README.md
├── data/
│   ├── conocimiento.json      # Base de conocimiento (categorías, patrones, respuestas)
│   └── historial.json         # Se genera automáticamente con cada conversación
├── src/
│   ├── __init__.py
│   ├── nlp_utils.py           # Normalización de texto y cálculo de similitud
│   ├── chatbot.py              # Lógica principal: decide qué responder
│   ├── conocimiento.py         # Cargar/guardar/agregar conocimiento (JSON)
│   ├── memoria.py              # Historial de conversaciones
│   └── utilidades.py           # Hora, fecha y calculadora simple
└── tests/
    ├── __init__.py
    └── test_chatbot.py         # Pruebas unitarias con unittest
```

## Cómo ejecutarlo

Requisitos: tener **Python 3.8 o superior** instalado.

1. Clona o descarga el proyecto.
2. Abre la carpeta en **Visual Studio Code**.
3. Abre una terminal dentro de VS Code (`Ctrl + ñ` o `Terminal > Nueva Terminal`).
4. Ejecuta:

```bash
python main.py
```

5. ¡Empieza a chatear! Escribe `ayuda` para ver qué sabe hacer, o `salir` para terminar.

## ¿Cómo "entiende" el chatbot? (para explicar en clase)

En lugar de escribir cientos de líneas como:

```python
if mensaje == "hola":
    ...
elif mensaje == "Hola":
    ...
elif mensaje == "HOLA":
    ...
```

El proyecto usa dos ideas centrales:

1. **Normalización de texto** (`nlp_utils.normalizar_texto`): convierte
   cualquier mensaje a minúsculas, sin tildes y sin signos de puntuación,
   para que "¡Hola!", "hola" y "HOLA " se traten como lo mismo.

2. **Similitud de texto** (`nlp_utils.calcular_similitud`, usando
   `difflib.SequenceMatcher` de la librería estándar): en vez de exigir una
   coincidencia exacta, el bot mide qué tan parecido es el mensaje del
   usuario a cada "patrón" guardado en `data/conocimiento.json`, y responde
   con la categoría que tenga mayor parecido (si supera un umbral mínimo).

Esto permite que el bot entienda variaciones como "q hora es", "que hora es"
o "dime la hora" sin necesidad de escribir un `if` para cada posibilidad.

##  Funcionalidades principales

-  Saludos, despedidas, agradecimientos y preguntas sobre su identidad.
-  Responder la hora y la fecha actual.
-  Resolver operaciones matemáticas simples (`5 + 3`, `10 * 2`, `20 / 4`).
-  Contar chistes.
-  **Aprendizaje en tiempo real**: si el bot no entiende algo, le puedes
  enseñar una categoría y una respuesta nueva, y quedará guardada en
  `data/conocimiento.json` para la próxima vez.
-  **Historial persistente**: cada conversación queda registrada con
  fecha y hora en `data/historial.json`.

##  Uso de funciones (`def`)

Todo el proyecto está construido a partir de **funciones pequeñas y con un
solo propósito** (principio de responsabilidad única), tal como se vio en
clase. Por ejemplo, `chatbot.py` no tiene una sola función gigante: separa
`procesar_comando_especial`, `buscar_mejor_categoria` y `generar_respuesta`,
cada una encargada de una sola tarea. Esto hace el código más fácil de leer,
probar y explicar.

##  Pruebas unitarias

El proyecto incluye pruebas automáticas con el módulo `unittest` de Python.
Para ejecutarlas desde la raíz del proyecto:

```bash
python -m unittest discover tests
```

##  Posibles mejoras futuras

- Conectar con una interfaz gráfica (Tkinter) o una interfaz web (Flask).
- Agregar reconocimiento de intenciones más avanzado (machine learning real).
- Agregar soporte multi-idioma.

##  Autor

Proyecto desarrollado como parcial universitario para la materia de
Programación / Introducción a la Inteligencia Artificial.
