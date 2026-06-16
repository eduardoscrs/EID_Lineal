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
                "background-color": "#fffaf1",
                "color": "#1f2933",
                "border-color": "#ded6c9",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#16202a"),
                        ("color", "#fff7ed"),
                        ("border-color", "#ded6c9"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "#ded6c9"),
                    ],
                },
            ]
        )
    )


def obtener_perfil_vectorizador(tipo_vectorizador: str) -> dict[str, str]:
    """Textos cortos para explicar el metodo elegido."""
    if tipo_vectorizador == "TF-IDF":
        return {
            "titulo": "TF-IDF",
            "subtitulo": "Da mas peso a las palabras que distinguen a un documento.",
            "idea": "Una palabra vale mas cuando aparece en un documento, pero no aparece tanto en todos los demas.",
            "matriz": "Las celdas son pesos decimales. Un numero alto indica que el termino ayuda a identificar ese texto.",
            "uso": "Conviene cuando importa encontrar terminos representativos, no solo contar repeticiones.",
            "formula": "peso = frecuencia del termino x rareza en el corpus",
        }

    return {
        "titulo": "CountVectorizer",
        "subtitulo": "Cuenta cuantas veces aparece cada palabra en cada documento.",
        "idea": "Una palabra vale mas si se repite mas dentro del documento.",
        "matriz": "Las celdas son conteos enteros. Un numero alto indica mas apariciones del termino.",
        "uso": "Conviene cuando se quiere una lectura directa y facil de explicar en la matriz.",
        "formula": "peso = numero de apariciones del termino",
    }


