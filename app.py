import streamlit as st

from data.example_documents import DOCUMENTOS_EJEMPLO
from logic.vector_model import (
    calcular_similitud_consulta,
    generar_modelo_vectorial,
    matriz_a_dataframe,
    preparar_resultados,
)
from ui.sections import (
    mostrar_buscador,
    mostrar_cierre,
    mostrar_documentos,
    mostrar_graficos,
    mostrar_marco_recorrido,
    mostrar_matriz,
    mostrar_metodo_vectorial,
    mostrar_portada,
)
from ui.sidebar import mostrar_sidebar
from ui.styles import configurar_pagina


PASOS_PRESENTACION = [
    "Elegir metodo",
    "Entender el metodo",
    "Revisar documentos",
    "Construir matriz",
    "Probar busqueda",
    "Leer graficos",
    "Cerrar idea",
]


def inicializar_estado() -> None:
    """Crea las variables de sesion necesarias."""
    if "documentos_usuario" not in st.session_state:
        st.session_state.documentos_usuario = []
    if "tipo_vectorizador" not in st.session_state:
        st.session_state.tipo_vectorizador = None
    if "eliminar_stop_words" not in st.session_state:
        st.session_state.eliminar_stop_words = True
    if "paso_actual" not in st.session_state:
        st.session_state.paso_actual = 0
    if "consulta_busqueda" not in st.session_state:
        st.session_state.consulta_busqueda = ""


def construir_documentos() -> list[dict[str, str]]:
    """Une los documentos base con los documentos agregados desde la interfaz."""
    return DOCUMENTOS_EJEMPLO + st.session_state.documentos_usuario


def normalizar_paso() -> None:
    """Evita estados fuera del recorrido disponible."""
    paso_maximo = len(PASOS_PRESENTACION) - 1
    if st.session_state.tipo_vectorizador is None:
        st.session_state.paso_actual = 0
        return
    st.session_state.paso_actual = max(0, min(st.session_state.paso_actual, paso_maximo))


def aplicar_eleccion_vectorizador(tipo_vectorizador: str) -> None:
    """Guarda el metodo elegido y avanza a la pantalla explicativa."""
    st.session_state.tipo_vectorizador = tipo_vectorizador
    st.session_state.paso_actual = 1
    st.rerun()


def calcular_resultados_guardados(documentos, vectorizador, matriz_documento_termino):
    """Recalcula el ranking cuando existe una consulta persistida."""
    consulta = st.session_state.get("consulta_busqueda", "")
    if not consulta.strip():
        return None

    _, similitudes = calcular_similitud_consulta(
        vectorizador=vectorizador,
        consulta=consulta,
        matriz_documento_termino=matriz_documento_termino,
    )
    return preparar_resultados(documentos, similitudes)


def mostrar_controles_recorrido() -> None:
    """Botones inferiores para moverse como en una presentacion."""
    paso_actual = st.session_state.paso_actual
    ultimo_paso = len(PASOS_PRESENTACION) - 1
    puede_avanzar = st.session_state.tipo_vectorizador is not None and paso_actual < ultimo_paso

    st.markdown('<div class="presentation-controls">', unsafe_allow_html=True)
    col_anterior, col_estado, col_siguiente = st.columns([1, 2.4, 1])

    with col_anterior:
        if st.button("Anterior", use_container_width=True, disabled=paso_actual == 0):
            st.session_state.paso_actual = max(0, paso_actual - 1)
            st.rerun()

    with col_estado:
        st.markdown(
            f"""
            <div class="step-caption">
                Pantalla {paso_actual + 1} de {len(PASOS_PRESENTACION)} -
                {PASOS_PRESENTACION[paso_actual]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_siguiente:
        if st.button("Siguiente", use_container_width=True, disabled=not puede_avanzar):
            st.session_state.paso_actual = min(ultimo_paso, paso_actual + 1)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    configurar_pagina()
    inicializar_estado()
    normalizar_paso()

    eliminar_stop_words = mostrar_sidebar(PASOS_PRESENTACION)
    documentos = construir_documentos()
    etiquetas_documentos = [documento["nombre"] for documento in documentos]
    tipo_vectorizador = st.session_state.tipo_vectorizador

    if tipo_vectorizador is None:
        eleccion = mostrar_portada(documentos=documentos, tipo_vectorizador=None)
        if eleccion is not None:
            aplicar_eleccion_vectorizador(eleccion)
        return

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
    resultados = calcular_resultados_guardados(
        documentos=documentos,
        vectorizador=vectorizador,
        matriz_documento_termino=matriz_documento_termino,
    )

    mostrar_marco_recorrido(
        pasos=PASOS_PRESENTACION,
        paso_actual=st.session_state.paso_actual,
        tipo_vectorizador=tipo_vectorizador,
    )

    if st.session_state.paso_actual == 0:
        eleccion = mostrar_portada(documentos=documentos, tipo_vectorizador=tipo_vectorizador)
        if eleccion is not None:
            aplicar_eleccion_vectorizador(eleccion)
    elif st.session_state.paso_actual == 1:
        mostrar_metodo_vectorial(
            tipo_vectorizador=tipo_vectorizador,
            eliminar_stop_words=eliminar_stop_words,
            documentos=documentos,
            vocabulario=vocabulario,
            matriz_documento_termino=matriz_documento_termino,
        )
    elif st.session_state.paso_actual == 2:
        mostrar_documentos(documentos)
    elif st.session_state.paso_actual == 3:
        mostrar_matriz(matriz_df, vocabulario, tipo_vectorizador)
    elif st.session_state.paso_actual == 4:
        resultados = mostrar_buscador(
            documentos=documentos,
            vectorizador=vectorizador,
            matriz_documento_termino=matriz_documento_termino,
            vocabulario=vocabulario,
        )
    elif st.session_state.paso_actual == 5:
        mostrar_graficos(
            matriz_df=matriz_df,
            matriz_documento_termino=matriz_documento_termino,
            etiquetas_documentos=etiquetas_documentos,
            tipo_vectorizador=tipo_vectorizador,
            resultados=resultados,
        )
    else:
        mostrar_cierre(tipo_vectorizador, eliminar_stop_words, resultados)

    mostrar_controles_recorrido()


if __name__ == "__main__":
    main()
