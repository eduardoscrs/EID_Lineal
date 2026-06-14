# Progreso de la demo

## Estado por area

| Area | Objetivo | Avance | Nota |
| --- | --- | ---: | --- |
| Demo por consola | Ejecutar busquedas con documentos de prueba y similitud coseno | 30% | Base funcional lista para crecer |
| Motor vectorial | Mejorar tokenizacion, vocabulario, matriz y modos de frecuencia | 20% | Falta normalizacion avanzada y pruebas |
| Busqueda y ranking | Ordenar resultados, manejar consultas y preparar evaluaciones | 25% | Falta tabla de consultas esperadas |
| Datos de prueba | Ampliar documentos y cubrir temas variados | 15% | Falta pasar de 6 a 12+ textos |
| Visualizacion | Graficos de resultados para analisis e informe | 10% | Falta Matplotlib, barras PNG y/o mapa de calor |
| Front-end basico | Diseno comodo para consulta, resultados y carga de archivos | 0% | Puede partir con datos simulados |
| Informe | Marco teorico, ejemplo matematico, analisis y conclusiones | 10% | Falta escribir evidencia final |
| Integracion final | Unir consola, graficos, datos, informe y posible front | 0% | Se realiza al cierre de cada semana |

## Tareas por integrante

| Integrante | Frente principal | Tareas | Entregable independiente | Avance |
| --- | --- | --- | --- | ---: |
| Marcelo Santana | Motor vectorial | Normalizacion de texto, vocabulario, matriz documento-termino, modo frecuencia absoluta/binaria | `src/vectorizador.py` mejorado y ejemplos pequenos reproducibles | 20% |
| Eduardo Escares | Datos y ejecucion CLI | Ampliar `data/documentos.txt`, mejorar argumentos de `main.py`, agregar salida clara para matriz y resultados | Demo ejecutable con 12+ documentos y comandos documentados | 15% |
| Patricio Benavides | Ranking, metricas y graficos | Mejorar ranking, preparar consultas de prueba, generar graficos con Matplotlib | Graficos exportables y tabla de similitudes para el informe | 10% |
| Yaninna Alvarez | Front-end e informe | Bosquejar front basico con datos simulados, redactar marco teorico, ejemplo matematico y conclusiones | Prototipo visual simple e informe con secciones iniciales | 0% |

## Demo actual

La demo actual es una base de consola. Carga textos breves, genera el vocabulario,
construye la matriz documento-termino, vectoriza una consulta y calcula similitud
coseno contra cada documento. Luego ordena los resultados y muestra una barra
ASCII para comparar similitudes.

Comandos principales:

```bash
python3 main.py
python3 main.py --query "inteligencia artificial"
python3 main.py --query "seguridad redes ataques" --top 2
python3 main.py --interactive
```

La consola conviene como primer paso porque valida el calculo matematico antes
de invertir tiempo en interfaz. El front-end puede avanzar en paralelo usando
datos simulados con la misma forma de resultados esperada.

## Proximos pasos

### Semana 1

- Falta: ampliar documentos de prueba a 12 o mas.
- Falta: mostrar matriz documento-termino completa o parcial en consola.
- Falta: agregar consultas de prueba con resultado esperado.
- Falta: normalizacion mas fuerte para tildes, signos y palabras comunes.
- Falta: primer grafico Matplotlib de similitudes por consulta.
- Falta: bosquejo de front-end basico con input de consulta y tabla de resultados.
- Falta: marco teorico y ejemplo manual de similitud coseno.

### Semana 2

- Falta: integrar graficos al flujo de ejecucion.
- Falta: agregar opcion de carga de documentos desde archivo.
- Falta: analizar calidad de resultados, vocabulario y limitaciones.
- Falta: conectar front-end al resultado real o dejarlo como prototipo explicado.
- Falta: preparar capturas, anexos, bibliografia y conclusiones.
- Falta: revisar ejecucion limpia desde cero.

## Criterios de integracion

- Cada frente debe poder probarse sin esperar cambios de otro integrante.
- Los cambios de motor deben mantener `python3 main.py` funcionando.
- Los graficos deben generarse desde resultados ya calculados.
- El front-end debe partir con datos simulados para no bloquearse por backend.
- El informe debe citar comandos, capturas o resultados reproducibles.
