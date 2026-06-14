from __future__ import annotations

from dataclasses import dataclass  # crea clases simples para guardar datos
from math import sqrt
from pathlib import Path  # maneja rutas de archivos de forma portable

from src.vectorizador import construir_matriz, vectorizar_texto


@dataclass(frozen=True)  # frozen true evita modificar el documento por accidente
class Documento:
    id: str
    titulo: str
    texto: str


@dataclass(frozen=True)
class ResultadoBusqueda:
    documento: Documento
    similitud: float


def cargar_documentos(ruta: str | Path) -> list[Documento]:
    # carga documentos desde un archivo con formato id|titulo|texto
    documentos: list[Documento] = []
    # enumerate con start 1 ayuda a reportar errores con numero de linea real
    for numero_linea, linea in enumerate(Path(ruta).read_text().splitlines(), start=1):
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue

        partes = [parte.strip() for parte in linea.split("|", maxsplit=2)]  # id titulo texto
        if len(partes) != 3:
            raise ValueError(
                f"Linea {numero_linea} invalida: se esperaba id|titulo|texto"
            )

        documentos.append(Documento(id=partes[0], titulo=partes[1], texto=partes[2]))

    if not documentos:
        raise ValueError(f"No se encontraron documentos en {ruta}")
    return documentos


def similitud_coseno(vector_a: list[int], vector_b: list[int]) -> float:
    # calcula similitud coseno entre dos vectores numericos
    # zip recorre ambos vectores al mismo tiempo
    producto_punto = sum(a * b for a, b in zip(vector_a, vector_b))
    norma_a = sqrt(sum(a * a for a in vector_a))
    norma_b = sqrt(sum(b * b for b in vector_b))

    # si un vector queda vacio no existe angulo util para comparar
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return producto_punto / (norma_a * norma_b)


def buscar(
    documentos: list[Documento], consulta: str, top: int = 3
) -> tuple[list[str], list[list[int]], list[ResultadoBusqueda]]:
    # ordena documentos segun su similitud con una consulta
    textos = [documento.texto for documento in documentos]
    vocabulario, matriz = construir_matriz(textos)
    vector_consulta = vectorizar_texto(consulta, vocabulario)  # usa las mismas columnas

    resultados = [
        ResultadoBusqueda(
            documento=documento,
            similitud=similitud_coseno(vector_documento, vector_consulta),
        )
        for documento, vector_documento in zip(documentos, matriz)  # documento y su fila
    ]

    resultados.sort(key=lambda resultado: resultado.similitud, reverse=True)  # mayor primero
    return vocabulario, matriz, resultados[:top]
