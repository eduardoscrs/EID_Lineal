import numpy as np
import pandas as pd
import streamlit as st

from logic.vector_model import calcular_similitud_consulta, preparar_resultados
from ui.view_helpers import (
    calcular_altura_tabla,
    clasificar_similitud,
    construir_barra_puntaje,
    crear_vista_previa,
    escapar,
    estilizar_tabla_oscura,
    ordenar_columnas_por_valor,
    prioridad_visual_termino,
)


def mostrar_buscador(
    documentos: list[dict[str, str]],
    vectorizador,
    matriz_documento_termino,
    vocabulario: np.ndarray,
) -> pd.DataFrame | None:
    """Permite ingresar una consulta y calcula resultados de similitud."""
    st.markdown('<div class="section-eyebrow">Demo en vivo</div>', unsafe_allow_html=True)
    st.header("Consulta y similitud coseno")
    st.caption("La consulta se convierte al mismo espacio vectorial que los documentos.")

    st.markdown('<div class="sample-row-title">Consultas de ejemplo</div>', unsafe_allow_html=True)
    consultas_ejemplo = [
        "inteligencia artificial",
        "programacion con datos",
        "deporte de equipo",
        "seguridad en redes",
    ]
    columnas_ejemplo = st.columns(len(consultas_ejemplo))
    for indice, consulta_ejemplo in enumerate(consultas_ejemplo):
        with columnas_ejemplo[indice]:
            if st.button(consulta_ejemplo, key=f"consulta_ejemplo_{indice}", use_container_width=True):
                st.session_state.consulta_busqueda = consulta_ejemplo
                st.rerun()

    consulta = st.text_input(
        "Consulta de busqueda",
        placeholder="Ejemplo: inteligencia artificial",
        key="consulta_busqueda",
    )

    if not consulta.strip():
        st.warning("Ingresa una consulta para calcular la similitud coseno.")
        st.markdown(
            """
            <div class="small-note">
            El puntaje de similitud coseno va de 0 a 1 en esta aplicacion: cercano a 1 indica alta similitud y cercano a 0 indica baja similitud.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return None

    # La consulta entra al mismo espacio vectorial de la matriz:
    # mismas columnas, mismo peso TF-IDF o mismo conteo.
    vector_consulta, similitudes = calcular_similitud_consulta(
        vectorizador=vectorizador,
        consulta=consulta,
        matriz_documento_termino=matriz_documento_termino,
    )
    # Fila unica que permite revisar que terminos de la consulta quedaron
    # activos dentro del vocabulario aprendido.
    vector_consulta_df = pd.DataFrame(
        vector_consulta.toarray(),
        index=["Consulta"],
        columns=vocabulario,
    )
    # Cada similitud ya corresponde a un documento; preparar_resultados las
    # ordena para convertir el calculo en ranking.
    resultados = preparar_resultados(documentos, similitudes)

    if np.count_nonzero(vector_consulta.toarray()) == 0:
        st.warning(
            "La consulta no contiene terminos presentes en el vocabulario. Todas las similitudes seran 0."
        )

    mejor = resultados.iloc[0]
    vista_previa_mejor = crear_vista_previa(mejor["Texto"], 520)
    st.markdown(
        f"""
        <div class="top-result-card">
            <div class="top-result-kicker">Mejor coincidencia</div>
            <div class="top-result-title">
                {escapar(mejor["Documento"])} - {escapar(mejor["Tema"])}
            </div>
            <div class="preview-shell top-preview">
                <div class="preview-bar">
                    <span class="preview-dot"></span>
                    <span class="preview-title">Vista previa</span>
                </div>
                <div class="top-result-text">{escapar(vista_previa_mejor)}</div>
            </div>
            {construir_barra_puntaje(float(mejor["Similitud coseno"]))}
            <div class="score-label">
                Puntaje: {float(mejor["Similitud coseno"]):.4f} - {clasificar_similitud(float(mejor["Similitud coseno"]))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Documento mas similar", mejor["Documento"])
    col2.metric("Tema", mejor["Tema"])
    col3.metric("Puntaje", f"{mejor['Similitud coseno']:.4f}")

    st.subheader("Vector de la consulta")
    valores_consulta = vector_consulta_df.loc["Consulta"]
    # Se muestran solo pesos positivos porque los ceros significan que el
    # termino no participa en la comparacion coseno.
    terminos_consulta = valores_consulta[valores_consulta > 0].sort_values(ascending=False)
    if not terminos_consulta.empty:
        terminos_consulta = terminos_consulta.loc[
            sorted(
                terminos_consulta.index,
                key=lambda termino: (
                    -float(terminos_consulta[termino]),
                    *prioridad_visual_termino(termino),
                ),
            )
        ]
        chips_consulta = "".join(
            f'<span class="query-chip">{escapar(termino)}: {valor:.3f}</span>'
            for termino, valor in terminos_consulta.head(12).items()
        )
        st.markdown(
            f'<div class="pill-row">{chips_consulta}</div>',
            unsafe_allow_html=True,
        )
    columnas_vector_consulta = ordenar_columnas_por_valor(vector_consulta_df)
    st.dataframe(
        estilizar_tabla_oscura(vector_consulta_df.loc[:, columnas_vector_consulta].round(3)),
        width="stretch",
        height=calcular_altura_tabla(len(vector_consulta_df)),
    )

    st.subheader("Resultados ordenados")
    st.markdown(
        """
        <div class="small-note">
        Interpretacion: cercano a 1 significa alta similitud con la consulta. Cercano a 0 significa baja similitud.
        </div>
        """,
        unsafe_allow_html=True,
    )
    resultados_tabla = resultados.copy()
    resultados_tabla["Vista previa"] = resultados_tabla["Texto"].apply(
        lambda texto: crear_vista_previa(texto, 160)
    )
    resultados_tabla = resultados_tabla.drop(columns=["Texto"])
    columnas_resultados = [
        "Ranking",
        "Documento",
        "Tema",
        "Vista previa",
        "Similitud coseno",
    ]
    st.dataframe(
        estilizar_tabla_oscura(resultados_tabla[columnas_resultados]).format({"Similitud coseno": "{:.4f}"}),
        width="stretch",
        hide_index=True,
        height=calcular_altura_tabla(len(resultados_tabla)),
    )

    st.subheader("Ranking visual")
    for _, fila in resultados.head(5).iterrows():
        valor = float(fila["Similitud coseno"])
        st.markdown(
            f"""
            <div class="rank-card">
                <div class="rank-line">
                    <div class="rank-title">#{int(fila["Ranking"])} {escapar(fila["Documento"])} - {escapar(fila["Tema"])}</div>
                    <div class="rank-score">{valor:.4f}</div>
                </div>
                {construir_barra_puntaje(valor)}
                <div class="score-label">{clasificar_similitud(valor)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return resultados
