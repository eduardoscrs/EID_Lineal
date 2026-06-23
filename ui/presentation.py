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
        """,
        unsafe_allow_html=True,
    )
    columnas = st.columns(len(pasos))
    for indice, paso in enumerate(pasos):
        tipo_boton = "primary" if indice == paso_actual else "secondary"
        with columnas[indice]:
            if st.button(
                f"{indice + 1}. {paso}",
                key=f"paso_presentacion_{indice}",
                use_container_width=True,
                type=tipo_boton,
            ):
                st.session_state.paso_actual = indice
                st.session_state.subir_vista = True
                st.rerun()


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
                <div class="hero-title-main">Buscador vectorial de documentos</div>
                <p>
                    Una presentacion interactiva para mostrar como un texto se transforma en
                    un vector, como nace la matriz documento-termino y como se calcula la
                    similitud coseno.
                </p>
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
    tfidf_activo = tipo_vectorizador == "TF-IDF"
    count_activo = tipo_vectorizador == "CountVectorizer"
    clase_tfidf = "choice-card tfidf-card selected-choice" if tfidf_activo else "choice-card tfidf-card"
    clase_count = "choice-card count-card selected-choice" if count_activo else "choice-card count-card"

    with columna_tfidf:
        st.markdown(
            f"""
            <div class="{clase_tfidf}">
                <div class="choice-label">Opcion A</div>
                <h3>TF-IDF</h3>
                <p>Da mas peso a las palabras que aparecen en un documento, pero no en todos. Es util para destacar terminos distintivos dentro del corpus.</p>
                <div class="choice-formula">frecuencia x rareza</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        tipo_boton_tfidf = "primary" if tfidf_activo or tipo_vectorizador is None else "secondary"
        if st.button("Elegir TF-IDF", use_container_width=True, type=tipo_boton_tfidf):
            eleccion = "TF-IDF"

    with columna_count:
        st.markdown(
            f"""
            <div class="{clase_count}">
                <div class="choice-label">Opcion B</div>
                <h3>CountVectorizer</h3>
                <p>Cuenta cuantas veces aparece cada palabra. Es la forma mas directa para mostrar la matriz documento-termino y leer frecuencias reales.</p>
                <div class="choice-formula">numero de apariciones</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        tipo_boton_count = "primary" if count_activo else "secondary"
        if st.button("Elegir CountVectorizer", use_container_width=True, type=tipo_boton_count):
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
    # Estos numeros resumen la matriz construida: dimension, celdas activas
    # y densidad para explicar cuan dispersa queda la representacion.
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
