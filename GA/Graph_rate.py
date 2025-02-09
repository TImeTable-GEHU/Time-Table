import json
import os
import random
import matplotlib.pyplot as plt

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
        # Allow for both increase and decrease in fitness score, simulating a more natural fluctuation
        fluctuation = random.randint(-100, 300)  # Allowing for negative fluctuations as well
        new_fitness_score = self.params["fitness_score"] + fluctuation

        # Adjust values based on fitness improvement or decline
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

        # Return the updated parameters for plotting
        return self.params["initial_no_of_chromosomes"], self.params["total_no_of_generations"], self.params["fitness_score"]

# Create an instance of Defaults
defaults = Defaults()

# Prepare lists to store data for plotting
chromosomes_data = []
generations_data = []
fitness_data = []

# Run the update function for multiple iterations to collect data
for _ in range(20):  # Run for 20 iterations
    chromosomes, generations, fitness_score = defaults.update_parameters()
    
    # Store the values for plotting
    chromosomes_data.append(chromosomes)
    generations_data.append(generations)
    fitness_data.append(fitness_score)

# Plotting the data
plt.figure(figsize=(10, 6))

# Plot all the data points over time
plt.plot(range(1, 21), chromosomes_data, label="Chromosomes", marker='o')
plt.plot(range(1, 21), generations_data, label="Generations", marker='s')
plt.plot(range(1, 21), fitness_data, label="Fitness Score", marker='^')

plt.xlabel("Iterations")
plt.ylabel("Values")
plt.title("Dynamic Changes in Parameters Over Time")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()