def mostrar_marco_recorrido(
    pasos: list[str],
    paso_actual: int,
    tipo_vectorizador: str,
) -> None:
    """Muestra el encabezado fijo del recorrido tipo presentacion."""
    progreso = (paso_actual / (len(pasos) - 1)) * 100 if len(pasos) > 1 else 0
    etiquetas = []

    for indice, paso in enumerate(pasos):
        estado = "done" if indice < paso_actual else "active" if indice == paso_actual else ""
        etiquetas.append(
            f'<div class="stepper-item {estado}">'
            f'<span class="stepper-number">{indice + 1}</span>'
            f'<span class="stepper-label">{escapar(paso)}</span>'
            "</div>"
        )

    st.markdown(
        f"""
        <div class="story-shell">
            <div>
                <div class="story-kicker">Recorrido de presentacion</div>
                <div class="story-title">{escapar(tipo_vectorizador)} en una busqueda vectorial</div>
            </div>
            <div class="story-progress-label">{progreso:.0f}%</div>
        </div>
        <div class="progress-track"><div class="progress-fill" style="width: {progreso:.1f}%"></div></div>
        <div class="stepper-row">{''.join(etiquetas)}</div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_portada(
    documentos: list[dict[str, str]],
    tipo_vectorizador: str | None,
) -> str | None:
    """Pantalla inicial para elegir el tipo de representacion."""
    st.markdown(
        """
        <section class="presentation-hero">
            <div class="hero-copy">
                <div class="hero-kicker">Algebra lineal aplicada a texto</div>
                <h1>Buscador vectorial de documentos</h1>
                <p>
                    Una presentacion interactiva para mostrar como un texto se transforma en
                    un vector, como nace la matriz documento-termino y como se calcula la
                    similitud coseno.
                </p>
            </div>
            <div class="hero-panel">
                <div class="hero-panel-number">2</div>
                <div class="hero-panel-text">metodos para comparar el mismo corpus</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Documentos base", len(documentos))
    col2.metric("Metodos", "TF-IDF / Count")
    col3.metric("Salida", "Ranking por similitud")

    st.markdown('<div class="section-eyebrow">Primera decision</div>', unsafe_allow_html=True)
    st.subheader("Elige como se convertiran las palabras en numeros")

    actual = tipo_vectorizador or "Sin seleccion"
    st.caption(f"Seleccion actual: {actual}")

    eleccion = None
    columna_tfidf, columna_count = st.columns(2)

    with columna_tfidf:
        st.markdown(
            """
            <div class="choice-card tfidf-card">
                <div class="choice-label">Opcion A</div>
                <h3>TF-IDF</h3>
                <p>TF-IDF significa Term Frequency - Inverse Document Frequency. Es una técnica que no solo cuenta cuántas veces aparece una palabra, sino que también analiza qué tan importante o distintiva es dentro del conjunto de documentos.

La idea es que una palabra será más importante si aparece mucho en un documento, pero no aparece en todos los demás documentos.

Por ejemplo, palabras muy comunes como “el”, “la”, “de” o “y” pueden aparecer muchas veces, pero no ayudan mucho a diferenciar un documento de otro. En cambio, palabras como “inteligencia artificial”, “ciberseguridad” o “Python” pueden ser más útiles porque representan mejor el tema del documento.

TF-IDF baja el peso de las palabras demasiado comunes y aumenta el peso de las palabras más representativas o específicas.</p>
                <div class="choice-formula">frecuencia x rareza</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Elegir TF-IDF", use_container_width=True, type="primary"):
            eleccion = "TF-IDF"

    with columna_count:
        st.markdown(
            """
            <div class="choice-card count-card">
                <div class="choice-label">Opcion B</div>
                <h3>CountVectorizer</h3>
                <p>convierte cada documento en un vector contando cuántas veces aparece cada palabra del vocabulario.

En esta representación, cada fila corresponde a un documento y cada columna corresponde a una palabra. El valor de cada celda indica la cantidad de veces que esa palabra aparece en ese documento.

Por ejemplo, si la palabra “Python” aparece 3 veces en un documento, en la matriz aparecerá el valor 3 para esa palabra.

Este método es útil para explicar la matriz documento-término de forma directa, porque los valores representan frecuencias reales de palabras. Sin embargo, tiene una limitación: puede darle mucha importancia a palabras que aparecen muchas veces, aunque no sean tan relevantes para entender el contenido del texto.</p>
                <div class="choice-formula">numero de apariciones</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Elegir CountVectorizer", use_container_width=True):
            eleccion = "CountVectorizer"

    return eleccion


def mostrar_metodo_vectorial(
    documentos: list[dict[str, str]],
    vocabulario: np.ndarray,
    matriz_documento_termino,
    tipo_vectorizador: str,
    eliminar_stop_words: bool,
) -> None:
    """Explica el metodo elegido como segunda pantalla del recorrido."""
    perfil = obtener_perfil_vectorizador(tipo_vectorizador)
    valores_no_cero = matriz_documento_termino.count_nonzero()
    total_valores = matriz_documento_termino.shape[0] * matriz_documento_termino.shape[1]
    densidad = valores_no_cero / total_valores if total_valores else 0

    st.markdown(
        f"""
        <div class="method-hero">
            <div class="section-eyebrow">Metodo elegido</div>
            <h1>{escapar(perfil["titulo"])}</h1>
            <p>{escapar(perfil["subtitulo"])}</p>
            <div class="method-formula">{escapar(perfil["formula"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Documentos", len(documentos))
    col2.metric("Terminos del vocabulario", len(vocabulario))
    col3.metric(
        "Dimension de la matriz",
        f"{matriz_documento_termino.shape[0]} x {matriz_documento_termino.shape[1]}",
    )
    col4.metric("Valores no cero", valores_no_cero)
    col5.metric("Densidad", f"{densidad:.1%}")

    st.markdown(
        f"""
        <div class="explain-grid">
            <div class="explain-card">
                <div class="explain-title">Idea central</div>
                <div class="explain-text">{escapar(perfil["idea"])}</div>
            </div>
            <div class="explain-card">
                <div class="explain-title">Como se lee la matriz</div>
                <div class="explain-text">{escapar(perfil["matriz"])}</div>
            </div>
            <div class="explain-card">
                <div class="explain-title">Cuando conviene</div>
                <div class="explain-text">{escapar(perfil["uso"])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    estado_stop_words = "activada" if eliminar_stop_words else "desactivada"
    st.markdown(
        f"""
        <div class="info-box">
        Limpieza de palabras comunes: <strong>{estado_stop_words}</strong>. Esta opcion ayuda a que conectores como
        "de", "la" o "y" no dominen la matriz.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Flujo que se mostrara en la exposicion")
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
    st.markdown('<div class="section-eyebrow">Corpus de trabajo</div>', unsafe_allow_html=True)
    st.header("Documentos que alimentan el modelo")
    st.caption(
        "Cada texto sera una fila de la matriz. El tema ayuda a verificar si el ranking final tiene sentido."
    )

    documentos_df = pd.DataFrame(documentos)
    documentos_tabla = documentos_df.rename(
        columns={"nombre": "Documento", "tema": "Tema", "texto": "Texto"}
    )
    st.dataframe(
        estilizar_tabla_oscura(documentos_tabla),
        width="stretch",
        hide_index=True,
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
            width="stretch",
            hide_index=True,
            height=240,
        )

    st.subheader("Tabla de la matriz")
    st.dataframe(
        estilizar_tabla_oscura(matriz_df.round(3)),
        width="stretch",
        height=380,
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
        width="stretch",
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
        width="stretch",
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
    else:
        st.info("La pantalla de busqueda todavia no tiene una consulta guardada.")
