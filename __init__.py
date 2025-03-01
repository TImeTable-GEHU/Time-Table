from Constants.constant import Defaults
from Constants.helper_routines import (
    initialize_teacher_availability,
    update_matrix_for_best,
    update_teacher_availability_matrix,
)
from GA.chromosome import TimeTableGeneration
from GA.fitness import TimetableFitnessEvaluator
from GA.mutation import TimeTableCrossOver, TimeTableMutation
from GA.selection import TimeTableSelection
from Samples.samples import (
    InterDepartment,
    RoomCapacity,
    SpecialSubjects,
    SubjectTeacherMap,
    SubjectWeeklyQuota,
    TeacherWorkload,
    TimeSlots,
)


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
    time_slots,
    prev_selected_chromosomes=None,
    prev_mutated_chromosomes=None,
):
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
        time_slots=time_slots,
    )
    timetable, teacher_availability_matrix = timetable_generator.create_timetable(
        Defaults.initial_no_of_chromosomes
    )

    fitness_calculator = TimetableFitnessEvaluator(
        timetable,
        timetable_generator.sections_manager.keys(),
        SubjectTeacherMap.subject_teacher_map,
        timetable_generator.classrooms_manager.keys(),
        timetable_generator.lab_capacity_manager.keys(),
        timetable_generator.classrooms_manager,
        timetable_generator.sections_manager,
        timetable_generator.subject_quota_limits,
        timetable_generator.teacher_availability_preferences,
        timetable_generator.weekly_workload,
        time_slots,
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
            c1, c2 = crossover_object.perform_crossover(
                timetable[parent1], timetable[parent2]
            )
            crossover_chromosomes.append(c1)
            crossover_chromosomes.append(c2)

    mutation_object = TimeTableMutation()
    mutated_chromosomes = [
        mutation_object.mutate_schedule_for_week(ch) for ch in crossover_chromosomes
    ]
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
            teacher_availability_matrix, best_chromosome
        )

    return (
        best_chromosome,
        teacher_availability_matrix,
        selected_chromosomes,
        mutated_chromosomes,
    )


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
    total_generations,
    time_slots,
):
    prev_selected = None
    prev_mutated = None
    best_chromosome = None

    for _ in range(total_generations):
        (
            best_chromosome,
            teacher_availability_matrix,
            selected,
            mutated,
        ) = timetable_generation(
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
            time_slots=time_slots,
            prev_selected_chromosomes=prev_selected,
            prev_mutated_chromosomes=prev_mutated,
        )
        prev_selected = selected
        prev_mutated = mutated

    return best_chromosome, teacher_availability_matrix


if __name__ == "__main__":
    best, correct_teacher_availability_matrix = run_timetable_generation(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections=RoomCapacity.section_strength,
        total_classrooms=RoomCapacity.room_capacity,
        total_labs=RoomCapacity.lab_capacity,
        teacher_preferences=TeacherWorkload.teacher_preferences,
        teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
        special_subjects=SpecialSubjects.special_subjects,
        labs=SpecialSubjects.Labs,
        subject_quota_limits=SubjectWeeklyQuota.subject_quota,
        teacher_duty_days=TeacherWorkload.teacher_duty_days,
        teacher_availability_matrix=initialize_teacher_availability(
            TeacherWorkload.Weekly_workLoad.keys(), 5, 7
        ),
        total_generations=Defaults.total_no_of_generations,
        time_slots=TimeSlots.time_slots,
    )
    from icecream import ic

    ic(best)
    correct_teacher_availability_matrix = update_matrix_for_best(
        best,
        correct_teacher_availability_matrix,
        {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        },
        {
            "08:00 - 09:00": 1,
            "09:00 - 10:00": 2,
            "10:00 - 11:00": 3,
            "11:00 - 12:00": 4,
            "12:00 - 13:00": 5,
            "13:50 - 14:50": 6,
            "14:50 - 15:50": 7,
        },
    )
