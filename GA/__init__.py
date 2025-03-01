import copy
from dataclasses import dataclass

from Constants.helper_routines import (
    initialize_teacher_availability,
    update_matrix_for_best,
    update_teacher_availability_matrix,
)
from GA.chromosome import TimeTableGeneration
from GA.fitness import TimetableFitnessEvaluator
from GA.mutation import TimeTableCrossOver, TimeTableMutation
from GA.selection import TimeTableSelection


@dataclass
class TimetableConfig:
    teacher_subject_mapping: dict
    total_sections: dict
    total_classrooms: dict
    total_labs: dict
    teacher_preferences: dict
    teacher_weekly_workload: dict
    special_subjects: dict
    labs: dict
    subject_quota_limits: dict
    teacher_duty_days: dict
    teacher_availability_matrix: dict
    lab_availability_matrix: dict
    total_generations: int
    time_slots: dict
    day_map: dict
    time_slot_map: dict
    prev_selected: dict = None
    prev_mutated: list = None
    fixed_teacher_assignment: dict = None


class TimetableEngine:
    def __init__(self, config: TimetableConfig):
        self.config = config
        self.teacher_availability = copy.deepcopy(config.teacher_availability_matrix)
        self.lab_availability = copy.deepcopy(config.lab_availability_matrix)

    def _update_lab_availability(self, best_timetable):
        updated_lab = copy.deepcopy(self.config.lab_availability_matrix)
        for weekday, daily_schedule in best_timetable.items():
            day_index = self.config.day_map.get(weekday)
            if day_index is None:
                continue
            for allocations in daily_schedule.values():
                for alloc in allocations:
                    lab = alloc.get("classroom_id")
                    ts_index = self.config.time_slot_map.get(alloc.get("time_slot"))
                    if lab in updated_lab and ts_index is not None:
                        updated_lab[lab][day_index][ts_index - 1] = False
        return updated_lab

    def _generate_timetable(self, teacher_matrix):
        tg = TimeTableGeneration(
            teacher_subject_mapping=self.config.teacher_subject_mapping,
            total_sections=self.config.total_sections,
            total_classrooms=self.config.total_classrooms,
            total_labs=self.config.total_labs,
            teacher_preferences=self.config.teacher_preferences,
            teacher_weekly_workload=self.config.teacher_weekly_workload,
            special_subjects=self.config.special_subjects,
            labs=self.config.labs,
            subject_quota_limits=self.config.subject_quota_limits,
            teacher_duty_days=self.config.teacher_duty_days,
            teacher_availability_matrix=teacher_matrix,
            lab_availability_matrix=self.lab_availability,
            time_slots=self.config.time_slots,
            fixed_teacher_assignment=self.config.fixed_teacher_assignment or {}
        )
        timetable, updated_teacher = tg.create_timetable(self.config.total_generations)[:2]
        fitness = TimetableFitnessEvaluator(
            timetable=timetable,
            all_sections=list(tg.sections_manager.keys()),
            subject_teacher_mapping=tg.subject_teacher_mapping,
            available_classrooms=list(tg.classrooms_manager.keys()),
            available_labs=list(tg.lab_capacity_manager.keys()),
            classroom_capacity=tg.classrooms_manager,
            section_student_strength=tg.sections_manager,
            subject_quota_data=tg.subject_quota_limits,
            teacher_time_preferences=tg.teacher_availability_preferences,
            teacher_daily_workload=tg.weekly_workload,
            time_slots=self.config.time_slots,
        ).evaluate_timetable_fitness()

        selected = TimeTableSelection().select_chromosomes(fitness[1])
        if self.config.prev_selected:
            selected.update(self.config.prev_selected)

        crossover = TimeTableCrossOver()
        crossover_chromosomes = []
        selected_keys = list(selected.keys())
        for i in range(0, len(selected_keys), 2):
            if i + 1 < len(selected_keys):
                c1, c2 = crossover.perform_crossover(
                    timetable[selected_keys[i]], timetable[selected_keys[i + 1]]
                )
                crossover_chromosomes.extend([c1, c2])

        mutated = [TimeTableMutation().mutate_schedule_for_week(ch) for ch in crossover_chromosomes]
        if self.config.prev_mutated:
            mutated.extend(self.config.prev_mutated)

        best_chromosome, best_score = None, -1
        for key, score in selected.items():
            score = int(score)
            if score > best_score and key in timetable:
                best_score = score
                best_chromosome = timetable[key]

        if best_chromosome:
            updated_teacher = update_teacher_availability_matrix(teacher_matrix, best_chromosome)
        return best_chromosome, updated_teacher, selected, mutated

    def run(self):
        initial_teacher = copy.deepcopy(self.teacher_availability)
        updated_teacher = copy.deepcopy(initial_teacher)
        best_chromosome = None

        self.config.prev_selected = None
        self.config.prev_mutated = None

        for _ in range(self.config.total_generations):
            teacher_copy = copy.deepcopy(initial_teacher)
            best, updated_teacher, selected, mutated = self._generate_timetable(teacher_copy)
            best_chromosome = best

            self.config.prev_selected = selected
            self.config.prev_mutated = mutated

        updated_teacher = update_matrix_for_best(
            best_chromosome,
            updated_teacher,
            self.config.day_map,
            self.config.time_slot_map,
        )

        updated_lab = self._update_lab_availability(best_chromosome)
        return best_chromosome, updated_teacher, updated_lab


