class SubjectTeacherMap:
    subject_teacher_map = {
        "TBC-301": ["DS01", "PK02"],
        "TBC-302": ["BR03", "SKB04"],
        "TBC-303": ["JC06", "DP07"],
        "TBC-304": ["JP08", "SD09"],
        "TBC-305": ["MJ10", "RS11", "SD09"],
        "XBC-301": ["DT14", "NB08"],
        "PBC-301": ["BR03", "SD17"],
        "WAD-303": ["VD12", "AA13"],
        "PBC-302": ["DT14", "SD09", "JP08", "VJ05"],
    }


class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class Sections:
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
        "TBC-301": 3,
        "TBC-302": 3,
        "TBC-303": 3,
        "TBC-304": 3,
        "TBC-305": 3,
        "XBC-301": 2,
        "PBC-301": 1,
        "WAD-303": 1,
        "PBC-302": 1,
    }


class SpecialSubjects:
    special_subjects = ["Placement_Class"]
    Labs = ["PBC-301", "WAD-303", "PBC-302"]


class PenaltyConstants:
    PENALTY_TEACHER_DOUBLE_BOOKED = 30
    PENALTY_CLASSROOM_DOUBLE_BOOKED = 20
    PENALTY_OVER_CAPACITY = 25
    PENALTY_UN_PREFERRED_SLOT = 5
    PENALTY_OVERLOAD_TEACHER = 10


class TeacherWorkload:
    Weekly_workLoad = {
        "DS01": 5,
        "PK02": 5,
        "BR03": 5,
        "SKB04": 5,
        "JC06": 5,
        "DP07": 5,
        "JP08": 5,
        "SD09": 5,
        "MJ10": 5,
        "RS11": 5,
        "DT14": 5,
        "NB08": 5,
        "BR16": 5,
        "SD17": 5,
        "VD12": 5,
        "AA13": 5,
        "VJ05": 5,
    }

    teacher_preferences = {
        "DS01": [1, 2, 3, 4, 5, 6, 7],
        "PK02": [1, 2, 3, 4, 5, 6, 7],
        "BR03": [1, 2, 3, 4, 5, 6, 7],
        "SKB04": [1, 2, 3, 4, 5, 6, 7],
        "JC06": [1, 2, 3, 4, 5, 6, 7],
        "DP07": [1, 2, 3, 4, 5, 6, 7],
        "JP08": [1, 2, 3, 4, 5, 6, 7],
        "SD09": [1, 2, 3, 4, 5, 6, 7],
        "MJ10": [1, 2, 3, 4, 5, 6, 7],
        "RS11": [1, 2, 3, 4, 5, 6, 7],
        "DT14": [1, 2, 3, 4, 5, 6, 7],
        "NB08": [1, 2, 3, 4, 5, 6, 7],
        "BR16": [1, 2, 3, 4, 5, 6, 7],
        "SD17": [1, 2, 3, 4, 5, 6, 7],
        "VD12": [1, 2, 3, 4, 5, 6, 7],
        "AA13": [1, 2, 3, 4, 5, 6, 7],
        "VJ05": [1, 2, 3, 4, 5, 6, 7],
    }

    teacher_duty_days = {
        "DS01": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "PK02": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "BR03": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "SKB04": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "JC06": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "DP07": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "JP08": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "SD09": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "MJ10": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "RS11": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "DT14": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "NB08": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "BR16": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "SD17": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "VD12": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "AA13": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "VJ05": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
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
