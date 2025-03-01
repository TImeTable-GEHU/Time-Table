class Defaults:
    room_capacity = 60
    working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    starting_section_fitness = 1000
    max_class_capacity = 250
    initial_no_of_chromosomes = 1000
    total_no_of_generations = 100
    class_strength = 50



class TeacherPreferences:
    def __init__(self, teacher_weekly_workload: dict):
        self.teacher_preferences = {}
        for teacher, workload in teacher_weekly_workload.items():
            self.teacher_preferences[teacher] = list(range(1, 8))

    def get_preferences(self):
        return self.teacher_preferences


class SubjectWeeklyQuota:
    def __init__(self, subject_quota):
        self.subject_quota = subject_quota


class TeacherPreloads:
    def __init__(self, teacher_preferences: dict, weekly_workload: dict):
        self.teacher_preferences = teacher_preferences
        self.weekly_workload = weekly_workload


class TeachersDutyDays:
    def __init__(self, teacher_duty_days: dict):
        self.teacher_duty_days = teacher_duty_days


class SpecialSubjects:
    def __init__(
        self, special_subjects: list, labs: list, specialization_subjects: list
    ):
        self.special_subjects = special_subjects
        self.labs = labs
        self.specialization_subjects = specialization_subjects


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10
    PENALTY_NON_DUTY_DAY = 40


class SectionsConstants:
    # Define attribute weights and conditions
    ATTRIBUTE_WEIGHTS = {
        "good_cgpa": 1,  # 2^0
        "hostler": 2,  # 2^1
    }

    ATTRIBUTE_CONDITIONS = {
        "hostler": lambda student: student.get("Hostler", False),
    }
