import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.stop_words import STOP_WORDS_ES


def crear_vectorizador(tipo_vectorizador: str, eliminar_stop_words: bool):
    """Devuelve CountVectorizer o TfidfVectorizer segun la seleccion."""
    stop_words = STOP_WORDS_ES if eliminar_stop_words else None

    if tipo_vectorizador == "TF-IDF":
        return TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words=stop_words,
        )

    return CountVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words=stop_words,
    )


def generar_modelo_vectorial(
    documentos: list[dict[str, str]],
    tipo_vectorizador: str,
    eliminar_stop_words: bool,
):
    """Ajusta el vectorizador y genera la matriz documento-termino."""
    textos = [documento["texto"] for documento in documentos]
    vectorizador = crear_vectorizador(tipo_vectorizador, eliminar_stop_words)
    matriz_documento_termino = vectorizador.fit_transform(textos)
    vocabulario = vectorizador.get_feature_names_out()
    return vectorizador, matriz_documento_termino, vocabulario


def matriz_a_dataframe(matriz, vocabulario: np.ndarray, etiquetas: list[str]) -> pd.DataFrame:
    """Convierte una matriz dispersa de scikit-learn en una tabla de pandas."""
    return pd.DataFrame(matriz.toarray(), index=etiquetas, columns=vocabulario)


def calcular_similitud_consulta(vectorizador, consulta: str, matriz_documento_termino):
    """Vectoriza una consulta y calcula su similitud con cada documento."""
    vector_consulta = vectorizador.transform([consulta])
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

    resultados = pd.DataFrame(filas).sort_values(
        by="Similitud coseno",
        ascending=False,
    )
    resultados.insert(0, "Ranking", range(1, len(resultados) + 1))
    return resultados
