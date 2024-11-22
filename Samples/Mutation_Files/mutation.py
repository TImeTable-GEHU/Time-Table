import random

class Mutation:
    def __init__(self, mutation_rate=0.5):
        """
        Initializes the Mutation class with a specified mutation rate.

        Args:
            mutation_rate (float): Fraction (0 to 1) of sections to mutate.
        """
        self.mutation_rate = mutation_rate

    def mutate_time_slots_in_section(self, schedule, section):
        """
        Mutates the time slots within a particular section by shuffling them.

        Args:
            schedule (dict): The schedule containing sections and their data.
            section (str): The section in which mutation should occur.

        Returns:
            bool: True if mutation was performed, False otherwise.
        """
        # Check if the section exists in the schedule
        if section in schedule:
            section_list = schedule[section]

            # Ensure there are enough time slots to shuffle
            if len(section_list) < 2:
                print(f"Not enough time slots to mutate in section '{section}'.")
                return False

            # Extract and shuffle the time slots
            time_slots = [entry["time_slot"] for entry in section_list]
            random.shuffle(time_slots)

            # Assign the shuffled time slots back to the section
            for i, entry in enumerate(section_list):
                entry["time_slot"] = time_slots[i]

            return True
        else:
            return False

    def mutate_all_sections(self, schedule):
        """
        Mutates time slots for a fixed fraction of sections in the schedule.

        Args:
            schedule (dict): The schedule containing sections and their data.

        Returns:
            list: List of sections where mutations occurred.
        """
        # Calculate the number of sections to mutate
        total_sections = list(schedule.keys())
        num_to_mutate = max(1, int(self.mutation_rate * len(total_sections)))

        # Randomly select the sections to mutate
        sections_to_mutate = random.sample(total_sections, num_to_mutate)
        mutated_sections = []

        for section in sections_to_mutate:
            if self.mutate_time_slots_in_section(schedule, section):
                mutated_sections.append(section)

        return mutated_sections

    def print_schedule(self, schedule):
        """
        Prints the schedule in an organized format.

        Args:
            schedule (dict): The schedule to print.
        """
        print("\nMutated Schedule:")
        print("=" * 50)
        for section, entries in schedule.items():
            print(f"Section {section}:")
            print("-" * 30)
            for entry in entries:
                print(f"  Teacher: {entry['teacher_id']}, Subject: {entry['subject_id']}, "
                      f"Classroom: {entry['classroom_id']}, Time Slot: {entry['time_slot']}")
            print("-" * 30)
        print("=" * 50)


# Example schedule
schedule = {
    "A": [
        {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:55 - 10:50"},
        {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:00 - 9:55"},
        {"teacher_id": "AP24", "subject_id": "SCS-501", "classroom_id": "R1", "time_slot": "11:10 - 12:05"},
        {"teacher_id": "AK23", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "12:05 - 1:00"},
        {"teacher_id": "SS03", "subject_id": "TCS-502", "classroom_id": "R1", "time_slot": "1:20 - 2:15"},
        {"teacher_id": "SP06", "subject_id": "TCS-503", "classroom_id": "R1", "time_slot": "2:15 - 3:10"},
        {"teacher_id": "DT20", "subject_id": "XCS-501", "classroom_id": "R1", "time_slot": "3:30 - 4:25"},
    ],
    "B": [
        {"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:55 - 10:50"},
        {"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:00 - 9:55"},
        {"teacher_id": "BJ10", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "11:10 - 12:05"},
        {"teacher_id": "PA21", "subject_id": "XCS-501", "classroom_id": "R2", "time_slot": "12:05 - 1:00"},
    ],
    "C": [
        {"teacher_id": "RS11", "subject_id": "TMA-502", "classroom_id": "R3", "time_slot": "9:00 - 9:55"},
        {"teacher_id": "AA04", "subject_id": "TCS-502", "classroom_id": "R3", "time_slot": "9:55 - 10:50"},
        {"teacher_id": "RD09", "subject_id": "PCS-506", "classroom_id": "L3", "time_slot": "12:05 - 1:00"},
        {"teacher_id": "RD09", "subject_id": "PCS-506", "classroom_id": "L3", "time_slot": "11:10 - 12:05"},
        {"teacher_id": "DP07", "subject_id": "TCS-503", "classroom_id": "R3", "time_slot": "1:20 - 2:15"},
        {"teacher_id": "SJ16", "subject_id": "TCS-509", "classroom_id": "R3", "time_slot": "2:15 - 3:10"},
        {"teacher_id": "AB01", "subject_id": "TCS-531", "classroom_id": "R3", "time_slot": "3:30 - 4:25"},
    ],
    "D": [
        {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:55 - 10:50"},
        {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:00 - 9:55"},
        {"teacher_id": "AC05", "subject_id": "TCS-502", "classroom_id": "R4", "time_slot": "11:10 - 12:05"},
        {"teacher_id": "PK02", "subject_id": "TCS-531", "classroom_id": "R4", "time_slot": "12:05 - 1:00"},
    ]
}

# Create an instance of the Mutation class with a fixed mutation rate (e.g., 50%)
mutation_rate = 0.5
mutator = Mutation(mutation_rate=mutation_rate)

# Perform mutations on all sections
mutated_sections = mutator.mutate_all_sections(schedule)

# Print the mutated schedule
mutator.print_schedule(schedule)

# Output the sections where mutation occurred
print(f"Mutated Sections: {mutated_sections}")
