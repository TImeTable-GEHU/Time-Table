import random
import copy

class Mutation:
    def __init__(self, mutation_rate= random.random()):
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
        if section in schedule:
            section_list = schedule[section]

            if len(section_list) < 2:  # Not enough time slots to shuffle
                return False

            time_slots = [entry["time_slot"] for entry in section_list]
            random.shuffle(time_slots)

            for i, entry in enumerate(section_list):
                entry["time_slot"] = time_slots[i]

            return True
        return False

    def mutate_schedule_for_week(self, weekly_schedule):
        """
        Mutates the time slots for all weekdays in the weekly schedule.

        Args:
            weekly_schedule (dict): The weekly schedule containing days, sections, and data.

        Returns:
            dict: The mutated weekly schedule.
        """
        # Create a deep copy to keep the original intact
        mutated_weekly_schedule = copy.deepcopy(weekly_schedule)

        for day, day_schedule in mutated_weekly_schedule.items():
            # Calculate the number of sections to mutate
            total_sections = list(day_schedule.keys())
            num_to_mutate = max(1, int(self.mutation_rate * len(total_sections)))

            # Randomly select sections to mutate
            sections_to_mutate = random.sample(total_sections, num_to_mutate)

            for section in sections_to_mutate:
                self.mutate_time_slots_in_section(day_schedule, section)

        return mutated_weekly_schedule

    def print_weekly_schedule(self, weekly_schedule):
        """
        Prints the weekly schedule in an organized format.

        Args:
            weekly_schedule (dict): The schedule to print.
        """
        print("\nWeekly Schedule:")
        print("=" * 50)
        for day, day_schedule in weekly_schedule.items():
            print(f"Day: {day}")
            print("-" * 30)
            for section, entries in day_schedule.items():
                print(f"  Section {section}:")
                for entry in entries:
                    print(f"    Teacher: {entry['teacher_id']}, Subject: {entry['subject_id']}, "
                          f"Classroom: {entry['classroom_id']}, Time Slot: {entry['time_slot']}")
            print("-" * 30)
        print("=" * 50)


# Example weekly schedule
weekly_schedule = {
    "Monday": {
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
    },
    "Tuesday": {
        "A": [{"teacher_id": "AK22", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"}],
        "B": [{"teacher_id": "BJ16", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:55 - 10:50"}]
    },
    "Wednesday": {
        "A": [{"teacher_id": "DT20", "subject_id": "XCS-501", "classroom_id": "R1", "time_slot": "11:10 - 12:05"}]
    },
    "Thursday": {
        "A": [{"teacher_id": "SJ12", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "12:05 - 1:00"}]
    },
    "Friday": {
        "A": [{"teacher_id": "AB01", "subject_id": "TCS-531", "classroom_id": "R3", "time_slot": "1:20 - 2:15"}]
    },
    "Saturday": {
        "A": [{"teacher_id": "SJ14", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "2:15 - 3:10"}]
    }
}

# Create an instance of the Mutation class with a mutation rate  randomly chosen
mutation_rate = random.random()
mutator = Mutation(mutation_rate=mutation_rate)

# Perform mutations for the entire week
mutated_weekly_schedule = mutator.mutate_schedule_for_week(weekly_schedule)

# Print the original and mutated schedules
print("Original Weekly Schedule:")
mutator.print_weekly_schedule(weekly_schedule)

print("\nMutated Weekly Schedule:")
mutator.print_weekly_schedule(mutated_weekly_schedule)