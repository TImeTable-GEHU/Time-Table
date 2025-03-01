import copy
import random
from math import ceil

from Constants.constant import Defaults


class TimeTableGeneration:
    def __init__(
        self,
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
        time_slots: dict,
        fixed_teacher_assignment: dict = None,
    ):
        self.sections_manager = total_sections
        self.classrooms_manager = total_classrooms
        self.lab_capacity_manager = total_labs
        self.weekdays = Defaults.working_days
        self.subject_teacher_mapping = teacher_subject_mapping
        self.subject_quota_limits = subject_quota_limits
        self.lab_subject_list = labs
        self.special_subject_list = special_subjects
        self.teacher_availability_preferences = teacher_preferences
        self.available_time_slots = time_slots
        self.teacher_duty_days = teacher_duty_days
        self.weekly_workload = teacher_weekly_workload
        self.teacher_availability_matrix = teacher_availability_matrix
        self.initial_lab_availability_matrix = copy.deepcopy(lab_availability_matrix)
        self.lab_availability_matrix = copy.deepcopy(self.initial_lab_availability_matrix)
        self.fixed_teacher_assignment = fixed_teacher_assignment or {}
        self._map_sections_to_classrooms()

    def _map_sections_to_classrooms(self) -> dict:
        sorted_classrooms = sorted(
            self.classrooms_manager.items(),
            key = lambda item: item[1],
            reverse=True
        )
        sorted_sections = sorted(
            self.sections_manager.items(),
            key = lambda item: item[1],
            reverse = True
        )
        section_classroom_map = {}

        for section, student_count in sorted_sections:
            for index, (classroom, capacity) in enumerate(sorted_classrooms):
                if capacity >= student_count:
                    section_classroom_map[section] = classroom
                    sorted_classrooms.pop(index)
                    break

        self.section_to_classroom_map = section_classroom_map
        return section_classroom_map


    def _initialize_teacher_workload_tracker(self) -> dict:
        return {
            teacher: 0
            for teacher in self.weekly_workload
        }


    def _get_available_subjects(self, section: str, subject_usage_tracker: dict) -> list:
        return [
            subject
            for subject in self.subject_teacher_mapping
            if subject_usage_tracker[section][subject] < self.subject_quota_limits.get(subject, 0)
        ]


    def _assign_subject_and_teacher(
        self,
        section: str,
        slot_index: int,
        subjects_scheduled_today: set,
        assigned_classroom: str,
        subject_usage_tracker: dict,
        teacher_workload_tracker: dict,
        teacher_availability_matrix: dict,
        day_index: int,
    ) -> tuple:
        available_subjects = self._get_available_subjects(section, subject_usage_tracker)
        random.shuffle(available_subjects)
        assigned_teacher = None
        selected_subject = None
        assigned_room = assigned_classroom

        for subject in available_subjects:
            if (subject in self.lab_subject_list or subject == "Placement_Class") and slot_index not in [1, 3, 5]:
                continue
            if subject not in subjects_scheduled_today:
                # First, check for a fixed teacher assignment for (section, subject)
                fixed_teacher = self.fixed_teacher_assignment.get(section, {}).get(subject)
                if fixed_teacher:
                    if (
                        fixed_teacher in teacher_availability_matrix and
                        len(teacher_availability_matrix[fixed_teacher]) > day_index and
                        len(teacher_availability_matrix[fixed_teacher][day_index]) > (slot_index - 1) and
                        teacher_availability_matrix[fixed_teacher][day_index][slot_index - 1]
                    ):
                        assigned_teacher = fixed_teacher
                        teacher_workload_tracker[fixed_teacher] += 1
                        selected_subject = subject
                        subjects_scheduled_today.add(subject)
                        break

                # Otherwise, assign normally from the available pool
                teachers = self.subject_teacher_mapping[subject]
                preferred_teachers = [
                    t for t in teachers if self.teacher_availability_preferences.get(t, [])
                ]
                for teacher in sorted(preferred_teachers, key=lambda t: teacher_workload_tracker[t]):
                    if (
                        teacher in teacher_availability_matrix and
                        len(teacher_availability_matrix[teacher]) > day_index and
                        len(teacher_availability_matrix[teacher][day_index]) > (slot_index - 1) and
                        teacher_availability_matrix[teacher][day_index][slot_index - 1]
                    ):
                        assigned_teacher = teacher
                        teacher_workload_tracker[teacher] += 1
                        selected_subject = subject
                        subjects_scheduled_today.add(subject)
                        break

            if assigned_teacher:
                break

        if not assigned_teacher:
            selected_subject = "Library"
            assigned_teacher = "None"
        return assigned_teacher, selected_subject, assigned_room


    def _allocate_lab(
        self,
        teacher: str,
        subject: str,
        day_index: int,
        slot_index: int,
        section_strength: int,
    ) -> tuple:
        group1_size = ceil(section_strength / 2)
        group2_size = section_strength - group1_size
        labs_list = list(self.lab_availability_matrix.keys())

        for i in range(len(labs_list)):
            lab1 = labs_list[i]
            if (
                self.lab_availability_matrix[lab1][day_index][slot_index - 1]
                and self.lab_availability_matrix[lab1][day_index][slot_index]
                and self.lab_capacity_manager.get(lab1, 0) >= group1_size
            ):
                for j in range(i + 1, len(labs_list)):
                    lab2 = labs_list[j]
                    if (
                        self.lab_availability_matrix[lab2][day_index][slot_index - 1]
                        and self.lab_availability_matrix[lab2][day_index][slot_index]
                        and self.lab_capacity_manager.get(lab2, 0) >= group2_size
                    ):
                        self.lab_availability_matrix[lab1][day_index][
                            slot_index - 1
                        ] = False
                        self.lab_availability_matrix[lab1][day_index][
                            slot_index
                        ] = False
                        self.lab_availability_matrix[lab2][day_index][
                            slot_index - 1
                        ] = False
                        self.lab_availability_matrix[lab2][day_index][
                            slot_index
                        ] = False
                        entries = [
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab1,
                                "time_slot": self.available_time_slots[slot_index],
                                "group": 1,
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab1,
                                "time_slot": self.available_time_slots[slot_index + 1],
                                "group": 1,
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab2,
                                "time_slot": self.available_time_slots[slot_index],
                                "group": 2,
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab2,
                                "time_slot": self.available_time_slots[slot_index + 1],
                                "group": 2,
                            },
                        ]
                        return entries, slot_index + 2

        merged_entry = {
            "teacher_id": teacher,
            "subject_id": subject,
            "classroom_id": "merged_lab",
            "time_slot": self.available_time_slots[slot_index],
            "group": "merged",
            "flagged": False,
        }
        return [merged_entry], slot_index + 1


    def _generate_section_schedule(
        self,
        section: str,
        half_day_sections: list,
        subject_usage_tracker: dict,
        teacher_workload_tracker: dict,
        teacher_availability_matrix: dict,
        day_index: int,
        section_strength: int,
    ) -> tuple:
        schedule = []
        subjects_scheduled = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots = 4 if section in half_day_sections else 7
        slot_index = 1

        while slot_index <= total_slots:
            teacher, subject, room = self._assign_subject_and_teacher(
                section,
                slot_index,
                subjects_scheduled,
                assigned_classroom,
                subject_usage_tracker,
                teacher_workload_tracker,
                teacher_availability_matrix,
                day_index,
            )
            time_slot = self.available_time_slots[slot_index]
            if subject in self.lab_subject_list or subject == "Placement_Class":
                if slot_index <= total_slots - 1:
                    lab_entries, slot_index = self._allocate_lab(
                        teacher, subject, day_index, slot_index, section_strength
                    )
                    schedule.extend(lab_entries)
                    subject_usage_tracker[section][subject] += len(lab_entries)
                else:
                    schedule.append(
                        {
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": assigned_classroom,
                            "time_slot": time_slot,
                            "group": "fallback",
                        }
                    )
                    subject_usage_tracker[section][subject] += 1
                    slot_index += 1
            else:
                schedule.append(
                    {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": room,
                        "time_slot": time_slot,
                        "group": "all",
                    }
                )
                if subject != "Library":
                    subject_usage_tracker[section][subject] += 1
                slot_index += 1

        return schedule, teacher_availability_matrix


    def generate_daily_schedule(
        self,
        sections: list,
        half_day_sections: list,
        subject_usage_tracker: dict,
        day_index: int,
    ) -> tuple:
        daily_schedule = {}
        teacher_workload = self._initialize_teacher_workload_tracker()
        for section in sections:
            section_strength = self.sections_manager[section]
            (
                schedule,
                self.teacher_availability_matrix,
            ) = self._generate_section_schedule(
                section,
                half_day_sections,
                subject_usage_tracker,
                teacher_workload,
                self.teacher_availability_matrix,
                day_index,
                section_strength,
            )
            daily_schedule[section] = schedule
        return daily_schedule, subject_usage_tracker, self.teacher_availability_matrix


    def _generate_weekly_schedule(self) -> tuple:
        weekly_schedule = {}
        subject_usage = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.keys()
        }
        sections = list(self.sections_manager.keys())
        for day_index, weekday in enumerate(self.weekdays):
            random.shuffle(sections)
            half_day = sections[: len(sections) // 2]
            (
                daily_sched,
                subject_usage,
                self.teacher_availability_matrix,
            ) = self.generate_daily_schedule(
                sections, half_day, subject_usage, day_index
            )
            weekly_schedule[weekday] = daily_sched
        return weekly_schedule, subject_usage, self.teacher_availability_matrix


    def create_timetable(self, num_weeks: int) -> tuple:
        timetable = {}
        for week in range(1, num_weeks + 1):
            self.lab_availability_matrix = copy.deepcopy(
                self.initial_lab_availability_matrix
            )
            (
                weekly_schedule,
                _,
                self.teacher_availability_matrix,
            ) = self._generate_weekly_schedule()
            timetable[f"Week {week}"] = weekly_schedule
        return timetable, self.teacher_availability_matrix, self.lab_availability_matrix
