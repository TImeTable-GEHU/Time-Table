import json
import random
from Samples.Fitness_Files.fitness import TimetableFitness

import json
import random
from Samples.Fitness_Files.fitness import TimetableFitness

class Selection:
    def __init__(self):
        pass

    def read_population_from_json(self, file_path):
        """
        Reads the population and fitness scores from the JSON file.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract class schedules as chromosomes, each linked to a week
                population = data["timetable"]
                week_fitness_scores = data["week_fitness_scores"]  # Read fitness scores directly
                return population, week_fitness_scores
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return {}, []
        except json.JSONDecodeError:
            print(f"Error: The file at {file_path} is not valid JSON.")
            return {}, []

    def select_top_chromosomes(self, population: dict, week_fitness_scores: list, percentage=0.30) -> list:
        """
        Selects the top chromosomes based on their fitness scores from the JSON data.
        """
        if not population or not week_fitness_scores:
            print("The population or fitness scores are empty. Ensure data is loaded correctly.")
            return []

        num_to_select = int(len(week_fitness_scores) * percentage)
        # Sort fitness scores in descending order by score
        sorted_fitness_scores = sorted(week_fitness_scores, key=lambda x: x['score'], reverse=True)
        selected_fitness_scores = sorted_fitness_scores[:num_to_select]

        # Check if the week exists in the population and map weeks to their corresponding timetables
        week_to_timetable_map = {week: timetable for week, timetable in population.items()}

        # Select only the timetables for the chosen weeks
        selected_timetables = []
        for score_entry in selected_fitness_scores:
            week = score_entry['week']
            if week in week_to_timetable_map:
                selected_timetables.append(week_to_timetable_map[week])
            else:
                print(f"Warning: No timetable found for Week {week}. Skipping this week.")

        print("\n--- Selected Weeks and Fitness Scores ---")
        for i, score_entry in enumerate(selected_fitness_scores, start=1):
            print(f"Selection {i}: Week {score_entry['week']} - Score {score_entry['score']}")

        self.create_new_json_file_with_selection(
            len(population),
            len(selected_fitness_scores),
            selected_fitness_scores,
            selected_timetables
        )
        return selected_fitness_scores

    def create_new_json_file_with_selection(self, total_population, selected_count, selected_fitness_scores, selected_timetables):
        output_file_path = "Selected_Fitness_Results.json"
        try:
            # Prepare the data for the new JSON file
            selected_data = {
                "total_population": total_population,
                "selected_count": selected_count,
                "fitness_scores": selected_fitness_scores,
                "timetables": {entry['week']: timetable for entry, timetable in zip(selected_fitness_scores, selected_timetables)}
            }

            # Write the selected data to a new JSON file
            with open(output_file_path, 'w') as file:
                json.dump(selected_data, file, indent=4)

            print(f"\n--- New JSON file created successfully: {output_file_path} ---")
        except Exception as e:
            print(f"Error creating the new JSON file: {e}")

# Main Execution
selector = Selection()

# Read the population and fitness scores from the provided JSON file path
population, week_fitness_scores = selector.read_population_from_json("Samples/Sample_Chromosome.json")

# Select top chromosomes based on the fitness scores if data is valid
if population and week_fitness_scores:
    selected_chromosomes = selector.select_top_chromosomes(population, week_fitness_scores, percentage=0.30)
