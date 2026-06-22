import pandas as pd
import streamlit as st

from ui.view_helpers import escapar, obtener_perfil_vectorizador
from visualization.charts import (
    crear_grafico_barras_similitud,
    crear_grafico_terminos,
    crear_mapa_calor_documentos,
    crear_mapa_calor_matriz,
)


def mostrar_graficos(
    matriz_df: pd.DataFrame,
    matriz_documento_termino,
    etiquetas_documentos: list[str],
    tipo_vectorizador: str,
    resultados: pd.DataFrame | None,
) -> None:
    """Muestra las visualizaciones principales de apoyo."""
    st.markdown('<div class="section-eyebrow">Evidencia visual</div>', unsafe_allow_html=True)
    st.header("Graficos para explicar el resultado")
    st.caption("Estas vistas sirven como apoyo para responder que palabras pesan mas y que documentos quedan cerca.")

    st.subheader("1. Terminos principales")
    st.pyplot(
        crear_grafico_terminos(matriz_df, tipo_vectorizador),
        clear_figure=True,
        width="stretch",
    )
    st.divider()

    st.subheader("2. Similitud con la consulta")
    if resultados is None:
        st.info("Ingresa una consulta en la pantalla anterior para ver este grafico.")
    else:
        st.pyplot(
            crear_grafico_barras_similitud(resultados),
            clear_figure=True,
            width="stretch",
        )
    st.divider()

    st.subheader("3. Matriz como mapa de calor")
    st.pyplot(
        crear_mapa_calor_matriz(matriz_df, tipo_vectorizador),
        clear_figure=True,
        width="stretch",
    )
    st.divider()

    st.subheader("4. Cercania entre documentos")
    st.pyplot(
        crear_mapa_calor_documentos(matriz_documento_termino, etiquetas_documentos),
        clear_figure=True,
        width="stretch",
    )


def mostrar_cierre(
    tipo_vectorizador: str,
    eliminar_stop_words: bool,
    resultados: pd.DataFrame | None,
) -> None:
    """Pantalla final con ideas de cierre para la presentacion."""
    perfil = obtener_perfil_vectorizador(tipo_vectorizador)
    estado_stop_words = "con limpieza de palabras comunes" if eliminar_stop_words else "sin limpieza de palabras comunes"

    st.markdown('<div class="section-eyebrow">Cierre de la exposicion</div>', unsafe_allow_html=True)
    st.header("Idea final")
    st.markdown(
        f"""
        <div class="closing-band">
            <h2>Un buscador puede comparar textos si primero los convierte en vectores.</h2>
            <p>
                En esta version se uso <strong>{escapar(tipo_vectorizador)}</strong>,
                {escapar(estado_stop_words)}. La matriz permite aplicar algebra lineal
                y la similitud coseno ordena los documentos mas cercanos a la consulta.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.markdown(
        f"""
        <div class="takeaway-card">
            <div class="takeaway-title">Metodo</div>
            <div class="takeaway-text">{escapar(perfil["idea"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col2.markdown(
        """
        <div class="takeaway-card">
            <div class="takeaway-title">Matriz</div>
            <div class="takeaway-text">Filas son documentos, columnas son terminos y cada celda guarda un peso numerico.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col3.markdown(
        """
        <div class="takeaway-card">
            <div class="takeaway-title">Similitud</div>
            <div class="takeaway-text">El coseno compara la direccion de los vectores y devuelve un ranking interpretable.</div>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )

    if resultados is not None and not resultados.empty:
        mejor = resultados.iloc[0]
        st.markdown(
            f"""
            <div class="final-result">
                <div class="top-result-kicker">Ultima consulta guardada</div>
                <div class="top-result-title">{escapar(mejor["Documento"])} - {escapar(mejor["Tema"])}</div>
                <div class="score-label">Similitud coseno: {float(mejor["Similitud coseno"]):.4f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
