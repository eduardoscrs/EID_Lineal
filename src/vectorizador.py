from __future__ import annotations

import re
from collections import Counter  # cuenta cuantas veces aparece cada token
from typing import Iterable  # acepta listas tuplas u otras colecciones recorribles


# palabras muy comunes que aportan poco al comparar temas entre documentos
STOPWORDS = {
    "a",
    "al",
    "con",
    "de",
    "del",
    "el",
    "en",
    "es",
    "la",
    "las",
    "los",
    "para",
    "por",
    "que",
    "se",
    "un",
    "una",
    "y",
}


def tokenizar(texto: str, quitar_stopwords: bool = True) -> list[str]:
    # convierte texto libre en tokens normalizados
    # regex simple conserva letras y numeros elimina signos de puntuacion
    tokens = re.findall(r"[a-zA-Z0-9]+", texto.lower())
    if not quitar_stopwords:
        return tokens
    return [token for token in tokens if token not in STOPWORDS]  # quita ruido comun


def construir_vocabulario(documentos: Iterable[str]) -> list[str]:
    # construye un vocabulario ordenado a partir de los documentos
    vocabulario: set[str] = set()  # set evita palabras duplicadas
    for documento in documentos:
        vocabulario.update(tokenizar(documento))  # update agrega varios tokens al set
    return sorted(vocabulario)  # orden fijo misma columna para el mismo termino


def vectorizar_texto(texto: str, vocabulario: list[str]) -> list[int]:
    # representa un texto como vector de frecuencia sobre el vocabulario
    conteo = Counter(tokenizar(texto))  # counter actua como token a frecuencia
    return [conteo[termino] for termino in vocabulario]  # posicion igual a columna


def construir_matriz(
    documentos: Iterable[str], vocabulario: list[str] | None = None
) -> tuple[list[str], list[list[int]]]:
    # construye la matriz documento termino
    # list permite recorrer los documentos mas de una vez si venian como iterable
    documentos_lista = list(documentos)
    # si llega un vocabulario externo se usa si no se calcula desde los documentos
    vocabulario_final = vocabulario or construir_vocabulario(documentos_lista)
    # cada fila representa un documento cada columna representa un termino
    matriz = [
        vectorizar_texto(documento, vocabulario_final) for documento in documentos_lista
    ]
    return vocabulario_final, matriz
