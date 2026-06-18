import numpy as np
import streamlit as st

from ui.view_helpers import escapar, obtener_perfil_vectorizador


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
