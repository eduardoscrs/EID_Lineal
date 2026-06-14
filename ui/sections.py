import html

import numpy as np
import pandas as pd
import streamlit as st

from logic.vector_model import calcular_similitud_consulta, preparar_resultados
from visualization.charts import (
    crear_grafico_barras_similitud,
    crear_mapa_calor_matriz,
    crear_grafico_terminos,
    crear_mapa_calor_documentos,
)


def escapar(texto: object) -> str:
    """Escapa texto antes de insertarlo en bloques HTML."""
    return html.escape(str(texto), quote=True)


def clasificar_similitud(valor: float) -> str:
    """Entrega una etiqueta simple para explicar el puntaje."""
    if valor >= 0.60:
        return "Alta similitud"
    if valor >= 0.25:
        return "Similitud media"
    return "Baja similitud"


def construir_barra_puntaje(valor: float) -> str:
    """Crea una barra HTML proporcional al puntaje de similitud."""
    ancho = max(0, min(100, valor * 100))
    return (
        '<div class="score-bar">'
        f'<div class="score-fill" style="width: {ancho:.1f}%"></div>'
        "</div>"
    )


def estilizar_tabla_oscura(dataframe: pd.DataFrame):
    """Aplica colores oscuros a tablas mostradas con Streamlit."""
    return (
        dataframe.style.set_properties(
            **{
                "background-color": "#0a1d2c",
                "color": "#e6f6f4",
                "border-color": "#1b4f69",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#0b2233"),
                        ("color", "#5eead4"),
                        ("border-color", "#1b4f69"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "#1b4f69"),
                    ],
                },
            ]
        )
    )


