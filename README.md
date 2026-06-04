# Buscador Semántico Simple utilizando Representación Vectorial de Texto

Proyecto de investigación desarrollado para la asignatura **Álgebra Lineal para la Computación**.

## Descripción del proyecto

Este proyecto consiste en implementar un **buscador semántico simple** utilizando conceptos de álgebra lineal, representación vectorial de texto y medidas de similitud.

La idea principal es transformar documentos o textos en **vectores numéricos**, construir una representación matricial de ellos y comparar su similitud mediante operaciones vectoriales, especialmente usando la **similitud coseno**.

El sistema permite ingresar una consulta y obtener como resultado los documentos más similares dentro de un conjunto de textos previamente definido.

## Objetivo general

Construir un buscador semántico básico capaz de representar textos mediante vectores y recuperar documentos relevantes utilizando medidas de similitud basadas en álgebra lineal.

## Objetivos específicos

* Representar documentos como vectores numéricos.
* Comprender el concepto de espacio vectorial aplicado al procesamiento de texto.
* Construir una matriz documento-término.
* Aplicar la similitud coseno para comparar textos.
* Implementar un buscador simple en Python.
* Analizar los resultados obtenidos mediante consultas.
* Representar gráficamente las similitudes entre consultas y documentos.

## Fundamento matemático

### Representación vectorial de texto

Cada documento se representa como un vector dentro de un espacio vectorial. Cada dimensión del vector corresponde a una palabra del vocabulario generado a partir del conjunto de documentos.

Por ejemplo, si el vocabulario es:

```txt
[gato, perro, comida, casa]
```

Un documento como:

```txt
"gato comida casa"
```

podría representarse como:

```txt
[1, 0, 1, 1]
```

Esto indica que las palabras `gato`, `comida` y `casa` aparecen en el documento, mientras que `perro` no aparece.

### Matriz documento-término

La matriz documento-término permite representar varios documentos al mismo tiempo.

Cada fila representa un documento.
Cada columna representa una palabra del vocabulario.
Cada valor indica la frecuencia de una palabra en un documento.

Ejemplo:

| Documento   | gato | perro | comida | casa |
| ----------- | ---: | ----: | -----: | ---: |
| Documento 1 |    1 |     0 |      1 |    1 |
| Documento 2 |    0 |     1 |      1 |    0 |
| Documento 3 |    1 |     1 |      0 |    1 |

Esta matriz suele ser dispersa, ya que muchos documentos no contienen todas las palabras del vocabulario.

### Similitud coseno

La similitud coseno mide qué tan parecidos son dos vectores según el ángulo que forman entre ellos.

La fórmula es:

```txt
cos(θ) = (u · v) / (||u|| ||v||)
```

Donde:

* `u · v` es el producto punto entre los vectores.
* `||u||` es la norma del vector `u`.
* `||v||` es la norma del vector `v`.

Interpretación:

* Si el valor se acerca a `1`, los textos son muy similares.
* Si el valor se acerca a `0`, los textos son poco similares.
* Si el valor es exactamente `0`, no comparten términos relevantes.

## Funcionamiento del programa

El programa realiza los siguientes pasos:

1. Carga un conjunto de documentos o textos.
2. Limpia y procesa el texto.
3. Genera un vocabulario.
4. Convierte los documentos en vectores.
5. Construye una matriz documento-término.
6. Recibe una consulta de búsqueda.
7. Convierte la consulta en un vector.
8. Calcula la similitud coseno entre la consulta y cada documento.
9. Ordena los documentos desde el más similar al menos similar.
10. Muestra los resultados obtenidos.

## Tecnologías utilizadas

* Python
* NumPy
* Pandas
* Scikit-learn
* Matplotlib

## Bibliotecas principales

```python
numpy
pandas
scikit-learn
matplotlib
```

## Instalación

Para ejecutar el proyecto, primero se recomienda crear un entorno virtual.

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

Activar el entorno virtual en Linux o macOS:

```bash
source venv/bin/activate
```

