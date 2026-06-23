import numpy as np
import pandas as pd
import streamlit as st

from logic.vector_model import calcular_similitud_consulta, preparar_resultados
from ui.view_helpers import calcular_altura_tabla, escapar, estilizar_tabla_oscura


CONSULTAS_ANALISIS_PREDETERMINADAS = [
    "inteligencia artificial",
    "programacion con datos",
    "deporte de equipo",
    "seguridad en redes",
    "musica y arte",
    "sistemas de recomendacion",
]


def obtener_consultas_analisis() -> list[str]:
    """Lee las consultas configuradas para el analisis experimental."""
    if "consultas_analisis" not in st.session_state:
        st.session_state.consultas_analisis = "\n".join(CONSULTAS_ANALISIS_PREDETERMINADAS)

    consultas_texto = st.text_area(
        "Consultas de prueba",
        key="consultas_analisis",
        height=150,
        help="Escribe una consulta por linea para generar la tabla de evidencia del informe.",
    )
    return [consulta.strip() for consulta in consultas_texto.splitlines() if consulta.strip()]


def clasificar_calidad_resultado(similitud: float, margen: float) -> str:
    """Clasifica una busqueda con umbrales simples para el analisis del informe."""
    if similitud <= 0:
        return "Sin coincidencia"
    if similitud >= 0.35 and margen >= 0.05:
        return "Buena"
    if similitud >= 0.15:
        return "Media"
    return "Debil"


def interpretar_resultado_consulta(
    consulta: str,
    mejor: pd.Series,
    segundo: pd.Series | None,
    similitud: float,
    margen: float,
) -> str:
    """Genera una lectura breve y reutilizable para el informe."""
    if similitud <= 0:
        return (
            f"La consulta '{consulta}' no comparte terminos con el vocabulario generado, "
            "por eso el modelo no logra recuperar un documento relevante."
        )

    if segundo is None:
        comparacion = "no hay un segundo documento para comparar."
    elif margen < 0.05:
        comparacion = (
            f"queda muy cerca de {segundo['Documento']}, lo que indica una busqueda ambigua "
            "o vocabulario compartido entre documentos."
        )
    else:
        comparacion = (
            f"queda por encima de {segundo['Documento']} con una diferencia de {margen:.4f}, "
            "lo que da una separacion razonable entre el primer y segundo resultado."
        )

    return (
        f"La consulta '{consulta}' recupera como primer resultado {mejor['Documento']} "
        f"({mejor['Tema']}) con similitud {similitud:.4f}; {comparacion}"
    )


def calcular_evidencia_consultas(
    documentos: list[dict[str, str]],
    vectorizador,
    matriz_documento_termino,
    consultas: list[str],
) -> pd.DataFrame:
    """Calcula una tabla de resultados para varias consultas."""
    filas = []
    for consulta in consultas:
        # Repite el mismo calculo de similitud para cada consulta de prueba.
        _, similitudes = calcular_similitud_consulta(
            vectorizador=vectorizador,
            consulta=consulta,
            matriz_documento_termino=matriz_documento_termino,
        )
        resultados_consulta = preparar_resultados(documentos, similitudes)
        mejor = resultados_consulta.iloc[0]
        segundo = resultados_consulta.iloc[1] if len(resultados_consulta) > 1 else None
        similitud_mejor = float(mejor["Similitud coseno"])
        similitud_segundo = float(segundo["Similitud coseno"]) if segundo is not None else 0.0
        # Margen = diferencia entre el primer y segundo resultado. Mientras
        # mas alto, menos ambigua fue la recuperacion.
        margen = similitud_mejor - similitud_segundo

        filas.append(
            {
                "Consulta": consulta,
                "Documento recuperado": mejor["Documento"],
                "Tema": mejor["Tema"],
                "Similitud": similitud_mejor,
                "Segundo documento": segundo["Documento"] if segundo is not None else "-",
                "Similitud segundo": similitud_segundo,
                "Margen": margen,
                "Calidad": clasificar_calidad_resultado(similitud_mejor, margen),
                "Interpretacion": interpretar_resultado_consulta(
                    consulta=consulta,
                    mejor=mejor,
                    segundo=segundo,
                    similitud=similitud_mejor,
                    margen=margen,
                ),
            }
        )

    return pd.DataFrame(filas)


