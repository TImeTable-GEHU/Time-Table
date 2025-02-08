import random

from Constants.constant import Classrooms, Defaults, RoomCapacity, Sections
from Constants.time_intervals import TimeIntervalConstant


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
        labs: dict,
        subject_quota_limits: dict,
        teacher_duty_days: dict,
        teacher_availability_matrix=dict,
    ):
        self.sections_manager = Sections(total_sections)
        self.classrooms_manager = Classrooms(total_classrooms, total_labs)
        self.room_capacity_manager = RoomCapacity(
            self.classrooms_manager.classrooms, self.sections_manager.sections
        )
        self.weekdays = Defaults.working_days
        self.subject_teacher_mapping = teacher_subject_mapping
        self.subject_quota_limits = subject_quota_limits
        self.lab_subject_list = labs
        self.special_subject_list = special_subjects
        self.teacher_availability_preferences = teacher_preferences
        self.available_time_slots = TimeIntervalConstant.time_slots
        self.teacher_duty_days = teacher_duty_days
        self.weekly_workload = teacher_weekly_workload
        self.teacher_assignment_tracker = {teacher: 0 for teacher in teacher_weekly_workload}
        self.teacher_availability_matrix = teacher_availability_matrix
        self._map_sections_to_classrooms()
        self._assign_teachers_to_sections()


    def _map_sections_to_classrooms(self):
        sorted_classrooms = sorted(
            self.classrooms_manager.classrooms,
            key=lambda classroom: self.room_capacity_manager.room_capacity[classroom],
            reverse=True,
        )
        sorted_sections = sorted(
            self.sections_manager.sections,
            key=lambda section: self.room_capacity_manager.section_strength[section],
            reverse=True,
        )
        self.section_to_classroom_map = {}
        for section in sorted_sections:
            for classroom in sorted_classrooms:
                if self.room_capacity_manager.room_capacity[classroom] >= self.room_capacity_manager.section_strength[section]:
                    self.section_to_classroom_map[section] = classroom
                    sorted_classrooms.remove(classroom)
                    break


    def _assign_teachers_to_sections(self):
        self.teacher_section_map = {
            section: {subject: None for subject in self.subject_teacher_mapping}
            for section in self.sections_manager.sections
        }

        for section in self.sections_manager.sections:
            for subject, teacher_list in self.subject_teacher_mapping.items():
                sorted_teachers_by_load = sorted(teacher_list, key=lambda teacher: self.teacher_assignment_tracker[teacher])
                selected_teacher = sorted_teachers_by_load[0]
                self.teacher_section_map[section][subject] = selected_teacher
                self.teacher_assignment_tracker[selected_teacher] += 1


    def _initialize_teacher_workload_tracker(self):
        return {teacher: 0 for teacher in self.weekly_workload}


    def _get_available_subjects(self, section, subject_usage_tracker):
        return [
            subject
            for subject in self.subject_teacher_mapping
            if subject_usage_tracker[section][subject] < self.subject_quota_limits.get(subject, 0)
        ]


    def _assign_subject_and_teacher(
        self,
        section,
        slot_index,
        subjects_scheduled_today,
        assigned_classroom,
        section_subject_usage_tracker,
        teacher_workload_tracker,
        teacher_availability_matrix,
        day_index
    ):
        available_subjects = self._get_available_subjects(section, section_subject_usage_tracker)
        random.shuffle(available_subjects)

        assigned_teacher = None
        selected_subject = None
        assigned_room = None

        for subject in available_subjects:
            if subject in self.lab_subject_list and slot_index not in [1, 3, 5]:
                continue

            if subject in self.special_subject_list and slot_index not in [5]:
                continue

            if subject not in subjects_scheduled_today:
                teachers_for_subject = self.subject_teacher_mapping[subject]
                preferred_teachers = [
                    teacher for teacher in teachers_for_subject
                    if self.teacher_availability_preferences.get(
                        teacher, []
                    )
                ]
                sorted_teachers_by_load = sorted(preferred_teachers, key=lambda teacher: teacher_workload_tracker[teacher])

                for teacher in sorted_teachers_by_load:
                    if (
                        teacher in teacher_availability_matrix
                        and len(teacher_availability_matrix[teacher]) > day_index
                        and len(teacher_availability_matrix[teacher][day_index]) > (slot_index - 1)
                        and teacher_availability_matrix[teacher][day_index][slot_index - 1]
                    ):
                        teacher_availability_matrix[teacher][day_index][slot_index - 1] = False
                        assigned_teacher = teacher
                        teacher_workload_tracker[assigned_teacher] += 1
                        selected_subject = subject
                        subjects_scheduled_today.add(subject)

                        assigned_room = (
                            self.classrooms_manager.labs[slot_index % len(self.classrooms_manager.labs)]
                            if subject in self.lab_subject_list
                            else assigned_classroom
                        )
                        break

            if assigned_teacher:
                break

        if not assigned_teacher:
            selected_subject = "Library"
            assigned_teacher = "None"
            assigned_room = assigned_classroom

        return assigned_teacher, selected_subject, assigned_room


    def _generate_section_schedule(
        self,
        section,
        half_day_sections,
        section_subject_usage_tracker,
        teacher_workload_tracker,
        teacher_availability_matrix,
        day_index
    ):
        section_schedule = []
        subjects_scheduled_today = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots_for_section = 4 if section in half_day_sections else 7
        slot_index = 1

        while slot_index <= total_slots_for_section:
            time_slot = self.available_time_slots[slot_index]
            assigned_teacher, assigned_subject, assigned_room = self._assign_subject_and_teacher(
                section, slot_index, subjects_scheduled_today, assigned_classroom,
                section_subject_usage_tracker, teacher_workload_tracker,
                teacher_availability_matrix, day_index
            )

            section_schedule.append({
                "teacher_id": assigned_teacher,
                "subject_id": assigned_subject,
                "classroom_id": assigned_room,
                "time_slot": time_slot
            })

            if assigned_subject != "Library":
                section_subject_usage_tracker[section][assigned_subject] += 1

            if assigned_subject in self.lab_subject_list:
                if slot_index + 1 <= total_slots_for_section:
                    next_time_slot = self.available_time_slots[slot_index + 1]
                    section_schedule.append({
                        "teacher_id": assigned_teacher,
                        "subject_id": assigned_subject,
                        "classroom_id": assigned_room,
                        "time_slot": next_time_slot
                    })
                    section_subject_usage_tracker[section][assigned_subject] += 1
                    slot_index += 1  # Skip the next slot as it's taken by the lab subject

            slot_index += 1

        return section_schedule, teacher_availability_matrix


    def generate_daily_schedule(self, half_day_sections, section_subject_usage_tracker, day_index):
        daily_schedule = {}
        teacher_workload_tracker = self._initialize_teacher_workload_tracker()

        for section in self.sections_manager.sections:
            section_schedule, self.teacher_availability_matrix = self._generate_section_schedule(
                section, half_day_sections, section_subject_usage_tracker, teacher_workload_tracker, self.teacher_availability_matrix, day_index
            )
            daily_schedule[section] = section_schedule

        return daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix


    def _generate_weekly_schedule(self):
        weekly_schedule = {}
        section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping} for section in self.sections_manager.sections
        }

        for day_index, weekday in enumerate(self.weekdays):
            half_day_sections = self.sections_manager.sections[: len(self.sections_manager.sections)//2]
            daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix = self.generate_daily_schedule(
                half_day_sections, section_subject_usage_tracker, day_index
            )
            weekly_schedule[weekday] = daily_schedule

        return weekly_schedule, section_subject_usage_tracker, self.teacher_availability_matrix


    def create_timetable(self, num_weeks):
        timetable = {}

        for week_number in range(1, num_weeks + 1):
            weekly_schedule, _, self.teacher_availability_matrix = self._generate_weekly_schedule()
            timetable[f"Week {week_number}"] = weekly_schedule

        return timetable, self.teacher_availability_matrix