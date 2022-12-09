# Algoritmos Evolutivos - Grupo A
Proyecto de Algoritmos Evolutivos usando jMetalPy para la búsqueda de soluciones de instalación de redes de fibra óptica en barrios de Montevideo.
El problema a resolver es el de abastecimiento de cobertura de fibra optica a distintos barrios dentro de Montevideo. El mismo sera planteado como un problema multiobjetivo, que se pasara a detallar mas adelante, y para el cual se utilizara el Algoritmo Evolutivo SPEA-2 para su resolucion.

La principal razon para utilizar este tipo de algoritmos por sobre otros metodos tradicionales, se basa en la dificultad computacional del problema. El espacio de soluciones existentes tiene una tamano considerablemente grande, y se podrıa relacionar a problemas de grafos NP-Completos como Minimum Spanning Tree.

Asimismo, al ser un problema multiobjetivo, los AE trabajan de manera muy eficiente respecto a estos problemas, y brindan un conjunto de soluciones a partir de los cuales se puede elegir la que satisfaga mejor las necesidades de inversion.

Habran muchas soluciones en el frente de Pareto, que van a variar en cantidad de barrios que cubren, y en costo total.

# Descripción del código
Se armó el código respetando, dentro de lo posible, la estructura de archivos de la libreria `JMetalPY`:
- un archivo `crossover.py`: en el que se definen las operaciones de cruzamiento de soluciones
- un archivo `mutation.py`: en el que se definen la mutación de soluciones
- un archivo `problem.py`: en el que se definen la realidad del problema, junto con la creación de soluciones y funciones de fitness
- un archivo `solution.py`: en el que se definen la estructura de las soluciones (o individuos)

Luego tenemos archivos extras (de ayuda):
- `utils.py` instancias del problema e información de los barrios utilizada en el algoritmo
- `helpers.py` funciones de utilidad que se usan a lo largo del código
- `solution_parser.py` funciones de utilidad para parsear los archivos de ejecución
- `get_distances.py` script utilizado para obtener las distancias entre barrios

Scripts para ejecutar la configuración paramétrica y evaluación:
- `population_size_adjustment.py` script para ejecutar los algoritmos correspondientes a la configuración paramétrica del tamaño de población.
- `parameter_adjustment.py` script para ejecutar los algoritmos correspondientes a la configuración paramétrica de la prob. de cruzamiento y la prob. de mutación.
- `evaluation.py` script para ejecutar los algoritmos correspondientes a la evaluación.

Scripts para analizar los resultados de las ejecuciones de la configuración paramétrica y evaluación:
- `parameter_statistical_analysis.py` script para realizar una análisis estadistico de las ejecuciones de configuración paramétrica.
- `evaluation_statistical_analysis.py` script para realizar una análisis estadistico de las ejecuciones de evaluación.

Un archivo `main.py` para realizar una ejecución aislada del algoritmo

# Resultado de las ejecuciones
Estamos entregando todos los resultados de las ejecuciones para evaluación y configuración paramétrica en sus respectivas carpetas:

## Configuración paramétrica
Para la configuración parametrica hay 2 carpetas:
- `population_size_adjustment` : Se encuentran los resultados de variar el tamaño de población
- `parameter_adjustment` : Se encuentran los resultados de variar las distintas configuraciones de algoritmos variando la prob. de mutación y prob. de cruzamiento

Dentro de estas se encuentran las siguientes sub-carpetas:
- `fun`: con los valores objetivo de cada ejecución
- `var`: con las listas de adyacencia para recrear las soluciones

## Evaluación
Para la evaluación hay 1 carpeta `evaluation` correspondiente a los resultados de las ejecuciones de evaluación:

Dentro de esta se encuentran las siguientes sub-carpetas:
- `fun`: con los valores objetivo de cada ejecución
- `var`: con las listas de adyacencia para recrear las soluciones
- `time`: con los tiempos de ejecución de cada ejecución
- `reference_pareto`: con el frente de pareto de referencia para cada instancia utilizado en la evaluación para calcular las métricas (Hipervolumen Relativo)
- `reference_pareto`: con los frente de pareto de referencia para cada instancia para cada algoritmo utilizado para comparar los algoritmos frente a los greedy
