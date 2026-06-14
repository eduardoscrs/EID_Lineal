import streamlit as st

from data.example_documents import DOCUMENTOS_EJEMPLO
from logic.vector_model import generar_modelo_vectorial, matriz_a_dataframe
from ui.sections import (
    mostrar_buscador,
    mostrar_documentos,
    mostrar_funcionamiento,
    mostrar_graficos,
    mostrar_inicio,
    mostrar_matriz,
)
from ui.sidebar import mostrar_sidebar
from ui.styles import configurar_pagina


def inicializar_estado() -> None:
    """Crea las variables de sesion necesarias."""
    if "documentos_usuario" not in st.session_state:
        st.session_state.documentos_usuario = []


def construir_documentos() -> list[dict[str, str]]:
    """Une los documentos base con los documentos agregados desde la interfaz."""
    return DOCUMENTOS_EJEMPLO + st.session_state.documentos_usuario


def main() -> None:
    configurar_pagina()
    inicializar_estado()

    tipo_vectorizador, eliminar_stop_words = mostrar_sidebar()
    documentos = construir_documentos()
    etiquetas_documentos = [documento["nombre"] for documento in documentos]

    vectorizador, matriz_documento_termino, vocabulario = generar_modelo_vectorial(
        documentos=documentos,
        tipo_vectorizador=tipo_vectorizador,
        eliminar_stop_words=eliminar_stop_words,
    )
    matriz_df = matriz_a_dataframe(
        matriz=matriz_documento_termino,
        vocabulario=vocabulario,
        etiquetas=etiquetas_documentos,
    )

    tab_inicio, tab_documentos, tab_matriz, tab_buscador, tab_graficos, tab_funcionamiento = st.tabs(
        [
            "Inicio",
            "Documentos",
            "Matriz",
            "Buscador",
            "Graficos",
            "Funcionamiento",
        ]
    )

    with tab_inicio:
        mostrar_inicio(documentos, vocabulario, matriz_documento_termino, tipo_vectorizador)

    with tab_documentos:
        mostrar_documentos(documentos)

    with tab_matriz:
        mostrar_matriz(matriz_df, vocabulario, tipo_vectorizador)

    with tab_buscador:
        resultados = mostrar_buscador(
            documentos=documentos,
            vectorizador=vectorizador,
            matriz_documento_termino=matriz_documento_termino,
            vocabulario=vocabulario,
        )

    with tab_graficos:
        mostrar_graficos(
            matriz_df=matriz_df,
            matriz_documento_termino=matriz_documento_termino,
            etiquetas_documentos=etiquetas_documentos,
            tipo_vectorizador=tipo_vectorizador,
            resultados=resultados,
        )

    with tab_funcionamiento:
        mostrar_funcionamiento(tipo_vectorizador)


if __name__ == "__main__":
    main()
