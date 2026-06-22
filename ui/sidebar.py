import streamlit as st

from logic.document_loader import FORMATOS_SOPORTADOS, extraer_texto_archivo


def mostrar_sidebar(_pasos: list[str]) -> bool:
    """Renderiza el panel lateral de apoyo para la presentacion."""
    st.sidebar.header("Documentos")
    st.sidebar.caption("Sube archivos o agrega textos para armar el corpus de busqueda.")

    st.sidebar.subheader("Subir documentos")
    archivos_subidos = st.sidebar.file_uploader(
        "Subir documento(s)",
        type=list(FORMATOS_SOPORTADOS),
        accept_multiple_files=True,
        key=f"subir_documentos_{st.session_state.subidor_archivos_version}",
        help="Permite seleccionar varios archivos txt, md, csv, pdf o docx.",
    )

    nuevos_archivos = 0
    errores_archivos = []
    procesados = st.session_state.archivos_documentos_procesados

    for archivo in archivos_subidos:
        clave_archivo = f"{archivo.name}:{archivo.size}"
        if clave_archivo in procesados:
            continue

        try:
            texto_archivo = extraer_texto_archivo(archivo.name, archivo.getvalue())
        except (RuntimeError, ValueError) as error:
            errores_archivos.append(f"{archivo.name}: {error}")
            procesados.append(clave_archivo)
            continue

        numero = len(st.session_state.documentos_usuario) + 1
        st.session_state.documentos_usuario.append(
            {
                "nombre": f"Doc extra {numero}",
                "tema": archivo.name,
                "texto": texto_archivo,
            }
        )
        procesados.append(clave_archivo)
        nuevos_archivos += 1

    if nuevos_archivos:
        st.sidebar.success(f"{nuevos_archivos} documento(s) subido(s) correctamente.")

    if errores_archivos:
        st.sidebar.warning("No se pudieron cargar: " + "; ".join(errores_archivos))

    st.sidebar.divider()
    st.sidebar.subheader("Añadir texto")
    with st.sidebar.form("formulario_documento", clear_on_submit=True):
        tema = st.text_input("Nombre o tema", placeholder="Ejemplo: Astronomia")
        texto = st.text_area(
            "Texto breve",
            placeholder="Escribe aqui un documento corto para agregarlo al buscador.",
            height=120,
        )
        agregar = st.form_submit_button("Añadir texto")

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
            st.sidebar.success("Texto añadido correctamente.")
        else:
            st.sidebar.warning("Escribe un texto antes de agregar el documento.")

    if st.session_state.documentos_usuario:
        st.sidebar.caption(
            f"Documentos añadidos en esta sesion: {len(st.session_state.documentos_usuario)}"
        )
        if st.sidebar.button("Quitar documentos añadidos"):
            st.session_state.documentos_usuario = []
            st.session_state.archivos_documentos_procesados = []
            st.session_state.subidor_archivos_version += 1
            st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Opciones")
    tipo_actual = st.session_state.tipo_vectorizador
    if tipo_actual is not None:
        tipo_vectorizador = st.sidebar.selectbox(
            "Representacion vectorial",
            options=["TF-IDF", "CountVectorizer"],
            index=["TF-IDF", "CountVectorizer"].index(tipo_actual),
            help="TF-IDF pondera terminos relevantes. CountVectorizer cuenta apariciones.",
        )
        if tipo_vectorizador != tipo_actual:
            st.session_state.tipo_vectorizador = tipo_vectorizador
            st.session_state.subir_vista = True
            st.rerun()

    st.sidebar.checkbox(
        "Eliminar palabras comunes",
        key="eliminar_stop_words",
        help="Quita conectores frecuentes como 'de', 'la', 'y' para una matriz mas clara.",
    )
    st.sidebar.checkbox(
        "Documentos de ejemplo",
        key="usar_documentos_ejemplo",
        help="Agrega 10 documentos de ejemplos.",
    )

    return st.session_state.eliminar_stop_words
