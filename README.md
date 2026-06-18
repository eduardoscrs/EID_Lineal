# Buscador Semantico Simple

Aplicacion en Python con Streamlit para representar documentos como vectores, construir una matriz documento-termino y buscar textos similares mediante similitud coseno.

## Por que Streamlit

Streamlit permite crear interfaz, tablas, metricas y graficos usando solo Python. Para una presentacion es mas simple que separar un backend y un frontend, y deja el foco en la parte importante del ramo: vectores, matrices y similitud coseno.

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
3. Avanza por el recorrido de presentacion: metodo, documentos, matriz, busqueda, graficos, analisis y cierre.
4. En la pantalla de busqueda, escribe una consulta o usa una consulta de ejemplo.
5. Observa el ranking por similitud coseno y los graficos de apoyo.
6. En la pantalla de analisis, revisa la tabla de evidencia y descarga el CSV si necesitas guardar los resultados.

Tambien puedes anadir textos o subir varios documentos desde la barra lateral durante la sesion. La carga acepta archivos `txt`, `md`, `csv`, `pdf` y `docx`.

Si quieres trabajar solo con documentos propios, desmarca `Documentos de ejemplo` en la barra lateral.

El vocabulario ignora numeros sueltos y codigos alfanumericos; solo conserva palabras y numeros de cuatro digitos como anos.

## Estructura del proyecto

```text
EID_Lineal/
|-- app.py
|-- requirements.txt
|-- README.md
|-- data/
|   |-- __init__.py
|   |-- example_documents.py
|   `-- stop_words.py
|-- docs/
|   `-- progreso.md
|-- logic/
|   |-- __init__.py
|   |-- document_loader.py
|   `-- vector_model.py
|-- ui/
|   |-- __init__.py
|   |-- analysis.py
|   |-- documents.py
|   |-- presentation.py
|   |-- search.py
|   |-- sections.py
|   |-- sidebar.py
|   |-- styles.py
|   |-- summary.py
|   |-- theme.css
|   `-- view_helpers.py
`-- visualization/
    |-- __init__.py
    `-- charts.py
```

## Que hace cada archivo

### Raiz

- `app.py`: punto de entrada. Inicia Streamlit, define los pasos del recorrido, guarda el estado de sesion, construye los documentos, genera la matriz y decide que pantalla mostrar.
- `requirements.txt`: lista las dependencias necesarias para ejecutar el proyecto.
- `README.md`: guia general del proyecto, instalacion, ejecucion y estructura.

### data

- `data/example_documents.py`: contiene los documentos de ejemplo que usa la app por defecto.
- `data/stop_words.py`: contiene palabras comunes en espanol que se pueden eliminar de la matriz, como `de`, `la`, `el`, `y`.


### logic

- `logic/vector_model.py`: es el nucleo matematico. Crea el vectorizador `TF-IDF` o `CountVectorizer`, genera la matriz documento-termino, transforma la consulta y calcula similitud coseno.
- `logic/document_loader.py`: lee archivos subidos por el usuario. Soporta `txt`, `md`, `csv`, `pdf` y `docx`.


### ui

- `ui/sections.py`: funciona como indice. Reune y reexporta las pantallas para que `app.py` pueda importarlas de forma simple.
- `ui/presentation.py`: contiene la portada, el encabezado del recorrido y la pantalla para entender el metodo elegido.
- `ui/documents.py`: muestra los documentos disponibles y la matriz documento-termino.
- `ui/search.py`: maneja la pantalla de busqueda: consulta, vector de consulta, ranking y resultados.
- `ui/analysis.py`: genera evidencia experimental: consultas de prueba, similitudes, interpretacion, analisis critico y descarga CSV.
- `ui/summary.py`: contiene la pantalla de graficos y la pantalla final de cierre.
- `ui/sidebar.py`: controla la barra lateral: elegir metodo, activar documentos de ejemplo, agregar texto, subir archivos y navegar entre pasos.
- `ui/view_helpers.py`: contiene funciones auxiliares para la interfaz, como escapar HTML, crear vistas previas, ordenar terminos, clasificar similitud y dar estilo a tablas.
- `ui/styles.py`: configura la pagina de Streamlit y carga el archivo CSS.
- `ui/theme.css`: contiene los estilos visuales: colores, tarjetas, botones, tablas, layout y comportamiento responsive.


### visualization

- `visualization/charts.py`: crea los graficos con Matplotlib y Seaborn: barras de similitud, mapa de calor de documentos, terminos principales y mapa de calor de la matriz.



