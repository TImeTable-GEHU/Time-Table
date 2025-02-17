import copy
from Constants.helper_routines import (
    initialize_teacher_availability,
    update_matrix_for_best,
    update_teacher_availability_matrix
)
from GA.chromosome import TimeTableGeneration
from GA.fitness import TimetableFitnessEvaluator
from GA.mutation import TimeTableCrossOver, TimeTableMutation
from GA.selection import TimeTableSelection

def update_lab_availability_matrix(initial_lab_matrix, best_timetable, day_map, time_slot_map):
    """
    Iterate over the best chromosome (weekly timetable) and for each lab allocation,
    mark the corresponding slot as False in a deep copy of the initial lab matrix.
    """
    updated_lab_matrix = copy.deepcopy(initial_lab_matrix)
    # best_timetable is a dict keyed by weekday (e.g., 'Monday', 'Tuesday', etc.)
    for weekday, daily_schedule in best_timetable.items():
        # Convert weekday to day index using day_map
        day_index = day_map.get(weekday)
        if day_index is None:
            continue
        # daily_schedule is a dict: keys = section names, values = list of allocations
        for section, allocations in daily_schedule.items():
            for alloc in allocations:
                lab = alloc.get("classroom_id")
                # Only update if the classroom_id is one of the labs
                if lab in updated_lab_matrix:
                    time_slot_str = alloc.get("time_slot")
                    ts_index = time_slot_map.get(time_slot_str)
                    if ts_index is not None:
                        # Adjust index (if lab matrix lists are 0-indexed)
                        updated_lab_matrix[lab][day_index][ts_index - 1] = False
    return updated_lab_matrix

def timetable_generation(
    teacher_subject_mapping,
    total_sections,
    total_classrooms,
    total_labs,
    teacher_preferences,
    teacher_weekly_workload,
    special_subjects,
    labs,
    subject_quota_limits,
    teacher_duty_days,
    teacher_availability_matrix,
    lab_availability_matrix,  # Initial lab matrix passed in
    time_slots,
    total_generations,
    prev_selected_chromosomes=None,
    prev_mutated_chromosomes=None
):
    # Create an instance of TimeTableGeneration.
    timetable_generator = TimeTableGeneration(
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
        time_slots=time_slots
    )

    timetable, teacher_availability_matrix, _ = timetable_generator.create_timetable(total_generations)

    fitness_calculator = TimetableFitnessEvaluator(
        timetable=timetable,
        all_sections=list(timetable_generator.sections_manager.keys()),
        subject_teacher_mapping=timetable_generator.subject_teacher_mapping,
        available_classrooms=list(timetable_generator.classrooms_manager.keys()),
        available_labs=list(timetable_generator.lab_capacity_manager.keys()),
        classroom_capacity=timetable_generator.classrooms_manager,
        section_student_strength=timetable_generator.sections_manager,
        subject_quota_data=timetable_generator.subject_quota_limits,
        teacher_time_preferences=timetable_generator.teacher_availability_preferences,
        teacher_daily_workload=timetable_generator.weekly_workload,
        time_slots=time_slots
    )
    fitness_scores = fitness_calculator.evaluate_timetable_fitness()

    selection_object = TimeTableSelection()
    selected_chromosomes = selection_object.select_chromosomes(fitness_scores[1])
    if prev_selected_chromosomes:
        selected_chromosomes.update(prev_selected_chromosomes)

    crossover_object = TimeTableCrossOver()
    crossover_chromosomes = []
    selected_keys = list(selected_chromosomes.keys())
    for i in range(0, len(selected_keys), 2):
        if i + 1 < len(selected_keys):
            parent1 = selected_keys[i]
            parent2 = selected_keys[i + 1]
            c1, c2 = crossover_object.perform_crossover(timetable[parent1], timetable[parent2])
            crossover_chromosomes.extend([c1, c2])

    mutation_object = TimeTableMutation()
    mutated_chromosomes = [mutation_object.mutate_schedule_for_week(ch) for ch in crossover_chromosomes]
    if prev_mutated_chromosomes:
        mutated_chromosomes.extend(prev_mutated_chromosomes)

    best_chromosome_score = -1
    best_chromosome = None
    for w_no, w_score in selected_chromosomes.items():
        score = int(w_score)
        if score > best_chromosome_score and w_no in timetable:
            best_chromosome_score = score
            best_chromosome = timetable[w_no]

    if best_chromosome:
        teacher_availability_matrix = update_teacher_availability_matrix(
            teacher_availability_matrix,
            best_chromosome
        )

    # Return the best chromosome and the teacher matrix.
    # We do NOT return the working lab matrix because we want to update the initial matrix.
    return best_chromosome, teacher_availability_matrix, selected_chromosomes, mutated_chromosomes

