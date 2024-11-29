import json
from Constants.time_intervals import TimeIntervalConstant
from GA.chromosome import TimeTableGeneration
from Constants.constant import (
    PenaltyConstants,
    Defaults,
)
from Samples.samples import SubjectTeacherMap, SpecialSubjects, SubjectWeeklyQuota, Classrooms, TeacherWorkload


class TimetableFitnessEvaluator:
    def __init__(
        self,
        timetable,
        all_sections,
        subject_teacher_mapping,
        available_classrooms,
        available_labs,
        classroom_capacity,
        section_student_strength,
        subject_quota_data,
        teacher_time_preferences,
        teacher_daily_workload,
    ):
        self.timetable = timetable
        self.available_days = Defaults.working_days  # Removed trailing comma
        self.all_sections = all_sections
        self.subject_teacher_mapping = subject_teacher_mapping
        self.available_classrooms = available_classrooms
        self.available_labs = available_labs
        self.classroom_capacity = classroom_capacity
        self.section_student_strength = section_student_strength
        self.subject_quota_data = subject_quota_data
        self.teacher_time_preferences = teacher_time_preferences
        self.teacher_daily_workload = teacher_daily_workload

    def evaluate_timetable_fitness(self):
        daily_section_fitness_scores = {}
        weekly_fitness_scores = {}
        teacher_workload_tracking = {}
        for week, week_schedule in self.timetable.items():
            weekly_fitness = 0
            daily_section_fitness_scores[week] = {}
            teacher_time_slot_tracking = {}
            for day, day_schedule in week_schedule.items():
                daily_section_fitness_scores[week][day] = {}
                day_fitness = 0
                for section, section_schedule in day_schedule.items():
                    section_fitness = Defaults.starting_section_fitness

                    classroom_time_slot_tracking = {}

                    for schedule_item in section_schedule:
                        assigned_teacher = schedule_item["teacher_id"]
                        assigned_classroom = schedule_item["classroom_id"]
                        assigned_time_slot = TimeIntervalConstant.time_mapping.get(
                            schedule_item["time_slot"]
                        )
                        section_strength = self.section_student_strength.get(section, 0)

                        # Penalty 1: Double booking a teacher in the same time slot
                        if (assigned_teacher, assigned_time_slot) in teacher_time_slot_tracking.keys():
                            section_fitness -= PenaltyConstants.PENALTY_TEACHER_DOUBLE_BOOKED
                        else:
                            teacher_time_slot_tracking[(assigned_teacher, assigned_time_slot)] = section

                        # Penalty 2: Double booking a classroom in the same time slot
                        if (assigned_classroom, assigned_time_slot) in classroom_time_slot_tracking:
                            section_fitness -= PenaltyConstants.PENALTY_CLASSROOM_DOUBLE_BOOKED
                        else:
                            classroom_time_slot_tracking[(assigned_classroom, assigned_time_slot)] = section

                        # Penalty 3: Over-capacity classrooms
                        if section_strength > self.classroom_capacity.get(
                            assigned_classroom, Defaults.max_class_capacity
                        ):
                            section_fitness -= PenaltyConstants.PENALTY_OVER_CAPACITY

                        # Penalty 4: Assigning teachers during unpreferred time slots
                        preferred_time_slots = self.teacher_time_preferences.get(
                            assigned_teacher, []
                        )
                        if assigned_time_slot not in preferred_time_slots:
                            section_fitness -= PenaltyConstants.PENALTY_UN_PREFERRED_SLOT

                        # Penalty 5: Scheduling teacher on a non-duty day
                        assigned_day = day
                        if assigned_day not in TeacherWorkload.teacher_duty_days.get(assigned_teacher, []):
                            section_fitness -= PenaltyConstants.PENALTY_NON_DUTY_DAY

                        # Tracking teacher workload
                        if assigned_teacher not in teacher_workload_tracking:
                            teacher_workload_tracking[assigned_teacher] = []
                        teacher_workload_tracking[assigned_teacher].append(assigned_time_slot)

                    # Penalty 6: Exceeding teacher daily workload
                    for teacher, times_assigned in teacher_workload_tracking.items():
                        if teacher is not None:
                            if len(times_assigned) > self.teacher_daily_workload.get(teacher, 0):
                                section_fitness -= PenaltyConstants.PENALTY_OVERLOAD_TEACHER

                    daily_section_fitness_scores[week][day][section] = section_fitness
                    day_fitness += section_fitness

                weekly_fitness += day_fitness

            weekly_fitness_scores[week] = weekly_fitness

        return daily_section_fitness_scores, weekly_fitness_scores


if __name__ == "__main__":
    total_sections = 6
    total_classrooms = 8
    total_labs = 3

    # Generate timetable
    timetable_generator = TimeTableGeneration(
        teacher_subject_mapping=SubjectTeacherMap.subject_teacher_map,
        total_sections=total_sections,
        total_classrooms=total_classrooms,
        total_labs=total_labs,
        teacher_preferences=TeacherWorkload.teacher_preferences,
        teacher_weekly_workload=TeacherWorkload.Weekly_workLoad,
        special_subjects=SpecialSubjects.special_subjects,
        subject_quota_limits=SubjectWeeklyQuota.subject_quota,
        labs_list=SpecialSubjects.Labs,
        teacher_duty_days=TeacherWorkload.teacher_duty_days,
    )
    generated_timetables = timetable_generator.create_timetable(5)
    # print(generated_timetables)
    # Evaluate fitness
    fitness_evaluator = TimetableFitnessEvaluator(
        generated_timetables,
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

    section_fitness_data, weekly_fitness_data = fitness_evaluator.evaluate_timetable_fitness()

    # Save results
    with open("GA/chromosome.json", "w") as timetable_file:
        json.dump(generated_timetables, timetable_file, indent=4)

    fitness_output_data = {
        "section_fitness_scores": section_fitness_data,
        "weekly_fitness_scores": weekly_fitness_data,
    }

    with open("GA/fitness.json", "w") as fitness_scores_file:
        json.dump(fitness_output_data, fitness_scores_file, indent=4)

    print("Timetable and fitness scores have been saved.")
