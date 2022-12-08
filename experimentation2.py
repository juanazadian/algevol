from jmetal.algorithm.multiobjective.spea2 import SPEA2
from jmetal.util.termination_criterion import StoppingByEvaluations

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from problem import DFOM
from mutation import GraphMutation
from crossover import GraphCrossover

from jmetal.core.quality_indicator import *
from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment
from jmetal.operator import PolynomialMutation, SBXCrossover
from jmetal.problem import ZDT1, ZDT2, ZDT3
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import NEIGHBORHOODS_INFORMATION, REDUCED_NEIGHBORHOODS_GRAPH


from problem import DFOM

def configure_experiment(problems: dict, n_run: int):
    jobs = []
    max_evaluations = 20000

    mutation_probabilities = [0.001, 0.01, 0.1]
    crossover_probabilities = [0.5, 0.75, 1]
    population_sizes = [20, 40, 60]
    for mutation_probability in mutation_probabilities:
        for crossover_probability in crossover_probabilities:
            for population_size in population_sizes:
                for n in range(n_run):
                    for problem_tag, problem in problems.items():
                        jobs.append(
                            Job(
                                algorithm = SPEA2(
                                    problem=problem,
                                    population_size=population_size,
                                    offspring_population_size=population_size,
                                    mutation=GraphMutation(probability=mutation_probability, neighborhoods_graph = problem.neighborhoods_graph, distribution_index=20),
                                    crossover=GraphCrossover(probability=crossover_probability), # Se puede ajustar esa probabilidad.
                                    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
                                ),
                                algorithm_tag=f'SPEA2 - size:{population_size} - mutation:{mutation_probability} - crossover:{crossover_probability}',
                                problem_tag= problem_tag,
                                run=n,
                            )
                        )


    return jobs


if __name__ == '__main__':
    # Configure the experiments
    problem = DFOM(
        neighborhoods_information = NEIGHBORHOODS_INFORMATION,
        neighborhoods_graph = REDUCED_NEIGHBORHOODS_GRAPH,
        central_index = 0,
    )
    jobs = configure_experiment(problems={'DFOM': problem}, n_run=2)
    # Run the study
    output_directory = 'try'
    experiment = Experiment(output_dir=output_directory, jobs=jobs)
    experiment.run()


    generate_summary_from_experiment(
        input_dir=output_directory,
        reference_fronts='reference/',
        quality_indicators=[GenerationalDistance(), EpsilonIndicator(), HyperVolume([1.0, 1.0])]
    )
