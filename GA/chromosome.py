import random
import copy
from math import ceil
from Constants.constant import Defaults
from Constants.constant import TeacherPreferences
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
        lab_availability_matrix: dict,  # New parameter
        time_slots: dict,
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
        self.teacher_assignment_tracker = teacher_subject_mapping
        self.teacher_availability_matrix = teacher_availability_matrix
        # Save the original lab matrix so that each generation starts fresh.
        self.initial_lab_availability_matrix = copy.deepcopy(lab_availability_matrix)
        self.lab_availability_matrix = copy.deepcopy(self.initial_lab_availability_matrix)

        self._map_sections_to_classrooms()

    def _map_sections_to_classrooms(self):
        sorted_classrooms = sorted(
            self.classrooms_manager.items(), key=lambda x: x[1], reverse=True
        )
        sorted_sections = sorted(
            self.sections_manager.items(), key=lambda x: x[1], reverse=True
        )
        self.section_to_classroom_map = {}
        for section, strength in sorted_sections:
            for i, (classroom, capacity) in enumerate(sorted_classrooms):
                if capacity >= strength:
                    self.section_to_classroom_map[section] = classroom
                    sorted_classrooms.pop(i)
                    break
        return self.section_to_classroom_map

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
        assigned_room = assigned_classroom  # For non-lab subjects

        for subject in available_subjects:
            if (subject in self.lab_subject_list or subject in self.special_subject_list) and slot_index not in [1, 3, 5]:
                continue
            if subject not in subjects_scheduled_today:
                teachers_for_subject = self.subject_teacher_mapping[subject]
                preferred_teachers = [
                    teacher for teacher in teachers_for_subject
                    if self.teacher_availability_preferences.get(teacher, [])
                ]
                sorted_teachers_by_load = sorted(preferred_teachers,
                                                 key=lambda t: teacher_workload_tracker[t])
                for teacher in sorted_teachers_by_load:
                    if (teacher in teacher_availability_matrix and
                        len(teacher_availability_matrix[teacher]) > day_index and
                        len(teacher_availability_matrix[teacher][day_index]) > (slot_index - 1) and
                        teacher_availability_matrix[teacher][day_index][slot_index - 1]):
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
            assigned_room = assigned_classroom

        return assigned_teacher, selected_subject, assigned_room

    def _initialize_teacher_workload_tracker(self):
        return {
            teacher: 0
            for teacher in self.weekly_workload
        }

    def _get_available_subjects(self, section, subject_usage_tracker):
        return [
            subject
            for subject in self.subject_teacher_mapping
            if subject_usage_tracker[section][subject] < self.subject_quota_limits.get(subject, 0)
        ]

    def _allocate_lab(self, teacher, subject, day_index, slot_index, section_strength):
        """
            Always split the section into two groups:
            Group sizes: group1 = ceil(section_strength/2), group2 = section_strength - group1.
            Try to find two distinct labs with two consecutive free slots.
        """

        group1_size = ceil(section_strength / 2)
        group2_size = section_strength - group1_size
        labs_list = list(self.lab_availability_matrix.keys())
        for i in range(len(labs_list)):
            lab1 = labs_list[i]
            if (self.lab_availability_matrix[lab1][day_index][slot_index - 1] and
                self.lab_availability_matrix[lab1][day_index][slot_index] and
                self.lab_capacity_manager.get(lab1, 0) >= group1_size):
                for j in range(i + 1, len(labs_list)):
                    lab2 = labs_list[j]
                    if (self.lab_availability_matrix[lab2][day_index][slot_index - 1] and
                        self.lab_availability_matrix[lab2][day_index][slot_index] and
                        self.lab_capacity_manager.get(lab2, 0) >= group2_size):
                        # Mark slots as occupied in the working copy
                        self.lab_availability_matrix[lab1][day_index][slot_index - 1] = False
                        self.lab_availability_matrix[lab1][day_index][slot_index] = False
                        self.lab_availability_matrix[lab2][day_index][slot_index - 1] = False
                        self.lab_availability_matrix[lab2][day_index][slot_index] = False
                        entries = [
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab1,
                                "time_slot": self.available_time_slots[slot_index],
                                "group": 1
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab1,
                                "time_slot": self.available_time_slots[slot_index+1],
                                "group": 1
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab2,
                                "time_slot": self.available_time_slots[slot_index],
                                "group": 2
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": lab2,
                                "time_slot": self.available_time_slots[slot_index+1],
                                "group": 2
                            },
                        ]

                        return entries, slot_index + 2

        # Fallback: if no pair found, return a merged allocation.
        merged_entry = {
            "teacher_id": teacher,
            "subject_id": subject,
            "classroom_id": "merged_lab",
            "time_slot": self.available_time_slots[slot_index],
            "group": "merged",
            "flagged": False
        }

        return [merged_entry], slot_index + 1


    def _generate_section_schedule(
        self,
        section,
        half_day_sections,
        section_subject_usage_tracker,
        teacher_workload_tracker,
        teacher_availability_matrix,
        day_index: int,
        section_strength: int,
        labs_capacity: dict,
    ):
        schedule = []
        subjects_scheduled_today = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots = 4 if section in half_day_sections else 7
        slot_index = 1

        while slot_index <= total_slots:
            time_slot = self.available_time_slots[slot_index]
            teacher, subject, room = self._assign_subject_and_teacher(
                section,
                slot_index,
                subjects_scheduled_today,
                assigned_classroom,
                section_subject_usage_tracker,
                teacher_workload_tracker,
                teacher_availability_matrix,
                day_index,
            )

            if subject in self.lab_subject_list or subject in self.special_subject_list:
                # Lab & Special subjects both require two consecutive slots
                if slot_index <= total_slots - 1:
                    if subject in self.lab_subject_list:
                        # Allocate lab for lab subjects
                        entries, new_slot_index = self._allocate_lab(
                            teacher, subject, day_index, slot_index, section_strength
                        )
                    else:
                        # Allocate a normal classroom for special subjects
                        entries = [
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": assigned_classroom,  # Special subjects use normal classrooms
                                "time_slot": self.available_time_slots[slot_index],
                                "group": "special_subject",
                            },
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": assigned_classroom,
                                "time_slot": self.available_time_slots[slot_index + 1],
                                "group": "special_subject",
                            },
                        ]
                        new_slot_index = slot_index + 2  # Move ahead by two slots

                    schedule.extend(entries)
                    section_subject_usage_tracker[section][subject] += len(entries)
                    slot_index = new_slot_index
                else:
                    # If at the end of the day and no space for 2 slots, fallback to single-slot assignment
                    schedule.append({
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_classroom,
                        "time_slot": time_slot,
                        "group": "fallback"
                    })
                    section_subject_usage_tracker[section][subject] += 1
                    slot_index += 1

            else:
                # General subjects get a single slot in a normal classroom
                schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": room,
                    "time_slot": time_slot,
                    "group": "all",
                })
                if subject != "Library":
                    section_subject_usage_tracker[section][subject] += 1
                slot_index += 1

        return schedule, teacher_availability_matrix



    def generate_daily_schedule(
        self,
        section_list,
        half_day_sections,
        section_subject_usage_tracker,
        day_index,
        teacher_workload_tracker
    ):
        daily_schedule = {}
        teacher_workload_tracker = self._initialize_teacher_workload_tracker()
        for section in section_list:
            section_strength = self.sections_manager[section]
            labs_capacity = self.lab_capacity_manager
            section_schedule, self.teacher_availability_matrix = self._generate_section_schedule(
                section,
                half_day_sections,
                section_subject_usage_tracker,
                teacher_workload_tracker,
                self.teacher_availability_matrix,
                day_index,
                section_strength,
                labs_capacity
            )
            daily_schedule[section] = section_schedule

        return daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix,teacher_workload_tracker

    def _generate_weekly_schedule(self):
        weekly_schedule = {}
        teacher_workload_tracker = self._initialize_teacher_workload_tracker()
        section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.keys()
        }

        section_list = list(self.sections_manager.keys())
        for day_index, weekday in enumerate(self.weekdays):
            random.shuffle(section_list)
            half_day_sections = section_list[: len(section_list) // 2]
            daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix,teacher_workload_tracker = self.generate_daily_schedule(
                section_list, half_day_sections, section_subject_usage_tracker, day_index,teacher_workload_tracker
            )
            weekly_schedule[weekday] = daily_schedule

        return weekly_schedule, section_subject_usage_tracker, self.teacher_availability_matrix

    def create_timetable(self, num_weeks):
        timetable = {}
        # Reset lab matrix to initial state for each timetable generation.
        for week_number in range(1, num_weeks + 1):
            self.lab_availability_matrix = copy.deepcopy(self.initial_lab_availability_matrix)
            weekly_schedule, _, self.teacher_availability_matrix = self._generate_weekly_schedule()
            timetable[f"Week {week_number}"] = weekly_schedule

        return timetable, self.teacher_availability_matrix, self.lab_availability_matrix
