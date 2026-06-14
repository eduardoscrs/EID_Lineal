from __future__ import annotations

from src.buscador import ResultadoBusqueda


def barras_ascii(resultados: list[ResultadoBusqueda], ancho: int = 32) -> str:
    # devuelve un grafico de barras ascii para comparar similitudes
    if not resultados:
        return "Sin resultados."

    lineas: list[str] = []
    for resultado in resultados:
        largo = round(resultado.similitud * ancho)  # convierte similitud a ancho visual
        barra = "#" * largo or "-"  # muestra explicitamente similitud cero
        porcentaje = resultado.similitud * 100
        lineas.append(
            f"{resultado.documento.id:>4} | {barra:<{ancho}} | {porcentaje:6.2f}%"
        )
    return "\n".join(lineas)


def resumen_matriz(vocabulario: list[str], matriz: list[list[int]]) -> str:
    # resume dimensiones y algunos terminos de la matriz documento termino
    columnas = len(vocabulario)
    filas = len(matriz)
    muestra = ", ".join(vocabulario[:12])  # solo muestra una parte para no saturar
    if columnas > 12:
        muestra = f"{muestra}, ..."
    return (
        f"Matriz documento-termino: {filas} documentos x {columnas} terminos\n"
        f"Primeros terminos: {muestra}"
    )