def mostrar_inicio(
    documentos: list[dict[str, str]],
    vocabulario: np.ndarray,
    matriz_documento_termino,
    tipo_vectorizador: str,
) -> None:
    """Seccion inicial con resumen y metricas principales."""
    st.markdown(
        """
        <div class="app-hero">
            <h1>Buscador Semantico Simple</h1>
            <p>Representacion vectorial de texto, matriz documento-termino y similitud coseno en una interfaz Streamlit.</p>
            <div class="hero-badges">
                <span class="hero-badge">Python</span>
                <span class="hero-badge">Streamlit</span>
                <span class="hero-badge">Scikit-learn</span>
                <span class="hero-badge">Algebra lineal aplicada</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-box">
        Esta aplicacion transforma documentos breves en vectores numericos. Luego convierte la consulta del usuario al mismo espacio vectorial y calcula que documentos son mas parecidos usando similitud coseno.
        </div>
        """,
        unsafe_allow_html=True,
    )

    valores_no_cero = matriz_documento_termino.count_nonzero()
    total_valores = matriz_documento_termino.shape[0] * matriz_documento_termino.shape[1]
    densidad = valores_no_cero / total_valores if total_valores else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Documentos", len(documentos))
    col2.metric("Terminos del vocabulario", len(vocabulario))
    col3.metric(
        "Dimension de la matriz",
        f"{matriz_documento_termino.shape[0]} x {matriz_documento_termino.shape[1]}",
    )
    col4.metric("Valores no cero", valores_no_cero)
    col5.metric("Densidad", f"{densidad:.1%}")

    st.caption(f"Vectorizador activo: {tipo_vectorizador}")

    st.subheader("Flujo de la aplicacion")
    st.markdown(
        """
        <div class="flow-grid">
            <div class="flow-step">
                <div class="flow-number">1</div>
                <div class="flow-title">Documentos</div>
                <div class="flow-text">Se cargan textos de ejemplo y textos agregados por el usuario.</div>
            </div>
            <div class="flow-step">
                <div class="flow-number">2</div>
                <div class="flow-title">Vocabulario</div>
                <div class="flow-text">El vectorizador identifica los terminos que forman las columnas.</div>
            </div>
            <div class="flow-step">
                <div class="flow-number">3</div>
                <div class="flow-title">Matriz</div>
                <div class="flow-text">Cada documento queda representado como un vector numerico.</div>
            </div>
            <div class="flow-step">
                <div class="flow-number">4</div>
                <div class="flow-title">Consulta</div>
                <div class="flow-text">La busqueda se transforma usando el mismo vocabulario.</div>
            </div>
            <div class="flow-step">
                <div class="flow-number">5</div>
                <div class="flow-title">Ranking</div>
                <div class="flow-text">La similitud coseno ordena los documentos mas cercanos.</div>
            </div>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )


def mostrar_documentos(documentos: list[dict[str, str]]) -> None:
    """Muestra los documentos disponibles para la busqueda."""
    st.header("Documentos cargados")
    st.caption("Estos textos forman el conjunto sobre el cual se realiza la busqueda.")

    documentos_df = pd.DataFrame(documentos)
    documentos_tabla = documentos_df.rename(
        columns={"nombre": "Documento", "tema": "Tema", "texto": "Texto"}
    )
    st.dataframe(
        estilizar_tabla_oscura(documentos_tabla),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Vista rapida en tarjetas")
    columnas = st.columns(2)
    for indice, documento in enumerate(documentos):
        cantidad_palabras = len(documento["texto"].split())
        tarjeta = f"""
        <div class="doc-card">
            <div class="doc-card-header">
                <span class="doc-name">{escapar(documento["nombre"])}</span>
                <span class="doc-topic">{escapar(documento["tema"])}</span>
            </div>
            <div class="doc-text">{escapar(documento["texto"])}</div>
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
        terminos_destacados = "".join(
            f'<span class="pill">{escapar(termino)}</span>'
            for termino in vocabulario[:30]
        )
        st.markdown(
            f'<div class="pill-row">{terminos_destacados}</div>',
            unsafe_allow_html=True,
        )
        vocabulario_df = pd.DataFrame({"Termino": vocabulario})
        st.dataframe(
            estilizar_tabla_oscura(vocabulario_df),
            use_container_width=True,
            hide_index=True,
            height=240,
        )

    st.subheader("Tabla de la matriz")
    st.dataframe(
        estilizar_tabla_oscura(matriz_df.round(3)),
        use_container_width=True,
        height=380,
    )


def mostrar_buscador(
    documentos: list[dict[str, str]],
    vectorizador,
    matriz_documento_termino,
    vocabulario: np.ndarray,
) -> pd.DataFrame | None:
    """Permite ingresar una consulta y calcula resultados de similitud."""
    st.header("Buscador")
    st.caption("Escribe una consulta y la aplicacion la comparara con todos los documentos.")

    consulta = st.text_input(
        "Consulta de busqueda",
        placeholder="Ejemplo: inteligencia artificial",
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

    vector_consulta, similitudes = calcular_similitud_consulta(
        vectorizador=vectorizador,
        consulta=consulta,
        matriz_documento_termino=matriz_documento_termino,
    )
    vector_consulta_df = pd.DataFrame(
        vector_consulta.toarray(),
        index=["Consulta"],
        columns=vocabulario,
    )
    resultados = preparar_resultados(documentos, similitudes)

    if np.count_nonzero(vector_consulta.toarray()) == 0:
        st.warning(
            "La consulta no contiene terminos presentes en el vocabulario. Todas las similitudes seran 0."
        )

    mejor = resultados.iloc[0]
    st.markdown(
        f"""
        <div class="top-result-card">
            <div class="top-result-kicker">Mejor coincidencia</div>
            <div class="top-result-title">
                {escapar(mejor["Documento"])} - {escapar(mejor["Tema"])}
            </div>
            <div class="top-result-text">{escapar(mejor["Texto"])}</div>
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
    terminos_consulta = valores_consulta[valores_consulta > 0].sort_values(ascending=False)
    if not terminos_consulta.empty:
        chips_consulta = "".join(
            f'<span class="query-chip">{escapar(termino)}: {valor:.3f}</span>'
            for termino, valor in terminos_consulta.head(12).items()
        )
        st.markdown(
            f'<div class="pill-row">{chips_consulta}</div>',
            unsafe_allow_html=True,
        )
    st.dataframe(
        estilizar_tabla_oscura(vector_consulta_df.round(3)),
        use_container_width=True,
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
    st.dataframe(
        estilizar_tabla_oscura(resultados).format({"Similitud coseno": "{:.4f}"}),
        use_container_width=True,
        hide_index=True,
        height=420,
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


def mostrar_graficos(
    matriz_df: pd.DataFrame,
    matriz_documento_termino,
    etiquetas_documentos: list[str],
    tipo_vectorizador: str,
    resultados: pd.DataFrame | None,
) -> None:
    """Muestra las visualizaciones principales de apoyo."""
    st.header("Graficos")

    grafico_terminos, matriz_visual, mapa_calor, grafico_consulta = st.tabs(
        [
            "Terminos principales",
            "Matriz visual",
            "Similitud entre documentos",
            "Similitud con consulta",
        ]
    )

    with grafico_terminos:
        st.pyplot(crear_grafico_terminos(matriz_df, tipo_vectorizador), clear_figure=True)

    with matriz_visual:
        st.pyplot(
            crear_mapa_calor_matriz(matriz_df, tipo_vectorizador),
            clear_figure=True,
        )

    with mapa_calor:
        st.pyplot(
            crear_mapa_calor_documentos(matriz_documento_termino, etiquetas_documentos),
            clear_figure=True,
        )

    with grafico_consulta:
        if resultados is None:
            st.info("Ingresa una consulta en la seccion Buscador para ver este grafico.")
        else:
            st.pyplot(crear_grafico_barras_similitud(resultados), clear_figure=True)


def mostrar_funcionamiento(tipo_vectorizador: str) -> None:
    """Explicacion breve dentro de la app, sin formato de informe."""
    st.header("Funcionamiento interno")
    st.markdown(
        f"""
        Esta aplicacion usa **{tipo_vectorizador}** para transformar texto en numeros.

        **Documento-termino:** cada documento se representa como una fila y cada termino como una columna.

        **Vector de consulta:** cuando escribes una busqueda, se crea un vector con el mismo vocabulario de la matriz.

        **Similitud coseno:** mide el angulo entre el vector de la consulta y el vector de cada documento.
        Si el valor esta cerca de **1**, los vectores apuntan en una direccion parecida y los textos son mas similares.
        Si el valor esta cerca de **0**, comparten poca informacion relevante.
        """
    )
