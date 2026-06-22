import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity


FONDO_FIGURA = "#eef3f7"
FONDO_EJES = "#ffffff"
COLOR_TEXTO = "#27374d"
COLOR_TEXTO_SECUNDARIO = "#526d82"
COLOR_GRID = "#dde6ed"
COLOR_VERDE = "#27374d"
COLOR_CELESTE = "#9db2bf"
CMAP_SIMILITUD = sns.color_palette(
    ["#ffffff", "#dde6ed", "#9db2bf", "#526d82", "#27374d"],
    as_cmap=True,
)
CMAP_MATRIZ = sns.color_palette(
    ["#ffffff", "#dde6ed", "#9db2bf", "#526d82", "#27374d"],
    as_cmap=True,
)


def aplicar_tema_grafico(fig, ax) -> None:
    """Aplica una paleta oscura coherente con la interfaz."""
    fig.patch.set_facecolor(FONDO_FIGURA)
    ax.set_facecolor(FONDO_EJES)
    ax.title.set_color(COLOR_TEXTO)
    ax.xaxis.label.set_color(COLOR_TEXTO_SECUNDARIO)
    ax.yaxis.label.set_color(COLOR_TEXTO_SECUNDARIO)
    ax.tick_params(colors=COLOR_TEXTO_SECUNDARIO)
    ax.grid(color=COLOR_GRID, alpha=0.45)
    for spine in ax.spines.values():
        spine.set_color(COLOR_GRID)


def aplicar_tema_colorbar(ax) -> None:
    """Ajusta el color de la barra lateral de un mapa de calor."""
    if not ax.collections:
        return
    colorbar = ax.collections[0].colorbar
    if colorbar is None:
        return
    colorbar.ax.yaxis.label.set_color(COLOR_TEXTO_SECUNDARIO)
    colorbar.ax.tick_params(colors=COLOR_TEXTO_SECUNDARIO)
    colorbar.outline.set_edgecolor(COLOR_GRID)


def crear_grafico_barras_similitud(resultados: pd.DataFrame):
    """Grafico de barras con la similitud entre consulta y documentos."""
    fig, ax = plt.subplots(figsize=(10, 4.8))
    datos = resultados.sort_values("Similitud coseno", ascending=True)
    maximo = datos["Similitud coseno"].max()
    colores = [
        COLOR_CELESTE if valor < maximo else COLOR_VERDE
        for valor in datos["Similitud coseno"]
    ]

    ax.barh(datos["Documento"] + " - " + datos["Tema"], datos["Similitud coseno"], color=colores)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Similitud coseno")
    ax.set_ylabel("Documento")
    ax.set_title("Similitud entre la consulta y cada documento")
    aplicar_tema_grafico(fig, ax)
    ax.grid(axis="x", alpha=0.35)

    for contenedor in ax.containers:
        ax.bar_label(contenedor, fmt="%.3f", padding=4, color=COLOR_TEXTO, fontsize=9)

    fig.tight_layout()
    return fig


def crear_mapa_calor_documentos(matriz_documento_termino, etiquetas: list[str]):
    """Mapa de calor de similitud coseno entre documentos."""
    similitud_documentos = cosine_similarity(matriz_documento_termino)

    fig, ax = plt.subplots(figsize=(9.5, 7))
    sns.heatmap(
        similitud_documentos,
        annot=True,
        fmt=".2f",
        cmap=CMAP_SIMILITUD,
        vmin=0,
        vmax=1,
        xticklabels=etiquetas,
        yticklabels=etiquetas,
        square=True,
        cbar_kws={"label": "Similitud coseno"},
        annot_kws={"color": COLOR_TEXTO, "fontsize": 8},
        ax=ax,
    )
    ax.set_title("Mapa de calor de similitud entre documentos")
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    aplicar_tema_grafico(fig, ax)
    aplicar_tema_colorbar(ax)
    fig.tight_layout()
    return fig


def crear_grafico_terminos(matriz_df: pd.DataFrame, tipo_vectorizador: str):
    """Grafico de terminos con mayor frecuencia o peso total."""
    puntajes = matriz_df.sum(axis=0).sort_values(ascending=False).head(12)
    etiqueta_eje = "Peso TF-IDF total" if tipo_vectorizador == "TF-IDF" else "Frecuencia total"

    fig, ax = plt.subplots(figsize=(10, 4.8))
    puntajes.sort_values(ascending=True).plot(kind="barh", color=COLOR_VERDE, ax=ax)
    ax.set_xlabel(etiqueta_eje)
    ax.set_ylabel("Termino")
    ax.set_title("Terminos mas importantes del conjunto de documentos")
    aplicar_tema_grafico(fig, ax)
    ax.grid(axis="x", alpha=0.35)
    fig.tight_layout()
    return fig


def crear_mapa_calor_matriz(matriz_df: pd.DataFrame, tipo_vectorizador: str):
    """Mapa de calor de los terminos mas importantes de la matriz."""
    terminos_principales = matriz_df.sum(axis=0).sort_values(ascending=False).head(18).index
    matriz_reducida = matriz_df.loc[:, terminos_principales]
    etiqueta = "Peso TF-IDF" if tipo_vectorizador == "TF-IDF" else "Frecuencia"

    fig, ax = plt.subplots(figsize=(11, 5.8))
    sns.heatmap(
        matriz_reducida,
        cmap=CMAP_MATRIZ,
        linewidths=0.35,
        linecolor=COLOR_GRID,
        cbar_kws={"label": etiqueta},
        ax=ax,
    )
    ax.set_title("Vista visual de la matriz documento-termino")
    ax.set_xlabel("Terminos principales")
    ax.set_ylabel("Documentos")
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    aplicar_tema_grafico(fig, ax)
    aplicar_tema_colorbar(ax)
    fig.tight_layout()
    return fig
