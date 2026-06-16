# Buscador Semantico Simple

Aplicacion en Python con Streamlit para representar documentos como vectores, construir una matriz documento-termino y buscar textos similares mediante similitud coseno.

## Por que Streamlit

Streamlit es una buena opcion para este proyecto porque permite crear interfaz, tablas, metricas y graficos usando solo Python. Para una presentacion es mas simple que separar un backend y un frontend, y deja el foco en la parte importante del ramo: vectores, matrices y similitud coseno.

## Estructura del proyecto

```text
proyecto de algebra/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── example_documents.py
│   └── stop_words.py
├── logic/
│   └── vector_model.py
├── ui/
│   ├── sections.py
│   ├── sidebar.py
│   └── styles.py
└── visualization/
    └── charts.py
```

## Que hace cada parte

- `app.py`: punto de entrada. Coordina la aplicacion y conecta todos los modulos.
- `data/example_documents.py`: documentos de ejemplo usados por el buscador.
- `data/stop_words.py`: palabras comunes que se pueden eliminar de la matriz.
- `logic/vector_model.py`: vectorizacion, matriz documento-termino, vector de consulta y similitud coseno.
- `ui/sidebar.py`: controles laterales para elegir vectorizador y agregar documentos.
- `ui/sections.py`: pantallas principales de la app.
- `ui/styles.py`: configuracion visual de Streamlit.
- `visualization/charts.py`: graficos de barras, mapa de calor y terminos principales.

## Requisitos

- Python 3.10 o superior
- Dependencias listadas en `requirements.txt`

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecutar la app

```bash
python -m streamlit run app.py

```

## Uso rapido

1. Abre la aplicacion en el navegador.
2. En la portada, elige `TF-IDF` o `CountVectorizer`.
3. Avanza por el recorrido de presentacion: metodo, documentos, matriz, busqueda, graficos y cierre.
4. En la pantalla de busqueda, escribe una consulta o usa una consulta de ejemplo.
5. Observa el ranking por similitud coseno y los graficos de apoyo.

Tambien puedes agregar documentos propios desde la barra lateral durante la sesion.