def mostrar_analisis_evidencia(
    documentos: list[dict[str, str]],
    vectorizador,
    matriz_documento_termino,
    matriz_df: pd.DataFrame,
    vocabulario: np.ndarray,
) -> None:
    """Genera evidencia experimental e interpretacion lista para informe."""
    st.markdown('<div class="section-eyebrow">Analisis experimental</div>', unsafe_allow_html=True)
    st.header("Evidencia lista para el informe")
    st.caption(
        "Esta pantalla genera consultas de prueba, interpreta los resultados y deja una tabla exportable para el informe."
    )

    consultas = obtener_consultas_analisis()
    if not consultas:
        st.warning("Agrega al menos una consulta para generar la evidencia.")
        return

    evidencia_df = calcular_evidencia_consultas(
        documentos=documentos,
        vectorizador=vectorizador,
        matriz_documento_termino=matriz_documento_termino,
        consultas=consultas,
    )
    # Proporcion de celdas no cero en la matriz documento-termino.
    densidad = (matriz_df.to_numpy() != 0).sum() / matriz_df.size if matriz_df.size else 0
    promedio_similitud = float(evidencia_df["Similitud"].mean())
    sin_coincidencia = int((evidencia_df["Similitud"] == 0).sum())
    buena_calidad = int((evidencia_df["Calidad"] == "Buena").sum())

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Consultas", len(evidencia_df))
    col2.metric("Vocabulario", len(vocabulario))
    col3.metric("Dimension matriz", f"{matriz_df.shape[0]} x {matriz_df.shape[1]}")
    col4.metric("Densidad", f"{densidad:.1%}")
    col5.metric("Promedio similitud", f"{promedio_similitud:.4f}")

    st.subheader("Tabla de busquedas para reportar")
    columnas_tabla = [
        "Consulta",
        "Documento recuperado",
        "Tema",
        "Similitud",
        "Segundo documento",
        "Similitud segundo",
        "Margen",
        "Calidad",
    ]
    st.dataframe(
        estilizar_tabla_oscura(evidencia_df[columnas_tabla]).format(
            {
                "Similitud": "{:.4f}",
                "Similitud segundo": "{:.4f}",
                "Margen": "{:.4f}",
            }
        ),
        width="stretch",
        hide_index=True,
        height=calcular_altura_tabla(len(evidencia_df), maximo_filas=12),
    )

    st.subheader("Interpretacion por consulta")
    for _, fila in evidencia_df.iterrows():
        st.markdown(
            f"""
            <div class="rank-card">
                <div class="rank-line">
                    <div class="rank-title">{escapar(fila["Consulta"])}</div>
                    <div class="rank-score">{float(fila["Similitud"]):.4f}</div>
                </div>
                <div class="score-label">{escapar(fila["Interpretacion"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Analisis critico")
    sparsidad = 1 - densidad
    lectura_vocabulario = (
        "La matriz es dispersa: la mayoria de las celdas queda en cero porque cada documento usa solo una parte del vocabulario."
        if sparsidad >= 0.75
        else "La matriz tiene una densidad relativamente alta para un corpus pequeno, lo que facilita comparar documentos."
    )
    lectura_resultados = (
        f"{buena_calidad} de {len(evidencia_df)} consultas tuvieron una separacion clara entre el primer y segundo resultado."
        if buena_calidad
        else "Ninguna consulta logro una separacion fuerte; conviene revisar vocabulario, longitud de documentos o terminos usados."
    )
    lectura_sin_coincidencia = (
        f"{sin_coincidencia} consulta(s) no compartieron terminos con el vocabulario y quedaron con similitud 0."
        if sin_coincidencia
        else "Todas las consultas compartieron al menos un termino con el vocabulario generado."
    )

    st.markdown(
        f"""
        <div class="explain-grid">
            <div class="explain-card">
                <div class="explain-title">Calidad de recuperacion</div>
                <div class="explain-text">{escapar(lectura_resultados)}</div>
            </div>
            <div class="explain-card">
                <div class="explain-title">Efecto del vocabulario</div>
                <div class="explain-text">{escapar(lectura_vocabulario)} Sparsidad aproximada: {sparsidad:.1%}.</div>
            </div>
            <div class="explain-card">
                <div class="explain-title">Limitacion principal</div>
                <div class="explain-text">{escapar(lectura_sin_coincidencia)} El modelo no reconoce sinonimos si no aparecen como terminos compartidos.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Terminos principales del corpus")
    # Suma por columnas: mide el peso total de cada termino en todo el corpus.
    terminos_df = (
        matriz_df.sum(axis=0)
        .sort_values(ascending=False)
        .head(12)
        .rename("Peso total")
        .reset_index()
        .rename(columns={"index": "Termino"})
    )
    st.dataframe(
        estilizar_tabla_oscura(terminos_df).format({"Peso total": "{:.4f}"}),
        width="stretch",
        hide_index=True,
        height=calcular_altura_tabla(len(terminos_df), maximo_filas=12),
    )

    st.download_button(
        "Descargar tabla CSV",
        data=evidencia_df[columnas_tabla].to_csv(index=False).encode("utf-8-sig"),
        file_name="evidencia_busquedas.csv",
        mime="text/csv",
        use_container_width=True,
    )
