"""
test_chatbot.py
----------------
Pruebas unitarias del proyecto usando el módulo estándar 'unittest'.

Estas pruebas sirven para demostrar en clase que el código funciona
correctamente y que fue probado de forma ordenada, no solo "a ojo".

Para ejecutar las pruebas desde la raíz del proyecto:
    python -m unittest discover tests
"""

import unittest

from src.nlp_utils import normalizar_texto, calcular_similitud, calcular_similitud_por_palabras
from src.utilidades import (
    es_operacion_matematica,
    resolver_operacion_matematica,
)
from src.chatbot import generar_respuesta, buscar_mejor_categoria
from src.conocimiento import agregar_nuevo_conocimiento
from src.cultura_general import extraer_tema_pregunta, responder_pregunta_general


class TestNlpUtils(unittest.TestCase):
    """Pruebas para las funciones de procesamiento de texto."""

    def test_normalizar_texto_quita_acentos_y_mayusculas(self):
        resultado = normalizar_texto("¡CÓMO ESTÁS!")
        self.assertEqual(resultado, "como estas")

    def test_normalizar_texto_quita_espacios_extra(self):
        resultado = normalizar_texto("   Hola   ")
        self.assertEqual(resultado, "hola")

    def test_calcular_similitud_textos_identicos(self):
        self.assertEqual(calcular_similitud("hola", "hola"), 1.0)

    def test_calcular_similitud_textos_diferentes(self):
        similitud = calcular_similitud("hola", "adios")
        self.assertLess(similitud, 0.5)


class TestSimilitudPorPalabras(unittest.TestCase):
    """Pruebas para la comparación de frases palabra por palabra."""

    def test_reconoce_palabra_clave_en_frase_larga(self):
        # "ayuda" debería reconocerse dentro de una frase mucho más larga.
        puntaje = calcular_similitud_por_palabras("en que me puedes ayudar", "ayuda")
        self.assertGreater(puntaje, 0.7)

    def test_frases_sin_relacion_dan_puntaje_bajo(self):
        puntaje = calcular_similitud_por_palabras("me gusta el futbol", "cuentame un chiste")
        self.assertLess(puntaje, 0.5)


class TestCulturaGeneral(unittest.TestCase):
    """Pruebas para el módulo de preguntas de cultura general."""

    def test_extraer_tema_pregunta_que_es(self):
        tema = extraer_tema_pregunta("que es el sol")
        self.assertEqual(tema, "sol")

    def test_extraer_tema_pregunta_no_aplica(self):
        tema = extraer_tema_pregunta("hola como estas")
        self.assertIsNone(tema)

    def test_responder_pregunta_general_conocida(self):
        respuesta = responder_pregunta_general("que es el sol")
        self.assertIsNotNone(respuesta)
        self.assertIn("estrella", respuesta.lower())

    def test_responder_pregunta_general_desconocida(self):
        respuesta = responder_pregunta_general("que es el flumoxinator")
        self.assertIsNone(respuesta)


class TestUtilidades(unittest.TestCase):
    """Pruebas para las funciones de hora, fecha y calculadora."""

    def test_detecta_operacion_matematica_valida(self):
        self.assertTrue(es_operacion_matematica("5 + 3"))
        self.assertTrue(es_operacion_matematica("10*2"))

    def test_detecta_texto_que_no_es_operacion(self):
        self.assertFalse(es_operacion_matematica("hola como estas"))

    def test_resolver_suma(self):
        resultado = resolver_operacion_matematica("5 + 3")
        self.assertEqual(resultado, "El resultado es: 8")

    def test_resolver_division_entre_cero(self):
        resultado = resolver_operacion_matematica("5 / 0")
        self.assertEqual(resultado, "No puedo dividir entre cero.")


class TestChatbot(unittest.TestCase):
    """Pruebas para la lógica principal de generación de respuestas."""

    def setUp(self):
        """Se ejecuta antes de cada prueba: crea una base de conocimiento de prueba."""
        self.base_conocimiento = {
            "saludos": {
                "patrones": ["hola", "buenas"],
                "respuestas": ["¡Hola!"]
            }
        }

    def test_buscar_mejor_categoria_encuentra_saludo(self):
        categoria, puntaje = buscar_mejor_categoria("hola", self.base_conocimiento)
        self.assertEqual(categoria, "saludos")
        self.assertGreater(puntaje, 0.7)

    def test_generar_respuesta_reconoce_saludo(self):
        respuesta = generar_respuesta("Hola!", self.base_conocimiento)
        self.assertEqual(respuesta, "¡Hola!")

    def test_generar_respuesta_devuelve_none_si_no_entiende(self):
        respuesta = generar_respuesta("xyzabc123 sin sentido", self.base_conocimiento)
        self.assertIsNone(respuesta)

    def test_generar_respuesta_resuelve_operacion_matematica(self):
        respuesta = generar_respuesta("4 * 2", self.base_conocimiento)
        self.assertEqual(respuesta, "El resultado es: 8")


class TestConocimiento(unittest.TestCase):
    """Pruebas para el módulo que administra la base de conocimiento."""

    def test_agregar_nuevo_conocimiento_crea_categoria(self):
        base = {}
        base = agregar_nuevo_conocimiento(base, "clima", "que clima hace", "Hace un lindo día.")
        self.assertIn("clima", base)
        self.assertIn("que clima hace", base["clima"]["patrones"])
        self.assertIn("Hace un lindo día.", base["clima"]["respuestas"])


if __name__ == "__main__":
    unittest.main()
