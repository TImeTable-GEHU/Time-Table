class Defaults:
    # All the defaults values over GA folder.
    room_capacity = 60
    working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    starting_section_fitness = 1000
    max_class_capacity = 250
    initial_no_of_chromosomes = 10
    total_no_of_generations = 10


class Sections:
    def __init__(self, section_number):
        self.sections = [chr(65 + i) for i in range(section_number)]


class Classrooms:
    def __init__(self, room_count, lab_count):
        self.classrooms = [f"R{i + 1}" for i in range(room_count)]
        self.labs = [f"L{i + 1}" for i in range(lab_count)]


class RoomCapacity:
    def __init__(self, classrooms, sections, default_capacity=Defaults.room_capacity):
        self.room_capacity = {room: default_capacity for room in classrooms}
        self.section_strength = {section: default_capacity for section in sections}


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
    def __init__(self, special_subjects: list, labs: list, specialization_subjects: list):
        self.special_subjects = special_subjects
        self.labs = labs
        self.specialization_subjects = specialization_subjects


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10
    PENALTY_NON_DUTY_DAY=40


class SectionsConstants:
    # Define attribute weights and conditions
    ATTRIBUTE_WEIGHTS = {
        'good_cgpa': 1,         # 2^0
        'hostler': 2,           # 2^1
    }

    ATTRIBUTE_CONDITIONS = {
        'hostler': lambda student: student.get('Hostler', False),
    }
