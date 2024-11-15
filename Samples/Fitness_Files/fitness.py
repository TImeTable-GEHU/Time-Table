import random
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import WorkingDays

class TimetableFitness:
    def __init__(self):
        self.days = WorkingDays.days
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
            "SCS-501": ["AP24"],
            "PCS-503": ["RS11", "DP07", "SP06", "VD25"],
            "Placement_Class": ["AK26"]
        }

        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        self.room_schedule = {slot: {} for slot in self.time_slots}
        self.assigned_teachers = {section: {} for section in self.sections}

        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

        self.subject_weekly_quota = {
            "TCS-531": 3,
            "TCS-502": 3,
            "TCS-503": 3,
            "PCS-506": 1,
            "PCS-503": 1,
            "TMA-502": 3,
            "PMA-502": 1,
            "TCS-509": 3,
            "XCS-501": 2,
            "CSP-501": 1,
            "SCS-501": 1,
            "Placement_Class": 1
        }

        self.weekly_assignments = {section: {subject: 0 for subject in self.subject_weekly_quota} for section in self.sections}

        self.teacher_preferences = {
            teacher_id: [1, 2, 3, 4, 5, 6, 7] for teacher_id in [teacher for teachers in self.subject_teacher_map.values() for teacher in teachers]
        }

        self.teacher_work_load = {teacher: 5 for teacher in self.teacher_preferences}
        self.teacher_assignments = {}

    def generate_day_schedule(self, day, half_day_sections, week_number):
        day_schedule = {}
        subject_teacher_usage = {subject: iter(teachers) for subject, teachers in self.subject_teacher_map.items()}

        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]
            num_slots = 4 if section in half_day_sections else 7

            for index in range(1, num_slots + 1):
                time_slot = self.time_slots[index]

                if any(item['time_slot'] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None

                while available_subjects:
                    subject = random.choice(available_subjects)

                    if subject == "Placement_Class" and index != 5:
                        available_subjects.remove(subject)
                        continue

                    if ("PCS" in subject or "PMA" in subject or "Placement_Class" in subject) and index not in [1, 3, 5]:
                        available_subjects.remove(subject)
                        continue

                    if subject not in subjects_used_today:
                        teacher_iter = subject_teacher_usage[subject]

                        try:
                            teacher = next(teacher_iter)
                            self.teacher_assignments.setdefault(section, {})[subject] = teacher
                        except StopIteration:
                            teacher_iter = iter(self.subject_teacher_map[subject])
                            teacher = next(teacher_iter)
                            subject_teacher_usage[subject] = teacher_iter
                            self.teacher_assignments.setdefault(section, {})[subject] = teacher

                        break

                    available_subjects.remove(subject)

                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"

                if subject != "Library":
                    self.weekly_assignments[section][subject] += 1

                subjects_used_today.add(subject)
                self.teacher_schedule[index][teacher] = section
                self.room_schedule[index][current_room] = section

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": current_room,
                    "time_slot": time_slot
                })

            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self, num_weeks=1):
        timetable = {}
        for week in range(1, num_weeks + 1):
            for week_day in self.days:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                timetable[f"Week {week} - {week_day}"] = self.generate_day_schedule(week_day, half_day_sections, week)
        return timetable

    def print_timetable(self, timetable):
        print("\n--- Weekly Timetable ---\n")
        for week_num in range(1, len(timetable)//len(self.days)+1):
            print(f"Week {week_num}")
            for day, day_schedule in timetable.items():
                if f"Week {week_num}" in day:
                    print(f"\nDay: {day}")
                    for section, section_schedule in day_schedule.items():
                        print(f"  Section: {section}")
                        for item in section_schedule:
                            print(f"    {item['time_slot']}: {item['subject_id']} (Teacher: {item['teacher_id']}, Room: {item['classroom_id']})")
                        print("  " + "-"*40)
            fitness_score, section_scores = self.calculate_fitness(timetable)
            print(f"Fitness Score for Week {week_num}: {fitness_score}")
            print("="*60)

    def calculate_fitness(self, chromosome):
        overall_fitness_score = 0
        section_fitness_scores = {}
        max_score_per_day = 100 * len(self.sections)

        for day, day_schedule in chromosome.items():
            section_fitness_scores[day] = {}
            for section, section_schedule in day_schedule.items():
                section_score = 100
                teacher_time_slots = {}
                classroom_time_slots = {}
                teacher_load = {}

                for item in section_schedule:
                    teacher = item['teacher_id']
                    classroom = item['classroom_id']
                    time_slot = item['time_slot']
                    strength = self.section_strength.get(section, 0)

                    if (teacher, time_slot) in teacher_time_slots:
                        section_score -= 40
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section

                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 30
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section

                    if strength > self.room_capacity.get(classroom, 0):
                        section_score -= 50

                    preferred_slots = self.teacher_preferences.get(teacher, [])
                    if time_slot not in preferred_slots:
                        section_score -= 10

                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)

                for teacher, time_slots in teacher_load.items():
                    if len(time_slots) > self.teacher_work_load.get(teacher, 5):
                        section_score -= (len(time_slots) - self.teacher_work_load[teacher]) * 20

                section_fitness_scores[day][section] = max(0, section_score)
                overall_fitness_score += max(0, section_score)

        total_possible_score = max_score_per_day * len(chromosome)
        overall_fitness_score = (overall_fitness_score / total_possible_score) * 100

        return overall_fitness_score, section_fitness_scores

# Example usage
timetable_fitness = TimetableFitness()
timetable = timetable_fitness.create_timetable(5)
timetable_fitness.print_timetable(timetable)
