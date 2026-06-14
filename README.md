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
* Biblioteca estándar de Python para la demo inicial
* Matplotlib para la etapa de gráficos
* NumPy, Pandas y Scikit-learn como posibles apoyos para una versión más avanzada

## Bibliotecas principales

La demo actual no requiere instalar dependencias externas. El archivo
`requirements.txt` queda preparado para las mejoras de visualización y análisis.

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

Luego, si se trabajará en gráficos o análisis avanzado, instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución del programa

Para ejecutar la demo completa por consola:

```bash
python3 main.py
```

El programa carga los documentos desde `data/documentos.txt`, construye la matriz
documento-término y ejecuta consultas de demostración.

Para ejecutar una consulta específica:

```bash
python3 main.py --query "inteligencia artificial"
```

Para usar el modo interactivo:

```bash
python3 main.py --interactive
```

La demo inicial funciona solamente con la biblioteca estándar de Python. Las dependencias de `requirements.txt` quedan como base para una etapa posterior con gráficos más avanzados.

## Cómo funciona la demo

La demo está separada en módulos pequeños para que el trabajo pueda dividirse sin
bloquear a otros integrantes:

* `data/documentos.txt`: textos de prueba en formato `id|titulo|texto`.
* `src/vectorizador.py`: tokeniza textos, genera vocabulario y crea vectores.
* `src/buscador.py`: carga documentos y calcula similitud coseno.
* `src/graficos.py`: muestra barras ASCII con los puntajes de similitud.
* `main.py`: conecta todo y expone comandos por consola.

Flujo interno:

1. Se cargan los documentos.
2. Se limpian y separan las palabras relevantes.
3. Se genera un vocabulario común.
4. Cada documento se convierte en un vector de frecuencias.
5. La consulta se convierte en un vector usando el mismo vocabulario.
6. Se calcula similitud coseno entre consulta y documentos.
7. Se ordenan y muestran los resultados más similares.

## Estado actual y crecimiento

La base funcional ya permite demostrar el cálculo principal del proyecto. El
siguiente crecimiento recomendado es:

* Falta: ampliar documentos de prueba.
* Falta: mostrar matriz documento-término de forma más clara.
* Falta: agregar gráficos reales con Matplotlib.
* Falta: preparar análisis de resultados para el informe.
* Falta: front-end básico con input de consulta, resultados y carga de documentos.

El seguimiento del trabajo está en `docs/progreso.md`.

Ejemplo de consulta:

```txt
inteligencia artificial y aprendizaje automático
```

El resultado esperado será una lista de documentos ordenados según su similitud con la consulta.

## Ejemplo de salida esperada

```txt
Consulta: inteligencia artificial
Matriz documento-término: 6 documentos x 58 términos

Resultados más similares:

1. Inteligencia artificial (0.4082)
   La inteligencia artificial permite crear sistemas capaces de aprender desde datos y resolver problemas complejos.

2. Aprendizaje automatico (0.0000)
   El aprendizaje automatico usa modelos matematicos para detectar patrones en conjuntos de datos.

doc1 | #############                    |  40.82%
doc2 | -                                |   0.00%
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

## Estructura actual del proyecto

```txt
buscador-semantico/
│
├── main.py
├── README.md
├── requirements.txt
├── data/
│   └── documentos.txt
├── docs/
│   ├── EID_Lineal (2).pdf
│   └── progreso.md
├── src/
│   ├── __init__.py
│   ├── vectorizador.py
│   ├── buscador.py
│   └── graficos.py
└── informe/
    └── pendiente
```

## Dependencias preparadas

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

* Marcelo Santana
* Eduardo Escares
* Patricio Benavides
* Yaninna Alvarez

## Curso

Álgebra Lineal para la Computación

## Fecha de entrega

23 de junio de 2026
