import random
import json
from constants.TimeIntervals import TimeIntervalConstant
from constants.constant import WorkingDays

class TimetableFitness:
    def __init__(self):
        self.days = WorkingDays.days
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.time_slots

        # Teacher-subject mapping
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

        # Classroom and capacity details
        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.lab = ["L1", "L2", "L3", "L4", "L5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}

        # Data structures for tracking schedules
        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        self.room_schedule = {slot: {} for slot in self.time_slots}
        self.assigned_teachers = {section: {} for section in self.sections}
        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

        # Subject-specific constraints
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

        # Teacher constraints
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
                is_lab = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Handle special rules for Placement_Class and labs
                    if subject == "Placement_Class" and index != 6:
                        available_subjects.remove(subject)
                        continue

                    if "Lab" in subject or "PCS" in subject or "PMA" in subject:
                        if index not in [1, 3, 5]:
                            available_subjects.remove(subject)
                            continue
                        is_lab = True  # Mark this as a lab

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

                # Assign rooms based on whether it's a lab
                if is_lab:
                    assigned_room = random.choice(self.lab)
                else:
                    assigned_room = current_room

                self.teacher_schedule[index][teacher] = section
                self.room_schedule[index][assigned_room] = section

                # Handle double slot allocation for labs
                if is_lab and index in [1, 3, 5]:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append({
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": assigned_room,
                            "time_slot": next_time_slot
                        })
                        self.room_schedule[next_slot_index][assigned_room] = section
                        self.teacher_schedule[next_slot_index][teacher] = section

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot
                })

            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self, num_weeks=1):
        timetable = {}
        for week in range(1, num_weeks + 1):
            week_schedule = {}
            for week_day in self.days:
                half_day_sections = random.sample(self.sections, len(self.sections) // 2)
                week_schedule[week_day] = self.generate_day_schedule(week_day, half_day_sections, week)
            timetable[f"Week {week}"] = week_schedule
        return timetable

    def calculate_fitness(self, chromosome):
        week_fitness_scores = []
        section_fitness_scores = {}

        # Track fitness score for each week
        for week_num, (week, week_schedule) in enumerate(chromosome.items(), start=1):
            overall_fitness_score = 0
            week_section_scores = {}

            # Process day-wise schedules for the week
            for day, day_schedule in week_schedule.items():
                day_section_scores = {}

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

                        if "Break" in time_slot:
                            continue

                        if (teacher, time_slot) in teacher_time_slots:
                            section_score -= 30
                        else:
                            teacher_time_slots[(teacher, time_slot)] = section

                        if (classroom, time_slot) in classroom_time_slots:
                            section_score -= 20
                        else:
                            classroom_time_slots[(classroom, time_slot)] = section

                        if teacher not in teacher_load:
                            teacher_load[teacher] = []
                        teacher_load[teacher].append(time_slot)

                        if strength > self.room_capacity.get(classroom, 0):
                            section_score -= 25

                        preferred_slots = self.teacher_preferences.get(teacher, [])
                        if time_slot not in preferred_slots:
                            section_score -= 5

                    for teacher, time_slots in teacher_load.items():
                        if len(time_slots) > self.teacher_work_load.get(teacher, 5):
                            section_score -= 10

                    day_section_scores[section] = section_score
                    overall_fitness_score += section_score

                week_section_scores[day] = day_section_scores

            week_fitness_scores.append({
                "week": f"Week {week_num}",
                "score": overall_fitness_score
            })

            section_fitness_scores[f"Week {week_num}"] = week_section_scores

        return week_fitness_scores, section_fitness_scores


# Main Execution
timetable_fitness = TimetableFitness()
timetable = timetable_fitness.create_timetable(2)
week_fitness_scores, fitness_scores = timetable_fitness.calculate_fitness(timetable)

output = {
    "timetable": timetable,
    "week_fitness_scores": week_fitness_scores,
    "section_fitness_scores": fitness_scores
}

# Save output to a JSON file
with open("Samples/Sample_Chromosome.json", "w") as f:
    json.dump(output, f, indent=4)

