from parameter_statistical_analysis import *
from evaluation_statistical_analysis import *
from helpers import get_border_solutions_pareto
if __name__ == "__main__":
    print('Se asume que ya han sido corridos los scripts de ejecucion population_size_adjustment.py, parameter_adjustment.py \n\n')

    print('Primero se obtiene el mejor tamaño de población:')
    rank_test_param_config = population_adjustment()
    print('rank test: ', rank_test_param_config)
    print('el tamaño de poblacion que obtiene mejores resultados en promedio es: ', obtain_best_population_size(rank_test_param_config), '\n\n')

    print('Luego para este tamaño de población, obtenemos la mejor configuración paramétrica:')
    rank_test_param_config = mutcross_adjustment()
    print('rank test: ', rank_test_param_config)
    print('la mejor configuración en promedio es: ', obtain_best_configuration(rank_test_param_config))

    print('\n\n')
    print('Luego con esta configuracion y tamaño de poblacion se debería correr el script de ejecución de las evaluaciones evaluation.py')
    print('En este script se asume que ya ha sido ejecutado el script de evaluacion \n')

    evaluation_statistical_analysis()

    print('Se estudia la normalidad de las distribuciones para cada algoritmo para cada instancia con el test de Kolmogorov-Smirnov \n\n')
    study_normal_distributions()

    print('Se realiza el test no paramétrico: Mann-Whitney U rank test \n\n')
    algorithm_comparison()
    print('\n\n')

    print('Ahora se comparan los algoritmos vs los Greedy')
    greedy_comparison()
    print('Como se puede observar en las graficas, todos los puntos basados en los resultados de los greedy son dominados por los frente de pareto de los algoritmos \n\n')

    print('\n\n')
    print('los frente de pareto para las instancias son: ')
    print_reference_paretos()

    print('\n\n')
    print('Puntos interesantes del frente de pareto:')
    print(get_border_solutions_pareto())
    
