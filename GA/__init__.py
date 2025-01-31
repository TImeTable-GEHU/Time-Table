# This is the Orchestrator file, which will govern the flow.

from Constants.constant import Defaults
from GA.mutation import TimeTableMutation, TimeTableCrossOver
from GA.selection import TimeTableSelection
from GA.fitness import TimetableFitnessEvaluator
from GA.chromosome import TimeTableGeneration
from Samples.samples import (
    SubjectTeacherMap,
    TeacherWorkload,
    SpecialSubjects,
    SubjectWeeklyQuota,
    Classrooms,
    Sections,

)


def timetable_generation():
    # Create Chromosomes
    timetable_generator = TimeTableGeneration(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections=6,
        total_classrooms=8,
        total_labs=3,
        teacher_preferences=TeacherWorkload.teacher_preferences,
        teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
        special_subjects=SpecialSubjects.special_subjects,
        subject_quota_limits=SubjectWeeklyQuota.subject_quota,
        labs_list=Classrooms.labs,
        teacher_duty_days=TeacherWorkload.teacher_duty_days,
    )

    timetable = timetable_generator.create_timetable(Defaults.initial_no_of_chromosomes)
    # Fitness of each Chromosome
    fitness_calculator = TimetableFitnessEvaluator(
        timetable,
        timetable_generator.sections_manager.sections,
        SubjectTeacherMap.subject_teacher_map,
        timetable_generator.classrooms_manager.classrooms,
        timetable_generator.classrooms_manager.labs,
        timetable_generator.room_capacity_manager.room_capacity,
        timetable_generator.room_capacity_manager.section_strength,
        timetable_generator.subject_quota_limits,
        timetable_generator.teacher_availability_preferences,
        timetable_generator.weekly_workload,
    )

    fitness_scores = fitness_calculator.evaluate_timetable_fitness()


    # Selection of all Chromosomes
    selection_object = TimeTableSelection()
    selected_chromosomes = selection_object.select_chromosomes(fitness_scores[1])

    # Crossover for all selected Chromosomes
    crossover_object = TimeTableCrossOver()
    crossover_chromosomes = []
    selected_chromosome_keys = list(selected_chromosomes.keys())

    for i in range(0, len(selected_chromosome_keys), 2):
        if i + 1 < len(selected_chromosome_keys):
            parent1 = selected_chromosome_keys[i]
            parent2 = selected_chromosome_keys[i + 1]
            child1, child2 = crossover_object.perform_crossover(
                timetable[parent1],
                timetable[parent2]
            )

            crossover_chromosomes.append(child1)
            crossover_chromosomes.append(child2)


    # Mutate all crossover Chromosomes
    mutation_object = TimeTableMutation()
    mutated_chromosomes = [
        mutation_object.mutate_schedule_for_week(chromosome)
        for chromosome in crossover_chromosomes
    ]
    best_chromosome_score = -1
    best_chromosome = dict()

    for week_no, week_score in selected_chromosomes.items():
        if int(week_score) > best_chromosome_score:
            best_chromosome_score = int(week_score)
            best_chromosome = timetable[week_no]
    return best_chromosome


def run_timetable_generation():
    for generation in range(Defaults.total_no_of_generations):
        best_chromosome = timetable_generation()
    return best_chromosome

run_timetable_generation()