def run_timetable_generation(
    teacher_subject_mapping: dict,
    total_sections: dict,
    total_classrooms: dict,
    total_labs: dict,
    teacher_preferences: dict,
    teacher_weekly_workload: dict,
    special_subjects: dict,
    labs: dict,
    subject_quota_limits: dict,
    teacher_duty_days: dict,
    teacher_availability_matrix: dict,
    lab_availability_matrix: dict,
    total_generations: int,
    time_slots: dict,
    day_map: dict,
    time_slot_map: dict,
    fixed_teacher_assignment: dict = None
):
    config = TimetableConfig(
        teacher_subject_mapping=teacher_subject_mapping,
        total_sections=total_sections,
        total_classrooms=total_classrooms,
        total_labs=total_labs,
        teacher_preferences=teacher_preferences,
        teacher_weekly_workload=teacher_weekly_workload,
        special_subjects=special_subjects,
        labs=labs,
        subject_quota_limits=subject_quota_limits,
        teacher_duty_days=teacher_duty_days,
        teacher_availability_matrix=teacher_availability_matrix,
        lab_availability_matrix=lab_availability_matrix,
        total_generations=total_generations,
        time_slots=time_slots,
        day_map=day_map,
        time_slot_map=time_slot_map,
        fixed_teacher_assignment=fixed_teacher_assignment or {}
    )
    engine = TimetableEngine(config)
    return engine.run()


if __name__ == "__main__":
    from Constants.constant import Defaults
    from Samples.samples import (
        SpecialSubjects,
        SubjectTeacherMap,
        SubjectWeeklyQuota,
        TeacherWorkload,
    )

    lab_matrix = {
        "L1": [[True] * 7 for _ in range(5)],
        "L2": [[True] * 7 for _ in range(5)],
        "L3": [[True] * 7 for _ in range(5)],
        "L4": [[True] * 7 for _ in range(5)],
        "L5": [[True] * 7 for _ in range(5)],
        "L6": [[True] * 7 for _ in range(5)],
    }

    teacher_availability = initialize_teacher_availability(
        TeacherWorkload.Weekly_workLoad.keys(), 5, 7
    )

    best_tt, final_teacher, final_lab = run_timetable_generation(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections={"A": 70, "B": 100, "C": 75, "D": 100},
        total_classrooms={"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250},
        total_labs={"L1": 70, "L2": 50, "L3": 70, "L4": 50, "L5": 70, "L6": 50},
        teacher_preferences=TeacherWorkload.teacher_preferences,
        teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
        special_subjects=SpecialSubjects.special_subjects,
        labs=SpecialSubjects.Labs,
        subject_quota_limits=SubjectWeeklyQuota.subject_quota,
        teacher_duty_days=TeacherWorkload.teacher_duty_days,
        teacher_availability_matrix=teacher_availability,
        lab_availability_matrix=lab_matrix,
        total_generations=Defaults.total_no_of_generations,
        time_slots={
            1: "9:00 - 9:55",
            2: "9:55 - 10:50",
            3: "11:10 - 12:05",
            4: "12:05 - 1:00",
            5: "1:20 - 2:15",
            6: "2:15 - 3:10",
            7: "3:30 - 4:25",
        },
        day_map={
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        },
        time_slot_map={
            "9:00 - 9:55": 1,
            "9:55 - 10:50": 2,
            "11:10 - 12:05": 3,
            "12:05 - 1:00": 4,
            "1:20 - 2:15": 5,
            "2:15 - 3:10": 6,
            "3:30 - 4:25": 7,
        },
        fixed_teacher_assignment={
            "A": {"TCS-531": "AB01", "TMA-502": "HP18"},  # section: {"subject": teacher}
            "B": {"TCS-503": "BJ10"}
        }
    )

    from icecream import ic
    ic(best_tt, final_teacher, final_lab)
