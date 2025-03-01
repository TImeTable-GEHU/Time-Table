import copy
import random

from Constants.constant import Defaults


class TimeTableMutation:
    def __init__(self, mutation_rate=0.7):
        self.mutation_rate = mutation_rate

    def mutate_time_slots_in_section(self, schedule: dict, section: str) -> bool:
        if section not in schedule or len(schedule[section]) < 2:
            return False

        section_slots = schedule[section]
        time_slots = [entry["time_slot"] for entry in section_slots]
        random.shuffle(time_slots)
        for i, entry in enumerate(section_slots):
            entry["time_slot"] = time_slots[i]
        return True

    def mutate_schedule_for_week(self, weekly_schedule: dict) -> dict:
        mutated_schedule = copy.deepcopy(weekly_schedule)
        for day, day_schedule in mutated_schedule.items():
            sections = list(day_schedule.keys())
            num_to_mutate = max(1, int(self.mutation_rate * len(sections)))
            sections_to_mutate = random.sample(sections, num_to_mutate)
            for section in sections_to_mutate:
                self.mutate_time_slots_in_section(day_schedule, section)
        return mutated_schedule


class TimeTableCrossOver:
    def perform_crossover(self, timetable1: dict, timetable2: dict) -> tuple:
        for day in Defaults.working_days:
            if day in timetable1 and day in timetable2:
                timetable1[day], timetable2[day] = timetable2[day], timetable1[day]
        return timetable1, timetable2
