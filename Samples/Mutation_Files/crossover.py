import random

def crossover(timetable1, timetable2, crossover_point):
    # Perform crossover
    offspring1 = timetable1[:crossover_point] + timetable2[crossover_point:]
    offspring2 = timetable2[:crossover_point] + timetable1[crossover_point:]

    # Function to remove duplicates in offspring while preserving original order
    def remove_duplicates(offspring, original):
        seen = set()
        unique_offspring = []
        for gene in offspring:
            if gene not in seen:
                unique_offspring.append(gene)
                seen.add(gene)
            else:
                # Add a unique gene from original parent that isn't in offspring
                for gene in original:
                    if gene not in seen:
                        unique_offspring.append(gene)
                        seen.add(gene)
                        break
        return unique_offspring

    # Remove duplicates from both offspring
    offspring1 = remove_duplicates(offspring1, timetable1)
    offspring2 = remove_duplicates(offspring2, timetable2)

    return offspring1, offspring2


# Example parents with dictionaries representing class schedules
timetable1 = [
    {"section": "A", "teacher": "sashi kumar", "time_slot": 1, "classRoom": "LT01"},
    {"section": "A", "teacher": "deepa nair", "time_slot": 2, "classRoom": "LT03"},
    {"section":"B", "teacher": "subhankar goyal", "time_slot": 2,"classRoom":"LT01"},
    {"section":"A", "teacher": "jeet ", "time_slot": 3,"classRoom":"LT03"},
]

timetable2 = [
    {"section": "A", "teacher": "mehul manu", "time_slot": 3, "classRoom": "LT02"},
    {"section": "A", "teacher": "priya sharma", "time_slot": 4, "classRoom": "LT04"},
    {"section":"C", "teacher": "kiran kher", "time_slot": 4,"classRoom":"LT02"},
    {"section":"B", "teacher": "devender", "time_slot": 4,"classRoom":"LT02"}
]

# Perform crossover
offspring1, offspring2 = single_point_crossover(timetable1, timetable2)

print("Parent 1:\n", timetable1)
print("Parent 2:\n", timetable2)
print("Offspring 1:\n", offspring1)
print("Offspring 2:\n", offspring2)