def run_timetable_generations(
    teacher_subject_mapping,
    total_sections,
    total_classrooms,
    total_labs,
    teacher_preferences,
    teacher_weekly_workload,
    special_subjects,
    labs,
    subject_quota_limits,
    teacher_duty_days,
    teacher_availability_matrix,
    lab_availability_matrix,
    total_generations,
    time_slots
):
    prev_selected = None
    prev_mutated = None
    best_chromosome = None
    for _ in range(total_generations):
        best_chromosome, teacher_availability_matrix, selected, mutated = timetable_generation(
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
            time_slots=time_slots,
            prev_selected_chromosomes=prev_selected,
            prev_mutated_chromosomes=prev_mutated,
            total_generations=total_generations
        )
        prev_selected = selected
        prev_mutated = mutated
    return best_chromosome, teacher_availability_matrix, lab_availability_matrix

def run_timetable_generation(
    teacher_subject_mapping,
    total_sections,
    total_classrooms,
    total_labs,
    teacher_preferences,
    teacher_weekly_workload,
    special_subjects,
    labs,
    subject_quota_limits,
    teacher_duty_days,
    teacher_availability_matrix,
    lab_availability_matrix,
    total_generations,
    time_slots,
    day_map,
    time_slot_map
):
    best_tt, teacher_availability_matrix, lab_availability_matrix = run_timetable_generations(
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
        time_slots=time_slots
    )
    teacher_availability_matrix = update_matrix_for_best(
        best_tt,
        teacher_availability_matrix,
        day_map,
        time_slot_map
    )
    # Update the INITIAL lab matrix based solely on the best chromosome's lab allocations.
    updated_lab_matrix = update_lab_availability_matrix(lab_availability_matrix, best_tt, day_map, time_slot_map)
    return best_tt, teacher_availability_matrix, updated_lab_matrix

if __name__ == '__main__':
    from Constants.constant import Defaults
    from GA.__init__ import run_timetable_generation
    from Samples.samples import (SpecialSubjects, SubjectTeacherMap,
                                 SubjectWeeklyQuota, TeacherWorkload)
    lab_availability_matrix = {
        "L1": [[True] * 7 for _ in range(5)],
        "L2": [[True] * 7 for _ in range(5)],
        "L3": [[True] * 7 for _ in range(5)],
        "L4": [[True] * 7 for _ in range(5)],
        "L5": [[True] * 7 for _ in range(5)],
        "L6": [[True] * 7 for _ in range(5)],
    }
    best, correct_teacher_availability_matrix, correct_lab_availability_matrix = run_timetable_generation(
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
        teacher_availability_matrix=initialize_teacher_availability(
            TeacherWorkload.Weekly_workLoad.keys(), 5, 7
        ),
        lab_availability_matrix=lab_availability_matrix,
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
            "Sunday": 6
        },
        time_slot_map={
            "9:00 - 9:55": 1,
            "9:55 - 10:50": 2,
            "11:10 - 12:05": 3,
            "12:05 - 1:00": 4,
            "1:20 - 2:15": 5,
            "2:15 - 3:10": 6,
            "3:30 - 4:25": 7
        }
    )
    from icecream import ic
    ic(best, correct_teacher_availability_matrix, correct_lab_availability_matrix)
