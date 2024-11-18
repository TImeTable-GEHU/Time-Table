# This is the Orchestrator file, which will govern the flow.
from GA.Fitness import TimetableFitnessCalculator
from GA.chromosome import TimetableGeneration

# Create Chromosomes
timetable_generator = TimetableGeneration()
timetable = timetable_generator.create_timetable(num_weeks=5)

# Fitness of each Chromosome
fitness_calculator = TimetableFitnessCalculator(timetable)
overall_fitness, fitness_scores = fitness_calculator.calculate_fitness()

# Selection of all Chromosomes

# Crossover for all selected Chromosomes

# Mutate all crossover Chromosomes

# Store best of Chromosomes