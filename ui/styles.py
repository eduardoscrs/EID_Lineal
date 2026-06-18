from pathlib import Path

import streamlit as st


THEME_PATH = Path(__file__).with_name("theme.css")


def configurar_pagina() -> None:
    """Configura la pagina y aplica estilos visuales."""
    st.set_page_config(
        page_title="Buscador Vectorial",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    estilos = THEME_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>\n{estilos}\n</style>", unsafe_allow_html=True)
