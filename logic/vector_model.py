import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.stop_words import STOP_WORDS_ES

# Terminos validos del vocabulario: palabras de 2+ letras o numeros de 4 digitos
# como anos. Esto define que columnas puede llegar a tener la matriz.
TOKEN_PATTERN_TEXTO = r"(?u)\b(?:[^\W\d_]{2,}|\d{4})\b"


def crear_vectorizador(tipo_vectorizador: str, eliminar_stop_words: bool):
    """Devuelve CountVectorizer o TfidfVectorizer segun la seleccion."""
    stop_words = STOP_WORDS_ES if eliminar_stop_words else None

    if tipo_vectorizador == "TF-IDF":
        # TF-IDF calcula pesos: alto si el termino aparece en este documento,
        # bajo si aparece en muchos documentos del corpus.
        return TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words=stop_words,
            token_pattern=TOKEN_PATTERN_TEXTO,
        )

    # CountVectorizer guarda frecuencias absolutas: cada celda es el numero
    # de veces que aparece un termino en un documento.
    return CountVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words=stop_words,
        token_pattern=TOKEN_PATTERN_TEXTO,
    )


def generar_modelo_vectorial(
    documentos: list[dict[str, str]],
    tipo_vectorizador: str,
    eliminar_stop_words: bool,
):
    """Ajusta el vectorizador y genera la matriz documento-termino."""
    textos = [documento["texto"] for documento in documentos]
    vectorizador = crear_vectorizador(tipo_vectorizador, eliminar_stop_words)

    # fit_transform hace dos cosas centrales:
    # 1. aprende el vocabulario del corpus, que seran las columnas;
    # 2. convierte cada documento en una fila numerica de la matriz.
    matriz_documento_termino = vectorizador.fit_transform(textos)

    # El vocabulario queda en el mismo orden que las columnas de la matriz.
    vocabulario = vectorizador.get_feature_names_out()

    return vectorizador, matriz_documento_termino, vocabulario


def matriz_a_dataframe(matriz, vocabulario: np.ndarray, etiquetas: list[str]) -> pd.DataFrame:
    """Convierte una matriz dispersa de scikit-learn en una tabla de pandas."""
    # La matriz de scikit-learn es dispersa para ahorrar memoria. toarray()
    # la vuelve visible como tabla: filas=documentos, columnas=terminos.
    return pd.DataFrame(matriz.toarray(), index=etiquetas, columns=vocabulario)


def calcular_similitud_consulta(vectorizador, consulta: str, matriz_documento_termino):
    """Vectoriza una consulta y calcula su similitud con cada documento."""
    # La consulta se transforma con el mismo vocabulario aprendido por fit.
    # No se crean columnas nuevas: terminos desconocidos quedan fuera.
    vector_consulta = vectorizador.transform([consulta])

    # Similitud coseno = (q . d) / (||q|| * ||d||). Compara direccion de
    # vectores, por eso funciona aunque los textos tengan largos distintos.
    similitudes = cosine_similarity(vector_consulta, matriz_documento_termino).flatten()

    return vector_consulta, similitudes


def preparar_resultados(
    documentos: list[dict[str, str]],
    similitudes: np.ndarray,
) -> pd.DataFrame:
    """Ordena los documentos desde mayor a menor similitud."""
    filas = []

    for indice, documento in enumerate(documentos):
        filas.append(
            {
                "Documento": documento["nombre"],
                "Tema": documento["tema"],
                "Texto": documento["texto"],
                "Similitud coseno": float(similitudes[indice]),
            }
        )

    # El ranking final se obtiene ordenando el puntaje de similitud coseno.
    resultados = pd.DataFrame(filas).sort_values(
        by="Similitud coseno",
        ascending=False,
    )

    resultados.insert(0, "Ranking", range(1, len(resultados) + 1))

    return resultados
