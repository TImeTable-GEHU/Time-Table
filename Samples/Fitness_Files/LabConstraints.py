import random
import json
from constants.TimeIntervals import TimeIntervalConstant

# Constants
LABS = ["Lab1", "Lab2", "Lab3", "Lab4"]
CLASSES = ["Class1", "Class2", "Class3", "Class4"]
TEACHERS = ["Teacher1", "Teacher2", "Teacher3", "Teacher4"]

# Constraints
MAX_LAB_COUNT = 2  # Max number of labs per week for a teacher
MAX_CLASS_COUNT = 3  # Max number of classes per week for a teacher
MAX_TEACHER_WORKLOAD = 5  # Max hours a teacher can work in a week

# Workload for subjects
SUBJECT_WORKLOAD = {
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

# Teacher availability and subjects they teach
TEACHER_SUBJECTS = {
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

# Initialize available time slots from TimeIntervalConstant
TimeSlots = TimeIntervalConstant.time_slots  # Assuming SLOTS is a list of time intervals

class TimetableFitness:
    def __init__(self):
        self.teachers = TEACHERS
        self.labs = LABS
        self.classes = CLASSES
        self.subject_workload = SUBJECT_WORKLOAD
        self.teacher_subjects = TEACHER_SUBJECTS
        self.teacher_schedule = {teacher: {} for teacher in self.teachers}
        self.section_strength = {cls: random.randint(40, 60) for cls in self.classes}  # Dynamic student count

    def assign_classes_and_labs(self):
        """
        Assign classes and labs to teachers based on constraints and time slots.
        """
        for teacher in self.teachers:
            subjects = self.teacher_subjects.get(teacher, [])
            total_hours = sum(self.subject_workload.get(subject, 0) for subject in subjects)

            if total_hours <= MAX_TEACHER_WORKLOAD:
                for subject in subjects:
                    # Assign classes or labs to available time slots
                    time_slot = random.choice(time_slot)
                    self.teacher_schedule[teacher][time_slot] = subject
            else:
                print(f"Teacher {teacher} exceeds max workload!")

    def fitness_func(self):
        """
        Calculate fitness score based on various constraints.
        """
        fitness_score = 0

        # 1. Validate teacher workload and schedule constraints
        for teacher, schedule in self.teacher_schedule.items():
            lab_count = sum(1 for slot, subject in schedule.items() if subject in self.labs)
            class_count = sum(1 for slot, subject in schedule.items() if subject in self.classes)
            total_hours = sum(self.subject_workload.get(subject, 0) for subject in schedule.values())

            if lab_count + class_count <= (MAX_LAB_COUNT + MAX_CLASS_COUNT) and total_hours <= MAX_TEACHER_WORKLOAD:
                fitness_score += 10  # Valid schedule
            else:
                fitness_score -= 10  # Invalid schedule

        # 2. Ensure no overlapping time slots
        all_schedules = [schedule for teacher, schedule in self.teacher_schedule.items()]
        used_slots = set()
        for schedule in all_schedules:
            for time_slot in schedule.keys():
                if time_slot in used_slots:
                    fitness_score -= 5  # Overlapping slot
                else:
                    used_slots.add(time_slot)

        return fitness_score

# Main Execution
timetable_fitness = TimetableFitness()

# Assign classes and labs to teachers
timetable_fitness.assign_classes_and_labs()

# Calculate fitness score
fitness_score = timetable_fitness.fitness_func()

# Output
print(f"Final Fitness Score: {fitness_score}")

# Save results to a JSON file
output = {
    "teacher_schedule": timetable_fitness.teacher_schedule,
    "fitness_score": fitness_score,
    "section_strength": timetable_fitness.section_strength
}
with open("Timetable_Fitness_Result.json", "w") as f:
    json.dump(output, f, indent=4)
    