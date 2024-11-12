import random

from constants.TimeIntervals import TimeIntervalConstant


class TimetableFitness:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots
        
        self.subject_teacher_map = {
            "TCS-531": ["AB01", "PK02"],
            "TCS-502": ["SS03", "AA04", "AC05"],
            "TCS-503": ["SP06", "DP07", "AC05"],
            "PCS-506": ["AD08", "RD09"],
            "TMA-502": ["BJ10", "RS11", "JM12", "NJ13"],
            "PMA-502": ["PM14", "AD08", "AA15"],
            "TCS-509": ["SJ16", "AB17", "HP18", "SG19"],
            "XCS-501": ["DT20", "PA21", "NB22"],
            "CSP-501": ["AK23"],
            "SCS-501": ["AP24"]
        }

        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}

        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        
        self.room_schedule = {slot: {} for slot in self.time_slots}
        
        self.assigned_teachers = {section: {} for section in self.sections}
        
        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

    def generate_day_schedule(self, day, sections_half_day):
        
        day_schedule = {}
        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]
            slots_to_run = [1, 2, 3, 4, 5] if section in sections_half_day else [1, 2, 3, 4, 5, 6, 7, 8]

            for index in slots_to_run:
                time_slot = self.time_slots[index]
                if "Break" in time_slot:
                    schedule_item = {
                        "teacher_id": "None",
                        "subject_id": "Break",
                        "classroom_id": "N/A",
                        "time_slot": time_slot
                    }
                else:
                    available_subjects = list(self.subject_teacher_map.keys())
                    subject, teacher = None, None

                    while available_subjects:
                        subject = random.choice(available_subjects)
                        if subject not in subjects_used_today:
                            if subject in self.assigned_teachers[section]:
                                teacher = self.assigned_teachers[section][subject]
                            else:
                                possible_teachers = self.subject_teacher_map[subject]
                                for candidate_teacher in possible_teachers:
                                    if candidate_teacher not in self.teacher_schedule[index].values():
                                        teacher = candidate_teacher
                                        self.assigned_teachers[section][subject] = teacher
                                        break
                            if teacher:
                                break
                        available_subjects.remove(subject)

                    if subject is None or teacher is None:
                        subject, teacher = "Library", "None"

                    subjects_used_today.add(subject)
                    self.teacher_schedule[index][teacher] = section
                    self.room_schedule[index][current_room] = section

                    if subject.startswith("PCS") or "Lab" in subject:
                        next_slot_index = index + 1
                        if next_slot_index in slots_to_run:
                            next_time_slot = self.time_slots[next_slot_index]
                            if "Break" not in next_time_slot:
                                section_schedule.append({
                                    "teacher_id": teacher,
                                    "subject_id": subject,
                                    "classroom_id": current_room,
                                    "time_slot": next_time_slot
                                })
                    
                    schedule_item = {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": current_room,
                        "time_slot": time_slot
                    }

                section_schedule.append(schedule_item)
            day_schedule[section] = section_schedule
        return day_schedule


    def create_timetable(self):
        timetable = {}
        for week_day in self.days:
            sections_half_day = random.sample(self.sections, len(self.sections) // 2)
            timetable[week_day] = self.generate_day_schedule(week_day, sections_half_day)
        return timetable


    def print_timetable(self, timetable):
        print("\n--- Weekly Timetable ---\n")
        for day, day_schedule in timetable.items():
            print(f"Day: {day}")
            for section, section_schedule in day_schedule.items():
                print(f"  Section: {section}")
                for item in section_schedule:
                    print(f"    {item['time_slot']}: {item['subject_id']} (Teacher: {item['teacher_id']}, Room: {item['classroom_id']})")
                print("  " + "-"*40)
            print("="*60)


# Usage
timetable = TimetableFitness()
weekly_schedule = timetable.create_timetable()
timetable.print_timetable(weekly_schedule)
