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
        self.weekly_workload = teacher_weekly_workload

        self.teacher_assignment_tracker = {teacher: 0 for teacher in teacher_weekly_workload.keys()}
        self._map_sections_to_classrooms()
        self._teacher_section()

    def _map_sections_to_classrooms(self):
        """Map sections to classrooms based on capacity."""
        sorted_classrooms = sorted(
            self.classrooms_manager.classrooms,
            key=lambda c: self.room_capacity_manager.room_capacity[c],
            reverse=True,
        )
        sorted_sections = sorted(
            self.sections_manager.sections,
            key=lambda s: self.room_capacity_manager.section_strength[s],
            reverse=True,
        )

        self.section_to_classroom_map = {}
        for section in sorted_sections:
            for classroom in sorted_classrooms:
                if self.room_capacity_manager.room_capacity[classroom] >= self.room_capacity_manager.section_strength[section]:
                    self.section_to_classroom_map[section] = classroom
                    sorted_classrooms.remove(classroom)
                    break
            else:
                raise ValueError(
                    f"No classroom can accommodate section {section} with strength {self.room_capacity_manager.section_strength[section]}."
                )

    def _teacher_section(self):
        """Map sections to teachers and subjects, ensuring balanced assignments."""
        self.teacher_section_map = {
            section: {subject: None for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.sections
        }

        for section in self.sections_manager.sections:
            for subject, teachers in self.subject_teacher_mapping.items():
                # Select teacher with the least workload
                teachers_with_least_load = sorted(
                    teachers, key=lambda teacher: self.teacher_assignment_tracker[teacher]
                )
                selected_teacher = teachers_with_least_load[0]
                self.teacher_section_map[section][subject] = selected_teacher
                self.teacher_assignment_tracker[selected_teacher] += 1

    def _initialize_teacher_workload_tracker(self):
        """Initialize a tracker for teacher workloads."""
        return {teacher: 0 for teacher in self.weekly_workload.keys()}

    def _generate_section_schedule(
        self, section, half_day_section_list, section_subject_usage_tracker, teacher_workload_tracker
    ):
        """Generate a schedule for an individual section."""
        section_schedule = []
        subjects_scheduled_today = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots_for_section = 4 if section in half_day_section_list else 7

        for slot_index, current_time_slot in enumerate(self.available_time_slots.values(), start=1):
            if slot_index > total_slots_for_section:
                break

            assigned_teacher, selected_subject, assigned_room = self._assign_subject_and_teacher(
                section,
                slot_index,
                subjects_scheduled_today,
                assigned_classroom,
                section_subject_usage_tracker,
                teacher_workload_tracker,
            )
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

            # Handle double-slot subjects
            if selected_subject in self.lab_subject_list and slot_index + 1 <= total_slots_for_section:
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
        return section_schedule

    def _assign_subject_and_teacher(
        self,
        section,
        slot_index,
        subjects_scheduled_today,
        assigned_classroom,
        section_subject_usage_tracker,
        teacher_workload_tracker,
    ):
        """Assign a subject and teacher for a specific slot."""
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
                teachers_with_least_load = sorted(
                    teachers_for_subject, key=lambda teacher: teacher_workload_tracker[teacher]
                )
                assigned_teacher = teachers_with_least_load[0]
                teacher_workload_tracker[assigned_teacher] += 1
                selected_subject = subject
                subjects_scheduled_today.add(subject)
                assigned_room = (
                    self.classrooms_manager.labs[slot_index % len(self.classrooms_manager.labs)]
                    if subject in self.lab_subject_list
                    else assigned_classroom
                )
                break

        if not assigned_teacher:
            selected_subject = "Library"
            assigned_teacher = "None"
            assigned_room = assigned_classroom

        return assigned_teacher, selected_subject, assigned_room

    def _get_available_subjects(self, section, section_subject_usage_tracker):
        """Get a list of subjects available for a specific section."""
        return [
            subject
            for subject in self.subject_teacher_mapping.keys()
            if section_subject_usage_tracker[section][subject] < self.subject_quota_limits.get(subject, 0)
        ]

    def generate_daily_schedule(self, half_day_section_list, section_subject_usage_tracker):
        """Generate the daily schedule for all sections."""
        daily_schedule = {}
        teacher_workload_tracker = self._initialize_teacher_workload_tracker()

        for section in self.sections_manager.sections:
            section_schedule = self._generate_section_schedule(
                section, half_day_section_list, section_subject_usage_tracker, teacher_workload_tracker
            )
            daily_schedule[section] = section_schedule

        return daily_schedule, section_subject_usage_tracker

    def _generate_weekly_schedule(self):
        """Generate a schedule for a single week."""
        week_schedule = {}
        section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.sections
        }
        for week_day in self.weekdays:
            half_day_sections = self.sections_manager.sections[: len(self.sections_manager.sections) // 2]
            daily_schedule, section_subject_usage_tracker = self.generate_daily_schedule(
                half_day_sections, section_subject_usage_tracker
            )
            week_schedule[week_day] = daily_schedule
        return week_schedule, section_subject_usage_tracker

    def create_timetable(self, num_weeks):
        """Create the timetable for the given number of weeks."""
        timetable = {}
        for week in range(1, num_weeks + 1):
            week_schedule, section_subject_usage_tracker = self._generate_weekly_schedule()
            timetable[f"Week {week}"] = week_schedule
        return timetable
