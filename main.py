from __future__ import annotations

import argparse
from pathlib import Path  # evita escribir rutas como strings sueltos

from src.buscador import Documento, buscar, cargar_documentos
from src.graficos import barras_ascii, resumen_matriz


RUTA_DOCUMENTOS = Path("data/documentos.txt")
CONSULTAS_DEMO = [
    "inteligencia artificial aprendizaje automatico",
    "redes y seguridad informatica",
    "recetas de cocina saludable",
]


def imprimir_documentos(documentos: list[Documento]) -> None:
    print("Documentos cargados:")
    for documento in documentos:
        print(f"- {documento.id}: {documento.titulo}")
    print()


def ejecutar_consulta(documentos: list[Documento], consulta: str, top: int) -> None:
    # buscar devuelve datos internos para explicar la matriz y resultados para mostrar
    vocabulario, matriz, resultados = buscar(documentos, consulta, top=top)

    print(f"Consulta: {consulta}")
    print(resumen_matriz(vocabulario, matriz))
    print()
    print("Resultados mas similares:")
    for posicion, resultado in enumerate(resultados, start=1):
        print(
            f"{posicion}. {resultado.documento.titulo} "
            f"({resultado.similitud:.4f})"
        )
        print(f"   {resultado.documento.texto}")
    print()
    print(barras_ascii(resultados))
    print("-" * 72)


def modo_interactivo(documentos: list[Documento], top: int) -> None:
    imprimir_documentos(documentos)
    print("Escribe una consulta o ENTER para salir.")
    while True:
        consulta = input("> ").strip()
        if not consulta:
            break
        ejecutar_consulta(documentos, consulta, top)


def parsear_argumentos() -> argparse.Namespace:
    # argparse permite usar parametros por consola query top e interactive
    parser = argparse.ArgumentParser(
        description="Buscador semantico simple con similitud coseno."
    )
    parser.add_argument(
        "--documentos",
        default=str(RUTA_DOCUMENTOS),
        help="Ruta del archivo id|titulo|texto.",
    )
    parser.add_argument(
        "--query",
        "-q",
        help="Consulta unica. Si se omite, se ejecutan consultas de demo.",
    )
    parser.add_argument("--top", type=int, default=3, help="Cantidad de resultados.")
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Activa busqueda interactiva por consola.",
    )
    return parser.parse_args()


def main() -> None:
    args = parsear_argumentos()
    documentos = cargar_documentos(args.documentos)

    # modo libre el usuario escribe varias consultas hasta presionar enter vacio
    if args.interactive:
        modo_interactivo(documentos, args.top)
        return

    imprimir_documentos(documentos)
    # sin query corre consultas preparadas para mostrar la demo rapidamente
    consultas = [args.query] if args.query else CONSULTAS_DEMO
    for consulta in consultas:
        ejecutar_consulta(documentos, consulta, args.top)


if __name__ == "__main__":
    main()
