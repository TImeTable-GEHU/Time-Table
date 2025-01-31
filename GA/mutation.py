import copy
import random

from Constants.constant import Defaults


class TimeTableMutation:
    def __init__(self, mutation_rate = 0.7):
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


class TimeTableCrossOver:
    def perform_crossover(self, timetable1: dict, timetable2: dict):
        """
            Crossovers two timetables.
            Rule1: Swap the entire day TT.
        """

        crossover_days = Defaults.working_days

        # Perform the crossover between week1 and week2
        for day in crossover_days:
            if day in (timetable1, timetable2):
                timetable1[day], timetable2[day] = timetable2[day], timetable1[day]

        return timetable1, timetable2
