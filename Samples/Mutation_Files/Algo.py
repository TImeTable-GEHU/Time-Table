import random

# Example data
class_times = [
    {"section":"A", "teacher": "sashi kumar", "time_slot": 1,"classRoom":"LT01"},
    {"section":"B", "teacher": "subhankar goyal", "time_slot": 2,"classRoom":"LT01"},
    {"section":"A", "teacher": "mehul manu", "time_slot": 3,"classRoom":"LT02"},
    {"section":"C", "teacher": "kiran kher", "time_slot": 4,"classRoom":"LT02"},
    {"section":"B", "teacher": "devender", "time_slot": 4,"classRoom":"LT02"}
    # Add more class entries here
]

# Mutation function for the timetable chromosome
def mutate_timetable(chromosome, mutation_rate = 0.7):
    """
    Applies mutation on a given timetable chromosome.
    
    Parameters:  

    - chromosome: list of dicts, each representing a class schedule (e.g., class_times above)
    - mutation_rate: float, probability of mutation for each gene (class time slot)
    
    Returns:
    - mutated_chromosome: list, mutated timetable chromosome
    """
    classroom =["LT02","LT01"]
    section =["A","B","C"]

    mutated_chromosome = chromosome.copy()  # Create a copy to mutate
    
    for gene in mutated_chromosome:
        if random.random() < mutation_rate:
            # Randomly swap time slots or assign a new time slot within valid range
            new_time_slot = random.randint(1, 5)  # Assuming time slots from 1 to 5
            gene["time_slot"] = new_time_slot  # Mutate by changing the time slot
            gene["classRoom"] =random.choice(classroom)
            gene["section"] =random.choice(section)
    
    return mutated_chromosome

# Example of mutation in action
print("Original Schedule:\n", class_times)
mutated_schedule = mutate_timetable(class_times)

print("/n")
print("Mutated Schedule:", mutated_schedule)
