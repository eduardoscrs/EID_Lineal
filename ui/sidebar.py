import streamlit as st


def mostrar_sidebar() -> tuple[str, bool]:
    """Renderiza configuracion, selector de vectorizador y carga manual."""
    st.sidebar.header("Configuracion")
    tipo_vectorizador = st.sidebar.radio(
        "Representacion vectorial",
        options=["TF-IDF", "CountVectorizer"],
        help="TF-IDF pondera terminos relevantes. CountVectorizer cuenta apariciones.",
    )
    eliminar_stop_words = st.sidebar.checkbox(
        "Eliminar palabras comunes",
        value=True,
        help="Quita conectores frecuentes como 'de', 'la', 'y' para una matriz mas clara.",
    )

    st.sidebar.divider()
    st.sidebar.subheader("Agregar documento")
    with st.sidebar.form("formulario_documento", clear_on_submit=True):
        tema = st.text_input("Nombre o tema", placeholder="Ejemplo: Astronomia")
        texto = st.text_area(
            "Texto breve",
            placeholder="Escribe aqui un documento corto para agregarlo al buscador.",
            height=120,
        )
        agregar = st.form_submit_button("Agregar documento")

    if agregar:
        if texto.strip():
            numero = len(st.session_state.documentos_usuario) + 1
            st.session_state.documentos_usuario.append(
                {
                    "nombre": f"Doc extra {numero}",
                    "tema": tema.strip() or f"Documento agregado {numero}",
                    "texto": texto.strip(),
                }
            )
            st.sidebar.success("Documento agregado correctamente.")
        else:
            st.sidebar.warning("Escribe un texto antes de agregar el documento.")

    if st.session_state.documentos_usuario:
        st.sidebar.caption(
            f"Documentos agregados en esta sesion: {len(st.session_state.documentos_usuario)}"
        )
        if st.sidebar.button("Quitar documentos agregados"):
            st.session_state.documentos_usuario = []
            st.rerun()

    return tipo_vectorizador, eliminar_stop_words
