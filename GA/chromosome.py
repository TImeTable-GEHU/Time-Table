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
        labs: dict,
        subject_quota_limits: dict,
        labs_list: list,
        teacher_duty_days: dict,
        teacher_availability_matrix=None,
        teacher_department_mapping=dict
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
        self.teacher_assignment_tracker = {t: 0 for t in teacher_weekly_workload}
        self.teacher_availability_matrix = teacher_availability_matrix
        self._map_sections_to_classrooms()
        self._teacher_section()

    def _map_sections_to_classrooms(self):
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
                if (
                    self.room_capacity_manager.room_capacity[classroom]
                    >= self.room_capacity_manager.section_strength[section]
                ):
                    self.section_to_classroom_map[section] = classroom
                    sorted_classrooms.remove(classroom)
                    break

    def _teacher_section(self):
        self.teacher_section_map = {
            s: {sub: None for sub in self.subject_teacher_mapping} for s in self.sections_manager.sections
        }
        for s in self.sections_manager.sections:
            for sub, t_list in self.subject_teacher_mapping.items():
                t_list_sorted = sorted(t_list, key=lambda t: self.teacher_assignment_tracker[t])
                chosen = t_list_sorted[0]
                self.teacher_section_map[s][sub] = chosen
                self.teacher_assignment_tracker[chosen] += 1

    def _initialize_teacher_workload_tracker(self):
        return {t: 0 for t in self.weekly_workload}

    def _get_available_subjects(self, section, usage):
        return [
            sub for sub in self.subject_teacher_mapping
            if usage[section][sub] < self.subject_quota_limits.get(sub, 0)
        ]

    def _assign_subject_and_teacher(
        self,
        section,
        slot_index,
        used_today,
        assigned_classroom,
        usage,
        teacher_load,
        availability_matrix,
        day_index,
        total_slots
    ):
        subs = self._get_available_subjects(section, usage)
        random.shuffle(subs)
        teacher, chosen_sub, room = None, None, None
        for sub in subs:
            if sub in self.lab_subject_list and slot_index not in [1, 3, 5]:
                continue
            if sub in self.special_subject_list and slot_index not in [5]:
                continue
            if sub not in used_today:
                t_list = self.subject_teacher_mapping[sub]
                preferred = [tt for tt in t_list if self.teacher_availability_preferences.get(tt, [])]
                preferred_sorted = sorted(preferred, key=lambda x: teacher_load[x])
                for t in preferred_sorted:
                    if (
                        t in availability_matrix
                        and len(availability_matrix[t]) > day_index
                        and len(availability_matrix[t][day_index]) > (slot_index - 1)
                        and availability_matrix[t][day_index][slot_index - 1]
                    ):
                        teacher = t
                        teacher_load[teacher] += 1
                        chosen_sub = sub
                        used_today.add(sub)
                        room = (
                            self.classrooms_manager.labs[slot_index % len(self.classrooms_manager.labs)]
                            if sub in self.lab_subject_list
                            else assigned_classroom
                        )
                        break
            if teacher:
                break
        if not teacher:
            chosen_sub, teacher, room = "Library", "None", assigned_classroom
        return teacher, chosen_sub, room

    def _generate_section_schedule(
        self, section, half_day_sections, usage, teacher_load, availability_matrix, day_index
    ):
        schedule = []
        used_subs = set()
        assigned_classroom = self.section_to_classroom_map[section]
        total_slots = 4 if section in half_day_sections else 7
        slot_idx = 1
        while slot_idx <= total_slots:
            time_slot = self.available_time_slots[slot_idx]
            a_teacher, a_sub, a_room = self._assign_subject_and_teacher(
                section, slot_idx, used_subs, assigned_classroom, usage,
                teacher_load, availability_matrix, day_index, total_slots
            )
            schedule.append({
                "teacher_id": a_teacher,
                "subject_id": a_sub,
                "classroom_id": a_room,
                "time_slot": time_slot
            })
            if a_sub != "Library":
                usage[section][a_sub] += 1
            if a_sub in self.lab_subject_list or a_sub in self.special_subject_list:
                nxt = slot_idx + 1
                if nxt <= total_slots:
                    next_time = self.available_time_slots[nxt]
                    schedule.append({
                        "teacher_id": a_teacher,
                        "subject_id": a_sub,
                        "classroom_id": a_room,
                        "time_slot": next_time
                    })
                    usage[section][a_sub] += 1
                    slot_idx += 1
            slot_idx += 1
        return schedule, availability_matrix

    def generate_daily_schedule(self, half_day_sections, usage, day_index):
        daily = {}
        teacher_load = self._initialize_teacher_workload_tracker()
        for s in self.sections_manager.sections:
            sec_sched, self.teacher_availability_matrix = self._generate_section_schedule(
                s, half_day_sections, usage, teacher_load, self.teacher_availability_matrix, day_index
            )
            daily[s] = sec_sched
        return daily, usage, self.teacher_availability_matrix

    def _generate_weekly_schedule(self):
        week_data = {}
        usage_tracker = {
            s: {sub: 0 for sub in self.subject_teacher_mapping} for s in self.sections_manager.sections
        }
        for i, w_day in enumerate(self.weekdays):
            half_day = self.sections_manager.sections[: len(self.sections_manager.sections)//2]
            d, usage_tracker, self.teacher_availability_matrix = self.generate_daily_schedule(
                half_day, usage_tracker, i
            )
            week_data[w_day] = d
        return week_data, usage_tracker, self.teacher_availability_matrix

    def create_timetable(self, num_weeks):
        timetable = {}
        for w in range(1, num_weeks + 1):
            ws, u_tracker, self.teacher_availability_matrix = self._generate_weekly_schedule()
            timetable[f"Week {w}"] = ws
        return timetable, self.teacher_availability_matrix