import streamlit as st


def mostrar_sidebar(pasos: list[str]) -> bool:
    """Renderiza el panel lateral de apoyo para la presentacion."""
    st.sidebar.header("Panel de exposicion")

    tipo_actual = st.session_state.tipo_vectorizador
    if tipo_actual is None:
        st.sidebar.info("El recorrido parte eligiendo TF-IDF o CountVectorizer.")
    else:
        st.sidebar.caption("Metodo activo")
        tipo_vectorizador = st.sidebar.selectbox(
            "Representacion vectorial",
            options=["TF-IDF", "CountVectorizer"],
            index=["TF-IDF", "CountVectorizer"].index(tipo_actual),
            help="TF-IDF pondera terminos relevantes. CountVectorizer cuenta apariciones.",
        )
        if tipo_vectorizador != tipo_actual:
            st.session_state.tipo_vectorizador = tipo_vectorizador
            st.rerun()

    st.sidebar.checkbox(
        "Eliminar palabras comunes",
        key="eliminar_stop_words",
        help="Quita conectores frecuentes como 'de', 'la', 'y' para una matriz mas clara.",
    )

    st.sidebar.divider()
    if st.session_state.tipo_vectorizador is not None:
        paso_elegido = st.sidebar.radio(
            "Recorrido",
            options=list(range(len(pasos))),
            format_func=lambda indice: f"{indice + 1}. {pasos[indice]}",
            index=st.session_state.paso_actual,
        )
        if paso_elegido != st.session_state.paso_actual:
            st.session_state.paso_actual = paso_elegido
            st.rerun()

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

    return st.session_state.eliminar_stop_words
