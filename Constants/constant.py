class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class Sections:
    sections = ["A","B","C","D"]

    # def __init__(self, section_number):
    #     self.sections = [chr(65 + i) for i in range(section_number)]


class SubjectTeacherMap:
    subject_teacher_map = {
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
        "Placement_Class": ["AK26"],
    }


class Classrooms:
    classrooms = ["R1", "R2", "R3", "R4", "R5"]
    labs = ["L1", "L2", "L3", "L4", "L5"]


class RoomCapacity:
    room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
    section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}


class SubjectQuota:
    subject_quota = {
        "TCS-531": 3,
        "TCS-502": 3,
        "TCS-503": 3,
        "PCS-506": 1,
        "TMA-502": 3,
        "PMA-502": 1,
        "TCS-509": 4,
        "XCS-501": 2,
        "CSP-501": 1,
        "SCS-501": 1,
        "PCS-503": 1,
        "Placement_Class": 1,
    }
    
class TeacherPreferences:
    teacher_preferences = {
        "AB01": [1],
        "PK02": [1, 2, 3, 4, 5, 6, 7],
        "SS03": [1, 2, 3, 4, 5, 6, 7],
        "AA04": [1, 2, 3, 4, 5, 6, 7],
        "AC05": [1, 2, 3, 4, 5, 6, 7],
        "SP06": [1, 2, 3, 4, 5, 6, 7],
        "DP07": [1, 2, 3, 4, 5, 6, 7],
        "AD08": [1, 2, 3, 4, 5, 6, 7],
        "RD09": [1, 2, 3, 4, 5, 6, 7],
        "BJ10": [1, 2, 3, 4, 5, 6, 7],
        "RS11": [1, 2, 3, 4, 5, 6, 7],
        "JM12": [1, 2, 3, 4, 5, 6, 7],
        "NJ13": [1, 2, 3, 4, 5, 6, 7],
        "PM14": [1, 2, 3, 4, 5, 6, 7],
        "AA15": [1, 2, 3, 4, 5, 6, 7],
        "SJ16": [1, 2, 3, 4, 5, 6, 7],
        "AB17": [1, 2, 3, 4, 5, 6, 7],
        "HP18": [1, 2, 3, 4, 5, 6, 7],
        "SG19": [1, 2, 3, 4, 5, 6, 7],
        "DT20": [1, 2, 3, 4, 5, 6, 7],
        "PA21": [1, 2, 3, 4, 5, 6, 7],
        "NB22": [1, 2, 3, 4, 5, 6, 7],
        "AK23": [1, 2, 3, 4, 5, 6, 7],
        "AP24": [1, 2, 3, 4, 5, 6, 7],
        "VD25": [1, 2, 3, 4, 5, 6, 7],
        "AK26": [5],
    }


class SpecialSubjects:
    special_subjects = ["Placement_Class"]
    Labs=["PCS-506", "PCS-503", "PMA-502"]


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10