Luego instalar las dependencias:

```bash
pip install numpy pandas scikit-learn matplotlib
```

## Ejecución del programa

Para ejecutar el buscador:

```bash
python main.py
```

El programa mostrará los documentos cargados y permitirá realizar búsquedas mediante consultas simples.

Ejemplo de consulta:

```txt
inteligencia artificial y aprendizaje automático
```

El resultado esperado será una lista de documentos ordenados según su similitud con la consulta.

## Ejemplo de salida esperada

```txt
Consulta: inteligencia artificial

Resultados más similares:

1. Documento 2
Similitud: 0.82
Texto: La inteligencia artificial permite crear sistemas capaces de aprender...

2. Documento 5
Similitud: 0.43
Texto: Los modelos de lenguaje utilizan grandes cantidades de datos...

3. Documento 1
Similitud: 0.10
Texto: El fútbol es uno de los deportes más populares del mundo...
```

## Análisis de resultados

Los resultados obtenidos deben analizarse considerando:

* Qué documentos fueron recuperados.
* Qué nivel de similitud obtuvo cada documento.
* Si los resultados tienen relación real con la consulta.
* Si el vocabulario afecta la calidad de búsqueda.
* Qué ocurre cuando una consulta contiene palabras que no están en los documentos.
* Qué limitaciones aparecen al usar solamente frecuencia de términos.

## Representación gráfica

Para analizar visualmente los resultados, se pueden incluir gráficos como:

* Gráfico de barras con la similitud entre una consulta y cada documento.
* Mapa de calor con similitudes entre documentos.
* Gráfico de dispersión utilizando reducción dimensional.

Ejemplo de gráfico recomendado:

```txt
Consulta: "machine learning"

Documento IA: 0.85
Documento Programación: 0.45
Documento Deportes: 0.05
Documento Cocina: 0.00
```

## Ventajas del enfoque

* Es simple de implementar.
* Usa conceptos fundamentales de álgebra lineal.
* Permite representar textos como vectores.
* Facilita la comparación entre documentos.
* Sirve como base para comprender buscadores modernos y sistemas de recomendación.

## Limitaciones del enfoque

* No comprende completamente el significado del texto.
* Depende mucho de las palabras exactas usadas.
* Puede fallar cuando dos textos usan sinónimos distintos.
* No considera el orden de las palabras.
* Puede generar matrices muy grandes y dispersas.
* No alcanza el nivel de modelos modernos basados en embeddings o inteligencia artificial avanzada.

## Aplicaciones modernas relacionadas

Este tipo de representación vectorial se utiliza en distintas áreas de la computación moderna, tales como:

* Motores de búsqueda.
* Sistemas de recomendación.
* Chatbots.
* Inteligencia artificial.
* Modelos de lenguaje.
* Recuperación de información.
* Clasificación automática de documentos.

## Estructura sugerida del proyecto

```txt
buscador-semantico/
│
├── main.py
├── README.md
├── requirements.txt
├── data/
│   └── documentos.txt
├── src/
│   ├── vectorizador.py
│   ├── buscador.py
│   └── graficos.py
└── informe/
    └── informe.pdf
```

## Posible contenido de requirements.txt

```txt
numpy
pandas
scikit-learn
matplotlib
```

## Conclusión

Este proyecto demuestra cómo los conceptos de álgebra lineal pueden aplicarse al procesamiento de texto y a la recuperación de información.

Mediante la representación vectorial de documentos, la matriz documento-término y la similitud coseno, es posible construir un buscador simple capaz de comparar textos y entregar resultados relevantes según una consulta.

Aunque este enfoque tiene limitaciones, permite comprender la base matemática de sistemas más avanzados utilizados actualmente en motores de búsqueda, inteligencia artificial, chatbots y sistemas de recomendación.

## Integrantes

* Nombre integrante 1
* Nombre integrante 2
* Nombre integrante 3
* Nombre integrante 4

## Curso

Álgebra Lineal para la Computación

## Fecha de entrega

23 de junio de 2026
