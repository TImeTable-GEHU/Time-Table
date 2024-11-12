import random
import copy

# Example data
class_times = [
    {"section": "A", "teacher": "sashi kumar", "time_slot": 1, "classRoom": "LT01"},
    {"section": "B", "teacher": "subhankar goyal", "time_slot": 2, "classRoom": "LT01"},
    {"section": "A", "teacher": "mehul manu", "time_slot": 3, "classRoom": "LT02"},
    {"section": "C", "teacher": "kiran kher", "time_slot": 4, "classRoom": "LT02"},
    {"section": "B", "teacher": "devender", "time_slot": 4, "classRoom": "LT02"},
]

# Mutation function for the timetable chromosome
def mutate_timetable(chromosome, mutation_rate=0.7):
    """
    Applies mutation on a given timetable chromosome, ensuring no classroom conflicts.
    
    Parameters:  
    - chromosome: list of dicts, each representing a class schedule (e.g., class_times above)
    - mutation_rate: float, probability of mutation for each gene (class time slot)
    
    Returns:
    - mutated_chromosome: list, mutated timetable chromosome
    """
    classrooms = ["LT02", "LT01"]
    sections = ["A", "B", "C"]
    mutated_chromosome = copy.deepcopy(chromosome)  # Create a deep copy to mutate
    
    # Track assigned classrooms per time slot
    assigned_classrooms = {time_slot: set() for time_slot in range(1, 6)}
    
    for gene in mutated_chromosome:
        # Add the original classroom assignment to avoid assigning it again in the mutation
        assigned_classrooms[gene["time_slot"]].add(gene["classRoom"])

    for gene in mutated_chromosome:
        if random.random() < mutation_rate:
            # Randomly assign a new time slot within a valid range
            new_time_slot = random.randint(1, 5)
            gene["time_slot"] = new_time_slot
            
            
            # Find a conflict-free classroom for the new time slot
            available_classrooms = [room for room in classrooms if room not in assigned_classrooms[new_time_slot]]
            if available_classrooms:
                gene["classRoom"] = random.choice(available_classrooms)
            else:
                gene["classRoom"] = random.choice(classrooms)  # Fall back if all rooms are assigned
            
            # Randomly assign a section
            gene["section"] = random.choice(sections)
            
            # Update assigned classrooms for the new time slot
            assigned_classrooms[new_time_slot].add(gene["classRoom"])

    return mutated_chromosome

# Example of mutation in action
print("Original Schedule:\n", class_times)
mutated_schedule = mutate_timetable(class_times)

print("\nMutated Schedule:", mutated_schedule)

