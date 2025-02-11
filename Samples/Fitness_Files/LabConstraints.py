import random
import json
from constants.time_intervals import TimeIntervalConstant

# Constants
LABS = ["Lab1", "Lab2", "Lab3", "Lab4"]
CLASSES = ["Class1", "Class2", "Class3", "Class4"]
TEACHERS = ["Teacher1", "Teacher2", "Teacher3", "Teacher4"]

# Constraints
MAX_LAB_COUNT = 2  # Max labs per week for a teacher
MAX_CLASS_COUNT = 3  # Max classes per week for a teacher
MAX_TEACHER_WORKLOAD = 5  # Max hours a teacher can work in a week
MAX_CONTINUOUS_CLASSES = 2  # Max consecutive hours for a teacher

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

# Initialize available time slots
TimeSlots = TimeIntervalConstant.time_slots  # Assuming TimeIntervalConstant has a list of time intervals


class TimetableFitness:
    def __init__(self):
        self.teachers = TEACHERS
        self.labs = LABS
        self.classes = CLASSES
        self.subject_workload = SUBJECT_WORKLOAD
        self.teacher_subjects = TEACHER_SUBJECTS
        self.teacher_schedule = {teacher: {} for teacher in self.teachers}
        self.section_strength = {cls: random.randint(40, 60) for cls in self.classes}

    def assign_classes_and_labs(self):
        """
        Assign classes and labs to teachers based on constraints and time slots.
        """
        for teacher in self.teachers:
            subjects = [subject for subject, teachers in TEACHER_SUBJECTS.items() if teacher in teachers]
            for subject in subjects:
                time_slot = random.choice(TimeSlots)  # Randomly select an available time slot
                if time_slot not in self.teacher_schedule[teacher]:
                    self.teacher_schedule[teacher][time_slot] = subject

    def LabNo(self):
        """
        Check if the number of labs assigned is within the constraints.
        """
        for teacher, schedule in self.teacher_schedule.items():
            lab_count = sum(1 for subject in schedule.values() if subject in self.labs)
            if lab_count > MAX_LAB_COUNT:
                return False
        return True

    def ClassNo(self):
        """
        Check if the number of classes assigned is within the constraints.
        """
        for teacher, schedule in self.teacher_schedule.items():
            class_count = sum(1 for subject in schedule.values() if subject in self.classes)
            if class_count > MAX_CLASS_COUNT:
                return False
        return True

    def TeacherWorkload(self):
        """
        Ensure total workload per teacher is within the limit.
        """
        for teacher, schedule in self.teacher_schedule.items():
            total_hours = sum(SUBJECT_WORKLOAD.get(subject, 0) for subject in schedule.values())
            if total_hours > MAX_TEACHER_WORKLOAD:
                return False
        return True

    def ContinuousClasses(self):
        """
        Ensure teachers do not have more than the allowed continuous classes.
        """
        for teacher, schedule in self.teacher_schedule.items():
            sorted_slots = sorted(schedule.keys())
            continuous_count = 0
            for i in range(len(sorted_slots) - 1):
                if TimeSlots.index(sorted_slots[i + 1]) - TimeSlots.index(sorted_slots[i]) == 1:
                    continuous_count += 1
                    if continuous_count > MAX_CONTINUOUS_CLASSES:
                        return False
                else:
                    continuous_count = 0
        return True

    def fitnessFunc(self):
        """
        Calculate fitness score based on all constraints.
        """
        fitness_score = 0

        if self.LabNo():
            fitness_score += 10
        else:
            fitness_score -= 10

        if self.ClassNo():
            fitness_score += 10
        else:
            fitness_score -= 10

        if self.TeacherWorkload():
            fitness_score += 10
        else:
            fitness_score -= 10

        if self.ContinuousClasses():
            fitness_score += 10
        else:
            fitness_score -= 10

        return fitness_score


# Main Execution
timetable_fitness = TimetableFitness()

# Assign classes and labs to teachers
timetable_fitness.assign_classes_and_labs()

# Calculate fitness score
fitness_score = timetable_fitness.fitnessFunc()

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
