import random
from Constants.time_intervals import TimeIntervalConstant
from Constants.constant import (
    Sections,
    Classrooms,
    RoomCapacity,
    Defaults,
)

class TimeTableGeneration:
    def __init__(
        self,
        teacher_subject_mapping: dict,
        total_sections: int,
        total_classrooms: int,
        total_labs: int,
        teacher_preferences: dict,
        teacher_weekly_workload: dict,
        special_subjects: dict,
        subject_quota_limits: dict,
        labs_list: list,
        teacher_duty_days: dict,
    ):
        self.sections_manager = Sections(total_sections)
        self.classrooms_manager = Classrooms(total_classrooms, total_labs)
        self.room_capacity_manager = RoomCapacity(
            self.classrooms_manager.classrooms, self.sections_manager.sections
        )
        self.weekdays = Defaults.working_days
        self.subject_teacher_mapping = teacher_subject_mapping
        self.subject_quota_limits = subject_quota_limits
        self.lab_subject_list = labs_list
        self.special_subject_list = special_subjects
        self.teacher_availability_preferences = teacher_preferences
        self.available_time_slots = TimeIntervalConstant.time_slots
        self.teacher_duty_days = teacher_duty_days

        sorted_classrooms = sorted(
            self.classrooms_manager.classrooms,
            key=lambda c: self.room_capacity_manager.room_capacity[c],
            reverse=True
        )
        sorted_sections = sorted(
            self.sections_manager.sections,
            key=lambda s: self.room_capacity_manager.section_strength[s],
            reverse=True
        )

        self.section_to_classroom_map = {}
        for section in sorted_sections:
            for classroom in sorted_classrooms:
                if self.room_capacity_manager.room_capacity[classroom] >= self.room_capacity_manager.section_strength[section]:
                    self.section_to_classroom_map[section] = classroom
                    sorted_classrooms.remove(classroom)
                    break
            else:
                raise ValueError(f"No classroom can accommodate section {section.name} with strength {self.room_capacity_manager.section_strength[section]}.")

        self.weekly_workload = teacher_weekly_workload

    def generate_daily_schedule(self, half_day_section_list, section_subject_usage_tracker):
        daily_schedule = {}
        teacher_workload_tracker = {teacher: 0 for teacher in self.weekly_workload.keys()}

        for i, section in enumerate(self.sections_manager.sections):
            section_schedule = []
            subjects_scheduled_today = set()
            assigned_classroom = self.section_to_classroom_map[section]
            total_slots_for_section = 4 if section in half_day_section_list else 7

            for slot_index, current_time_slot in enumerate(self.available_time_slots.values(), start=1):
                if slot_index > total_slots_for_section:
                    break

                available_subjects_for_slot = [
                    subject
                    for subject in self.subject_teacher_mapping.keys()
                    if section_subject_usage_tracker[section][subject] < self.subject_quota_limits.get(subject, 0)
                ]
                random.shuffle(available_subjects_for_slot)

                assigned_teacher = None
                is_lab_subject = False
                is_special_subject = False

                for selected_subject in available_subjects_for_slot:
                    if selected_subject in self.lab_subject_list and slot_index not in [1, 3, 5]:
                        continue
                    is_lab_subject = selected_subject in self.lab_subject_list

                    if selected_subject in self.special_subject_list and slot_index not in [5]:
                        continue
                    is_special_subject = selected_subject in self.special_subject_list

                    if selected_subject not in subjects_scheduled_today:
                        available_teachers = self.subject_teacher_mapping[selected_subject]
                        random.shuffle(available_teachers)

                        for teacher in available_teachers:
                            if teacher_workload_tracker[teacher] < self.weekly_workload.get(teacher, 0):
                                assigned_teacher = teacher
                                teacher_workload_tracker[teacher] += 1
                                break

                    if assigned_teacher:
                        break

                if not assigned_teacher:
                    selected_subject = "Library"
                    assigned_teacher = "None"

                subjects_scheduled_today.add(selected_subject)
                assigned_room = (
                    self.classrooms_manager.labs[slot_index % len(self.classrooms_manager.labs)]
                    if is_lab_subject
                    else assigned_classroom
                )

                if (is_lab_subject or is_special_subject) and slot_index + 1 <= total_slots_for_section:
                    next_time_slot = self.available_time_slots.get(slot_index + 1)
                    section_schedule.append(
                        {
                            "teacher_id": assigned_teacher,
                            "subject_id": selected_subject,
                            "classroom_id": assigned_room,
                            "time_slot": next_time_slot,
                        }
                    )
                    section_subject_usage_tracker[section][selected_subject] += 1

                section_schedule.append(
                    {
                        "teacher_id": assigned_teacher,
                        "subject_id": selected_subject,
                        "classroom_id": assigned_room,
                        "time_slot": current_time_slot,
                    }
                )
                if selected_subject != "Library":
                    section_subject_usage_tracker[section][selected_subject] += 1
            daily_schedule[section] = section_schedule

        return daily_schedule, section_subject_usage_tracker

    def create_timetable(self, num_weeks):
        timetable = {}
        for week in range(1, num_weeks + 1):
            week_schedule = {}
            section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.sections
        }
            for week_day in self.weekdays:
                half_day_sections = self.sections_manager.sections[: len(self.sections_manager.sections) // 2]
                week_schedule[week_day], section_subject_usage_tracker = self.generate_daily_schedule(
                    half_day_sections, section_subject_usage_tracker
                )
            timetable[f"Week {week}"] = week_schedule
        return timetable
