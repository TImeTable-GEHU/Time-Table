import random
from Samples.Fitness_Files.fitness import TimetableFitness

class Selection:
    def __init__(self):
        self.fitness_evaluator = TimetableFitness()
    
    def select_top_chromosomes(self, population: list, percentage=0.30) -> list:
        # Calculate the number of chromosomes to select
        num_to_select = int(len(population) * percentage)
        
        # Calculate fitness for each chromosome in the population
        fitness_scores = [(chromosome, self.fitness_evaluator.calculate_fitness(chromosome)) for chromosome in population]

        # Sort chromosomes by their fitness scores in descending order
        sorted_chromosomes = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
        
        # Define the number of chromosomes for each selection method
        best_num = int(num_to_select * 0.20)
        worst_num = int(num_to_select * 0.10)
        middle_num = num_to_select - (best_num + worst_num)

        # Select the top-performing chromosomes
        best_chromosomes = sorted_chromosomes[:best_num]
        worst_chromosomes = sorted_chromosomes[-worst_num:]
        middle_chromosomes = sorted_chromosomes[best_num:best_num + middle_num]

        # Roulette selection from the middle chromosomes
        total_fitness = sum(fitness for _, fitness in middle_chromosomes)
        roulette_chromosomes = random.choices(
            middle_chromosomes, 
            weights=[fitness / total_fitness for _, fitness in middle_chromosomes], 
            k=int(middle_num * 0.70)
        )

        # Rank-based selection from the middle chromosomes
        total_rank = sum(range(1, len(middle_chromosomes) + 1))
        rank_probabilities = [i / total_rank for i in range(1, len(middle_chromosomes) + 1)]
        rank_chromosomes = random.choices(
            middle_chromosomes, 
            weights=rank_probabilities, 
            k=int(middle_num * 0.30)
        )

        # Collect selected chromosomes into the final list
        selected_chromosomes = [chromosome for chromosome, _ in best_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in worst_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in roulette_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in rank_chromosomes]

        # Print selected chromosomes for verification
        print("\n--- Selected Chromosomes ---")
        for chromosome in selected_chromosomes:
            print(chromosome)

        return selected_chromosomes

# Example usage
if __name__ == "__main__":
    timetable_generator = TimetableFitness()
    population = [timetable_generator.create_timetable() for _ in range(10)]

    selector = Selection()
    selected_chromosomes = selector.select_top_chromosomes(population, percentage=0.30)

    print("\nSelection process complete.\n")
