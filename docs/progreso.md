# Progreso del proyecto

## Porcentajes de avance

| Area | Estado actual | Avance | Meta de cierre |
| --- | --- | ---: | --- |
| App Streamlit | Interfaz abre, tabs cargan y buscador funciona | 80% | App estable para presentar |
| Motor vectorial | TF-IDF y CountVectorizer operativos | 75% | Calculos revisados y explicables |
| Busqueda y ranking | Consulta, similitud coseno y resultados ordenados listos | 80% | 5 consultas de prueba validadas |
| Matriz documento-termino | Tabla, vocabulario y dimensiones visibles | 75% | Evidencia clara para informe |
| Graficos | Barras, mapas de calor y terminos principales disponibles | 70% | Graficos revisados y capturados |
| Documentos de ejemplo | Hay base de documentos integrada | 60% | Textos ampliados y balanceados |
| Carga de documentos | Permite agregar texto manual en la sesion | 45% | Definir si queda manual o se agrega subida |
| README y ejecucion | Instrucciones principales listas | 65% | Guia final sin ambiguedades |
| Informe y presentacion | Estructura pendiente de completar | 30% | Informe con capturas, analisis y conclusiones |
| QA final | Pruebas manuales iniciales realizadas | 45% | Lista de validacion completa |

## Tareas por integrante

| Integrante | Foco de la semana | Tareas concretas | Entregable | Avance |
| --- | --- | --- | --- | ---: |
| Marcelo Santana | Motor y validacion matematica | Revisar `logic/vector_model.py`, confirmar formula de similitud coseno, preparar 5 consultas esperadas, explicar TF-IDF vs CountVectorizer | Tabla de consultas con resultado esperado y explicacion breve del calculo | 55% |
| Eduardo Escares | Ejecucion y datos | Revisar `requirements.txt`, mejorar README si falta algun paso, ampliar `data/example_documents.py` a documentos mas variados, probar ejecucion desde venv limpio | App ejecutable siguiendo README y dataset final de ejemplo | 60% |
| Patricio Benavides | Graficos y analisis visual | Revisar `visualization/charts.py`, elegir 3 graficos finales, capturar evidencia de matriz y similitudes, anotar que muestra cada grafico | Capturas y descripcion corta de cada grafico para el informe | 50% |
| Yaninna Alvarez | Informe y presentacion | Redactar marco teorico, ejemplo manual con dos vectores, ventajas y limitaciones, conclusiones y aplicaciones modernas | Borrador de informe listo para integrar capturas y resultados | 35% |

## Plan de una semana

### Dia 1

- Falta: confirmar que todos pueden ejecutar `python -m streamlit run app.py`
- Falta: dejar cerrado el dataset base de documentos
- Falta: definir si la carga sera texto manual o subida de archivo

### Dia 2

- Falta: validar 5 consultas con resultados esperados
- Falta: revisar que la matriz documento-termino sea entendible
- Falta: corregir textos o nombres confusos dentro de la app

### Dia 3

- Falta: elegir graficos finales
- Falta: generar capturas para informe
- Falta: anotar interpretacion de cada grafico

### Dia 4

- Falta: completar marco teorico y ejemplo matematico
- Falta: escribir analisis de resultados
- Falta: explicar ventajas y limitaciones del enfoque

### Dia 5

- Falta: integrar capturas, tablas y explicaciones
- Falta: probar app desde cero con venv
- Falta: revisar README final

### Dia 6

- Falta: ensayo de presentacion
- Falta: revisar errores visuales o textos largos
- Falta: congelar cambios de codigo salvo errores criticos

### Dia 7

- Falta: revision final del informe
- Falta: prueba final de la app
- Falta: preparar entrega y respaldo

## Criterios de cierre

- La app debe abrir con `python -m streamlit run app.py`
- El buscador debe entregar ranking para al menos 5 consultas
- La matriz documento-termino debe mostrarse y poder explicarse
- Los graficos finales deben tener interpretacion en el informe
- El informe debe incluir formula, ejemplo manual, analisis, limitaciones y conclusiones
- La presentacion debe poder hacerse sin depender de cambios de ultimo minuto
