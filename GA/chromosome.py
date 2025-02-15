import random

from Constants.constant import Classrooms, Defaults, RoomCapacity, Sections
from Constants.time_intervals import TimeIntervalConstant


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
        time_slots:dict,
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
        self._map_sections_to_classrooms()
        self._assign_teachers_to_sections()

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
        assigned_room = None

        for subject in available_subjects:
            # If subject is a lab subject or "Placement_Class", force assignment only at specific slots.
            if (subject in self.lab_subject_list or subject == "Placement_Class") and slot_index not in [1, 3, 5]:
                continue

            if subject not in subjects_scheduled_today:
                teachers_for_subject = self.teacher_subject_mapping[subject]
                preferred_teachers = [
                    teacher for teacher in teachers_for_subject
                    if self.teacher_availability_preferences.get(teacher, [])
                ]
                sorted_teachers_by_load = sorted(preferred_teachers,
                                                 key=lambda teacher: teacher_workload_tracker[teacher])

                for teacher in sorted_teachers_by_load:
                    if (teacher in teacher_availability_matrix and
                            len(teacher_availability_matrix[teacher]) > day_index and
                            len(teacher_availability_matrix[teacher][day_index]) > (slot_index - 1) and
                            teacher_availability_matrix[teacher][day_index][slot_index - 1]):
                        assigned_teacher = teacher
                        teacher_workload_tracker[assigned_teacher] += 1
                        selected_subject = subject
                        subjects_scheduled_today.add(subject)
                        assigned_room = (
                            self.classrooms_manager.labs[slot_index % len(self.classrooms_manager.labs)]
                            if subject in self.lab_subject_list or subject == "Placement_Class"
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
                        # teacher_availability_matrix[teacher][day_index][slot_index - 1] = False
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
            day_index,
            section_strength=100,
            labs_capacity: dict = {"L1": 50, "L2": 50}
    ):
        section_schedule = []
        subjects_scheduled_today = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots = 4 if section in half_day_sections else 7
        slot_index = 1

        while slot_index <= total_slots:
            time_slot = self.available_time_slots[slot_index]
            assigned_teacher, assigned_subject, assigned_room = self._assign_subject_and_teacher(
                section, slot_index, subjects_scheduled_today, assigned_classroom,
                section_subject_usage_tracker, teacher_workload_tracker,
                teacher_availability_matrix, day_index
            )

            # Check if this subject must get 2 continuous hours.
            if (assigned_subject in self.lab_subject_list or assigned_subject == "Placement_Class"):
                # Check if splitting is needed (i.e. section strength exceeds the lab room capacity).
                if (section_strength is not None and labs_capacity is not None and
                        assigned_room in labs_capacity and section_strength > labs_capacity[assigned_room]):
                    # Try to find an alternate lab room for group 2.
                    lab2 = None
                    for lab in self.classrooms_manager.labs:
                        if lab != assigned_room and lab in labs_capacity:
                            if labs_capacity[lab] >= section_strength - labs_capacity[assigned_room]:
                                lab2 = lab
                                break
                    if lab2 is None:
                        raise ValueError("Insufficient lab capacity to split section for lab subject.")

                    # For splitting, ensure there are 4 consecutive slots available.
                    if slot_index + 3 <= total_slots:
                        ts1 = self.available_time_slots[slot_index]
                        ts2 = self.available_time_slots[slot_index + 1]
                        ts3 = self.available_time_slots[slot_index + 2]
                        ts4 = self.available_time_slots[slot_index + 3]

                        # Group 1 gets two slots in assigned_room.
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": assigned_room,
                            "time_slot": ts1,
                            "group": 1
                        })
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": assigned_room,
                            "time_slot": ts2,
                            "group": 1
                        })

                        # Group 2 gets two slots in lab2.
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": lab2,
                            "time_slot": ts3,
                            "group": 2
                        })
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": lab2,
                            "time_slot": ts4,
                            "group": 2
                        })
                        section_subject_usage_tracker[section][assigned_subject] += 4
                        slot_index += 4
                    else:
                        # Not enough slots for full split; fall back to non-split 2-hour allocation.
                        if slot_index + 1 <= total_slots:
                            next_time_slot = self.available_time_slots[slot_index + 1]
                            section_schedule.append({
                                "teacher_id": assigned_teacher,
                                "subject_id": assigned_subject,
                                "classroom_id": assigned_room,
                                "time_slot": time_slot,
                                "group": 1
                            })
                            section_schedule.append({
                                "teacher_id": assigned_teacher,
                                "subject_id": assigned_subject,
                                "classroom_id": assigned_room,
                                "time_slot": next_time_slot,
                                "group": 1
                            })
                            section_subject_usage_tracker[section][assigned_subject] += 2
                            slot_index += 2

                        else:
                            section_schedule.append({
                                "teacher_id": assigned_teacher,
                                "subject_id": assigned_subject,
                                "classroom_id": assigned_room,
                                "time_slot": time_slot,
                                "group": 1
                            })
                            section_subject_usage_tracker[section][assigned_subject] += 1
                            slot_index += 1

                else:
                    # No split needed; assign 2 consecutive slots in the same room.
                    if slot_index + 1 <= total_slots:
                        next_time_slot = self.available_time_slots[slot_index + 1]
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": assigned_room,
                            "time_slot": time_slot,
                            "group": 1
                        })
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": assigned_room,
                            "time_slot": next_time_slot,
                            "group": 1
                        })
                        section_subject_usage_tracker[section][assigned_subject] += 2
                        slot_index += 2
                    else:
                        section_schedule.append({
                            "teacher_id": assigned_teacher,
                            "subject_id": assigned_subject,
                            "classroom_id": assigned_room,
                            "time_slot": time_slot,
                            "group": 1
                        })
                        section_subject_usage_tracker[section][assigned_subject] += 1
                        slot_index += 1

            else:
                # For non-lab subjects, allocate a single slot.
                section_schedule.append({
                    "teacher_id": assigned_teacher,
                    "subject_id": assigned_subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot,
                    "group": "all"
                })
                if assigned_subject != "Library":
                    section_subject_usage_tracker[section][assigned_subject] += 1
                slot_index += 1

        return section_schedule, teacher_availability_matrix


    def generate_daily_schedule(self, section_list,half_day_sections,section_subject_usage_tracker, day_index):
        daily_schedule = {}
        teacher_workload_tracker = self._initialize_teacher_workload_tracker()

        for section in section_list:  # Iterate over half-day sections only
            section_schedule, self.teacher_availability_matrix = self._generate_section_schedule(
                section,
                half_day_sections,
                section_subject_usage_tracker,
                teacher_workload_tracker,
                self.teacher_availability_matrix,
                day_index
            )
            daily_schedule[section] = section_schedule

        return daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix


    def _generate_weekly_schedule(self):
        weekly_schedule = {}
        section_subject_usage_tracker = {
            section: {subject: 0 for subject in self.subject_teacher_mapping.keys()}
            for section in self.sections_manager.keys()
        }

        section_list = list(self.sections_manager.keys())

        for day_index, weekday in enumerate(self.weekdays):
            random.shuffle(section_list)
            half_day_sections = section_list[: len(section_list) // 2]
            daily_schedule, section_subject_usage_tracker, self.teacher_availability_matrix= self.generate_daily_schedule(
                section_list,half_day_sections, section_subject_usage_tracker, day_index
            )

            weekly_schedule[weekday] = daily_schedule
        return weekly_schedule, section_subject_usage_tracker, self.teacher_availability_matrix


    def create_timetable(self, num_weeks):
        timetable = {}

        for week_number in range(1, num_weeks + 1):
            weekly_schedule, _, self.teacher_availability_matrix = self._generate_weekly_schedule()
            timetable[f"Week {week_number}"] = weekly_schedule

        return timetable, self.teacher_availability_matrix
