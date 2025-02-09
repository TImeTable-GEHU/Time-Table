import json
import os
import random

CONFIG_FILE = "fitness.json"

class Defaults:
    def __init__(self):
        self.params = self.load_parameters()

    # Load stored parameters or set default values
    def load_parameters(self):
        default_params = {
            "initial_no_of_chromosomes": 10,
            "total_no_of_generations": 10,
            "fitness_score": 1000  # Default fitness score
        }

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                # Ensure all required keys exist
                for key, value in default_params.items():
                    if key not in data:
                        data[key] = value
                return data
        return default_params

    # Save updated parameters to file
    def save_parameters(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.params, file, indent=4)

    # Dynamically update chromosomes, generations, and fitness score
    def update_parameters(self):
        # Simulate a new fitness score (increase/decrease randomly for testing)
        new_fitness_score = self.params["fitness_score"] + random.randint(-50, 100)

        # Adjust values based on fitness improvement
        if new_fitness_score > self.params["fitness_score"]:
            self.params["initial_no_of_chromosomes"] += random.randint(1, 5)
            self.params["total_no_of_generations"] += random.randint(1, 3)
        else:
            self.params["initial_no_of_chromosomes"] = max(5, self.params["initial_no_of_chromosomes"] - random.randint(1, 3))
            self.params["total_no_of_generations"] = max(5, self.params["total_no_of_generations"] - random.randint(1, 2))

        # Update fitness score
        self.params["fitness_score"] = new_fitness_score

        # Save new parameters
        self.save_parameters()

        print(f"Updated Parameters: Population = {self.params['initial_no_of_chromosomes']}, Generations = {self.params['total_no_of_generations']}, Fitness Score = {self.params['fitness_score']}")

# Create an instance of Defaults
defaults = Defaults()

# Update parameters and print the result
defaults.update_parameters()
