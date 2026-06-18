import numpy as np
import pandas as pd
import streamlit as st

from ui.view_helpers import (
    calcular_altura_tabla,
    calcular_altura_tabla_matriz,
    crear_vista_previa,
    escapar,
    estilizar_tabla_oscura,
    ordenar_terminos_para_mostrar,
)


def mostrar_documentos(documentos: list[dict[str, str]]) -> None:
    """Muestra los documentos disponibles para la busqueda."""
    st.markdown('<div class="section-eyebrow">Corpus de trabajo</div>', unsafe_allow_html=True)
    st.header("Documentos que alimentan el modelo")
    st.caption(
        "Cada texto sera una fila de la matriz. El tema ayuda a verificar si el ranking final tiene sentido."
    )

    documentos_df = pd.DataFrame(documentos)
    documentos_tabla = pd.DataFrame(
        {
            "Documento": documentos_df["nombre"],
            "Tema": documentos_df["tema"],
            "Vista previa": documentos_df["texto"].apply(lambda texto: crear_vista_previa(texto, 180)),
            "Palabras": documentos_df["texto"].apply(lambda texto: len(str(texto).split())),
        }
    )
    st.dataframe(
        estilizar_tabla_oscura(documentos_tabla),
        width="stretch",
        hide_index=True,
        height=calcular_altura_tabla(len(documentos_tabla)),
    )

    temas = documentos_df["tema"].nunique()
    total_palabras = sum(len(documento["texto"].split()) for documento in documentos)
    col1, col2, col3 = st.columns(3)
    col1.metric("Textos disponibles", len(documentos))
    col2.metric("Temas distintos", temas)
    col3.metric("Palabras aproximadas", total_palabras)

    st.subheader("Vista rapida para presentar")
    columnas = st.columns(2)
    for indice, documento in enumerate(documentos):
        cantidad_palabras = len(documento["texto"].split())
        vista_previa = crear_vista_previa(documento["texto"])
        tarjeta = f"""
        <div class="doc-card">
            <div class="doc-card-header">
                <span class="doc-name">{escapar(documento["nombre"])}</span>
                <span class="doc-topic">{escapar(documento["tema"])}</span>
            </div>
            <div class="preview-shell">
                <div class="preview-bar">
                    <span class="preview-dot"></span>
                    <span class="preview-title">Vista previa</span>
                </div>
                <div class="doc-text">{escapar(vista_previa)}</div>
            </div>
            <div class="doc-meta">{cantidad_palabras} palabras</div>
        </div>
        """
        with columnas[indice % 2]:
            st.markdown(tarjeta, unsafe_allow_html=True)


def mostrar_matriz(
    matriz_df: pd.DataFrame,
    vocabulario: np.ndarray,
    tipo_vectorizador: str,
) -> None:
    """Muestra vocabulario, matriz documento-termino y dimensiones."""
    st.markdown('<div class="section-eyebrow">Representacion numerica</div>', unsafe_allow_html=True)
    st.header("Matriz documento-termino")

    st.markdown(
        f"""
        <div class="info-box">
        Cada fila representa un documento y cada columna representa un termino del vocabulario.
        En esta ejecucion se usa <strong>{tipo_vectorizador}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])
    altura_tablas_documentos = calcular_altura_tabla_matriz(matriz_df.shape[0])
    with col1:
        st.subheader("Dimensiones")
        valores_no_cero = int((matriz_df.to_numpy() != 0).sum())
        total_valores = matriz_df.shape[0] * matriz_df.shape[1]
        densidad = valores_no_cero / total_valores if total_valores else 0
        st.metric("Filas x columnas", f"{matriz_df.shape[0]} x {matriz_df.shape[1]}")
        st.metric("Documentos", matriz_df.shape[0])
        st.metric("Terminos", matriz_df.shape[1])
        st.metric("Valores no cero", valores_no_cero)
        st.metric("Densidad", f"{densidad:.1%}")

    with col2:
        st.subheader("Vocabulario generado")
        vocabulario_mostrar = ordenar_terminos_para_mostrar(vocabulario)
        terminos_destacados = "".join(
            f'<span class="pill">{escapar(termino)}</span>'
            for termino in vocabulario_mostrar[:30]
        )
        st.markdown(
            f'<div class="pill-row vocabulary-pill-row">{terminos_destacados}</div>',
            unsafe_allow_html=True,
        )
        vocabulario_df = pd.DataFrame({"Termino": vocabulario_mostrar})
        st.dataframe(
            estilizar_tabla_oscura(vocabulario_df),
            width="stretch",
            hide_index=True,
            height=altura_tablas_documentos,
        )

    st.subheader("Tabla de la matriz")
    columnas_matriz = [termino for termino in vocabulario_mostrar if termino in matriz_df.columns]
    st.dataframe(
        estilizar_tabla_oscura(matriz_df.loc[:, columnas_matriz].round(3)),
        width="stretch",
        height=altura_tablas_documentos,
    )
