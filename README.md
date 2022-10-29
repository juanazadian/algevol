# Algoritmos Evolutivos - Grupo A
Proyecto de Algoritmos Evolutivos usando jMetalPy para la búsqueda de soluciones de instalación de redes de fibra óptica en barrios de Montevideo.
El problema a resolver es el de abastecimiento de cobertura de fibra optica a distintos barrios dentro de Montevideo. El mismo sera planteado como un problema multiobjetivo, que se pasara a detallar mas adelante, y para el cual se utilizara el Algoritmo Evolutivo SPEA-2 para su resolucion. 

La principal razon para utilizar este tipo de algoritmos por sobre otros metodos tradicionales, se basa en la dificultad computacional del problema. El espacio de soluciones existentes tiene una tamano considerablemente grande, y se podrıa relacionar a problemas de grafos NP-Completos como Minimum Spanning Tree.

Asimismo, al ser un problema multiobjetivo, los AE trabajan de manera muy eficiente respecto a estos problemas, y brindan un conjunto de soluciones a partir de los cuales se puede elegir la que satisfaga mejor las necesidades de inversion. 

Habran muchas soluciones en el frente de Pareto, que van a variar en cantidad de barrios que cubren, y en costo total.
