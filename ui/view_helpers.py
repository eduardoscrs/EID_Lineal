import html

import pandas as pd


def escapar(texto: object) -> str:
    """Escapa texto antes de insertarlo en bloques HTML."""
    return html.escape(str(texto), quote=True)


def normalizar_espacios(texto: object) -> str:
    """Compacta saltos de linea y espacios repetidos para vistas previas."""
    return " ".join(str(texto).split())


def crear_vista_previa(texto: object, limite: int = 420) -> str:
    """Devuelve un resumen corto sin modificar el texto usado por el modelo."""
    texto_limpio = normalizar_espacios(texto)
    if len(texto_limpio) <= limite:
        return texto_limpio

    corte = texto_limpio.rfind(" ", 0, limite)
    if corte < limite * 0.65:
        corte = limite
    return texto_limpio[:corte].rstrip() + "..."


def prioridad_visual_termino(termino: object) -> tuple[int, str]:
    """Mueve numeros y abreviaciones cortas al final de las vistas."""
    termino_texto = str(termino)
    es_numero_anio = termino_texto.isdigit() and len(termino_texto) == 4
    es_abreviacion_corta = len(termino_texto) <= 2
    prioridad = 1 if es_numero_anio or es_abreviacion_corta else 0
    return prioridad, termino_texto


def ordenar_terminos_para_mostrar(terminos) -> list[str]:
    """Ordena terminos solo para que la interfaz sea mas legible."""
    return sorted([str(termino) for termino in terminos], key=prioridad_visual_termino)


def ordenar_columnas_por_valor(dataframe: pd.DataFrame) -> list[str]:
    """Ordena columnas dejando primero los pesos mas altos de una fila."""
    valores = dataframe.iloc[0]
    return sorted(
        dataframe.columns,
        key=lambda termino: (
            -float(valores[termino]),
            *prioridad_visual_termino(termino),
        ),
    )


def calcular_altura_tabla(cantidad_filas: int, maximo_filas: int = 10) -> int:
    """Ajusta tablas a sus filas visibles y deja scroll desde 10 filas."""
    filas_visibles = max(1, min(cantidad_filas, maximo_filas))
    return 52 + filas_visibles * 36


def calcular_altura_tabla_matriz(cantidad_filas: int) -> int:
    """Deja la tabla de vocabulario alineada con las metricas laterales."""
    return max(calcular_altura_tabla(cantidad_filas), 515)


def clasificar_similitud(valor: float) -> str:
    """Entrega una etiqueta simple para explicar el puntaje."""
    if valor >= 0.60:
        return "Alta similitud"
    if valor >= 0.25:
        return "Similitud media"
    return "Baja similitud"


def construir_barra_puntaje(valor: float) -> str:
    """Crea una barra HTML proporcional al puntaje de similitud."""
    ancho = max(0, min(100, valor * 100))
    return (
        '<div class="score-bar">'
        f'<div class="score-fill" style="width: {ancho:.1f}%"></div>'
        "</div>"
    )


def estilizar_tabla_oscura(dataframe: pd.DataFrame):
    """Aplica colores oscuros a tablas mostradas con Streamlit."""
    return (
        dataframe.style.set_properties(
            **{
                "background-color": "#f8fbfd",
                "color": "#27374d",
                "border-color": "#dde6ed",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#27374d"),
                        ("color", "#ffffff"),
                        ("border-color", "#526d82"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "#dde6ed"),
                    ],
                },
            ]
        )
    )


def obtener_perfil_vectorizador(tipo_vectorizador: str) -> dict[str, str]:
    """Textos cortos para explicar el metodo elegido."""
    if tipo_vectorizador == "TF-IDF":
        return {
            "titulo": "TF-IDF",
            "subtitulo": "Da mas peso a las palabras que distinguen a un documento.",
            "idea": "Una palabra vale mas cuando aparece en un documento, pero no aparece tanto en todos los demas.",
            "matriz": "Las celdas son pesos decimales. Un numero alto indica que el termino ayuda a identificar ese texto.",
            "uso": "Conviene cuando importa encontrar terminos representativos, no solo contar repeticiones.",
            "formula": "peso = frecuencia del termino x rareza en el corpus",
        }

    return {
        "titulo": "CountVectorizer",
        "subtitulo": "Cuenta cuantas veces aparece cada palabra en cada documento.",
        "idea": "Una palabra vale mas si se repite mas dentro del documento.",
        "matriz": "Las celdas son conteos enteros. Un numero alto indica mas apariciones del termino.",
        "uso": "Conviene cuando se quiere una lectura directa y facil de explicar en la matriz.",
        "formula": "peso = numero de apariciones del termino",
    }
