import numpy as np
import pandas as pd

# Vectorizadores para representar documentos como vectores numéricos
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# Función para calcular similitud coseno entre vectores
from sklearn.metrics.pairwise import cosine_similarity
# Lista de stop words en español
from data.stop_words import STOP_WORDS_ES

# Patrón para definir los términos válidos del texto
TOKEN_PATTERN_TEXTO = r"(?u)\b(?:[^\W\d_]{2,}|\d{4})\b"


def crear_vectorizador(tipo_vectorizador: str, eliminar_stop_words: bool):
    """Devuelve CountVectorizer o TfidfVectorizer segun la seleccion."""
    
    # Define si se eliminarán palabras vacías
    stop_words = STOP_WORDS_ES if eliminar_stop_words else None

    # Crea un vectorizador TF-IDF
    if tipo_vectorizador == "TF-IDF":
        return TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            stop_words=stop_words,
            token_pattern=TOKEN_PATTERN_TEXTO,
        )

    # Crea un vectorizador basado en frecuencia de términos
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
    
    # Extrae los textos de los documentos
    textos = [documento["texto"] for documento in documentos]

    # Crea el vectorizador seleccionado
    vectorizador = crear_vectorizador(tipo_vectorizador, eliminar_stop_words)

    # Genera la matriz documento-término
    matriz_documento_termino = vectorizador.fit_transform(textos)

    # Obtiene el vocabulario aprendido
    vocabulario = vectorizador.get_feature_names_out()

    return vectorizador, matriz_documento_termino, vocabulario

def matriz_a_dataframe(matriz, vocabulario: np.ndarray, etiquetas: list[str]) -> pd.DataFrame:
    """Convierte una matriz dispersa de scikit-learn en una tabla de pandas."""
    
    # Convierte la matriz a DataFrame para visualizarla
    return pd.DataFrame(matriz.toarray(), index=etiquetas, columns=vocabulario)

def calcular_similitud_consulta(vectorizador, consulta: str, matriz_documento_termino):
    """Vectoriza una consulta y calcula su similitud con cada documento."""
    
    # Convierte la consulta en un vector
    vector_consulta = vectorizador.transform([consulta])

    # Calcula la similitud coseno con cada documento
    similitudes = cosine_similarity(vector_consulta, matriz_documento_termino).flatten()

    return vector_consulta, similitudes

def preparar_resultados(
    documentos: list[dict[str, str]],
    similitudes: np.ndarray,
) -> pd.DataFrame:
    """Ordena los documentos desde mayor a menor similitud."""
    
    # Lista donde se almacenarán los resultados
    filas = []

    # Construye una fila para cada documento
    for indice, documento in enumerate(documentos):
        filas.append(
            {
                "Documento": documento["nombre"],
                "Tema": documento["tema"],
                "Texto": documento["texto"],
                "Similitud coseno": float(similitudes[indice]),
            }
        )

    # Ordena los documentos según su similitud con la consulta
    resultados = pd.DataFrame(filas).sort_values(
        by="Similitud coseno",
        ascending=False,
    )

    # Agrega una columna de ranking
    resultados.insert(0, "Ranking", range(1, len(resultados) + 1))

    return resultados