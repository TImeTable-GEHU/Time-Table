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
        "TCS-511":["PK02"],
        "TCS-592":["AB01"],
        "TCS-512":["HP18"],
        "TCS-519":["DP07"],
        "PCS-512":["VD25"]
        
    }
class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class Sections:
    sections = []

    def __init__(self, section_number):
        self.sections = [chr(65 + i) for i in range(section_number)]


class Classrooms:
    classrooms = ["R1", "R2", "R3", "R4", "R5"]
    labs = ["L1", "L2", "L3", "L4", "L5"]


class RoomCapacity:
    room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
    section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}


class SubjectWeeklyQuota:
    subject_quota = {
        "TCS-531": 3,
        "TCS-502": 3,
        "TCS-503": 3,
        "PCS-506": 1,
        "TMA-502": 3,
        "PMA-502": 1,
        "TCS-509": 3,
        "XCS-501": 2,
        "CSP-501": 1,
        "SCS-501": 1,
        "PCS-503": 1,
        "Placement_Class": 1,
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


class TeacherWorkload:
    Weekly_workLoad = {
        "AB01": 5,
        "PK02": 5,
        "SS03": 5,
        "AA04": 5,
        "AC05": 5,
        "SP06": 5,
        "DP07": 5,
        "AD08": 5,
        "RD09": 5,
        "BJ10": 5,
        "RS11": 5,
        "JM12": 5,
        "NJ13": 5,
        "PM14": 5,
        "AA15": 5,
        "SJ16": 5,
        "AB17": 5,
        "HP18": 5,
        "SG19": 5,
        "DT20": 5,
        "PA21": 5,
        "NB22": 5,
        "AK23": 5,
        "AP24": 5,
        "VD25": 5,
        "AK26": 5
    }

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
    teacher_duty_days = {
        "AB01": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "PK02": ["Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "SS03": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AA04": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AC05": ["Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "SP06": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "DP07": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AD08": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "RD09": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "BJ10": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "RS11": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "JM12": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "NJ13": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "PM14": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AA15": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "SJ16": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AB17": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "HP18": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "SG19": ["Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "DT20": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "PA21": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "NB22": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "AK23": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AP24": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "VD25": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
        "AK26": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],
    }
class SampleChromosome:
    schedule1={
            "Monday": {
                "A": [
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R1",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L4",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L4",
                        "time_slot": "11:10 - 12:05"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "HP18",
                        "subject_id": "TCS-509",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-503",
                        "classroom_id": "R4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R4",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "SG19",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R4",
                        "time_slot": "3:30 - 4:25"
                    }
                ]
            },
            "Tuesday": {
                "A": [
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "11:10 - 12:05"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R2",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "NB22",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "HP18",
                        "subject_id": "TCS-509",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "SG19",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Wednesday": {
                "A": [
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L5",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L5",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "L2",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "L2",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "RD09",
                        "subject_id": "PCS-506",
                        "classroom_id": "L1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RD09",
                        "subject_id": "PCS-506",
                        "classroom_id": "L1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-503",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "JM12",
                        "subject_id": "TMA-502",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Thursday": {
                "A": [
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L1",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "L5",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "L5",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "JM12",
                        "subject_id": "TMA-502",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Friday": {
                "A": [
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R2",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-502",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L5",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L5",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "HP18",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            }
        }
    schedule2={
            "Monday": {
                "A": [
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R1",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R2",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R2",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R2",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "RD09",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RD09",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "11:10 - 12:05"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "NB22",
                        "subject_id": "XCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Tuesday": {
                "A": [
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AK26",
                        "subject_id": "Placement_Class",
                        "classroom_id": "R1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "NB22",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R3",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R3",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-502",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Wednesday": {
                "A": [
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "11:10 - 12:05"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "PCS-503",
                        "classroom_id": "L1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "SP06",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "PCS-503",
                        "classroom_id": "L4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "NB22",
                        "subject_id": "XCS-501",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R4",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R4",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "HP18",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "3:30 - 4:25"
                    }
                ]
            },
            "Thursday": {
                "A": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R1",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R2",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "JM12",
                        "subject_id": "TMA-502",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R3",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "NJ13",
                        "subject_id": "TMA-502",
                        "classroom_id": "R4",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AP24",
                        "subject_id": "SCS-501",
                        "classroom_id": "R4",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "PA21",
                        "subject_id": "XCS-501",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            },
            "Friday": {
                "A": [
                    {
                        "teacher_id": "SJ16",
                        "subject_id": "TCS-509",
                        "classroom_id": "R1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R1",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "SP06",
                        "subject_id": "TCS-503",
                        "classroom_id": "R1",
                        "time_slot": "12:05 - 1:00"
                    }
                ],
                "B": [
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L1",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "RS11",
                        "subject_id": "PCS-503",
                        "classroom_id": "L1",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "BJ10",
                        "subject_id": "TMA-502",
                        "classroom_id": "R2",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "PK02",
                        "subject_id": "TCS-531",
                        "classroom_id": "R2",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "DP07",
                        "subject_id": "TCS-503",
                        "classroom_id": "R2",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R2",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "SS03",
                        "subject_id": "TCS-502",
                        "classroom_id": "R2",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "C": [
                    {
                        "teacher_id": "AC05",
                        "subject_id": "TCS-503",
                        "classroom_id": "R3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "AK23",
                        "subject_id": "CSP-501",
                        "classroom_id": "R3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "AB17",
                        "subject_id": "TCS-509",
                        "classroom_id": "R3",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AB01",
                        "subject_id": "TCS-531",
                        "classroom_id": "R3",
                        "time_slot": "12:05 - 1:00"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "2:15 - 3:10"
                    },
                    {
                        "teacher_id": "AD08",
                        "subject_id": "PCS-506",
                        "classroom_id": "L5",
                        "time_slot": "1:20 - 2:15"
                    },
                    {
                        "teacher_id": "DT20",
                        "subject_id": "XCS-501",
                        "classroom_id": "R3",
                        "time_slot": "3:30 - 4:25"
                    }
                ],
                "D": [
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L3",
                        "time_slot": "9:55 - 10:50"
                    },
                    {
                        "teacher_id": "PM14",
                        "subject_id": "PMA-502",
                        "classroom_id": "L3",
                        "time_slot": "9:00 - 9:55"
                    },
                    {
                        "teacher_id": "HP18",
                        "subject_id": "TCS-509",
                        "classroom_id": "R4",
                        "time_slot": "11:10 - 12:05"
                    },
                    {
                        "teacher_id": "AA04",
                        "subject_id": "TCS-502",
                        "classroom_id": "R4",
                        "time_slot": "12:05 - 1:00"
                    }
                ]
            }
        
    
    }
