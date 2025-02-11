# FITNESS

#1. def __init__(self, sections):

import unittest

class Sections:
    def __init__(self, num_sections):
        # Generate sections as sectionA, sectionB, sectionC, etc.
        self.sections = [f"section{chr(65 + i)}" for i in range(num_sections)]

    def __iter__(self):
        # Make the class iterable by returning an iterator over the sections list
        return iter(self.sections)

    def __len__(self):
        # Optionally, define the length of the sections
        return len(self.sections)

    def __getitem__(self, index):
        # Optional: Enable indexing for the sections
        return self.sections[index]


# TimetableFitness Class (to manage and calculate timetable fitness)
class TimetableFitness:
    def __init__(self, sections):
        # Ensure `self.sections` is iterable (convert Sections object to a list if needed)
        if isinstance(sections, Sections):
            self.sections = list(sections)  # Convert to list if it is a custom iterable object
        else:
            self.sections = sections  # Assume it is already a list or other iterable

        # Mocking additional data attributes for the sake of this example
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.time_slots = ["9-10 AM", "10-11 AM", "11-12 PM", "1-2 PM", "2-3 PM"]

        # Teacher-subject mapping
        self.subject_teacher_map = {"TCS-531": ["Teacher1", "Teacher2"], "TCS-502": ["Teacher3", "Teacher4"]}

        # Classroom and capacity details
        self.classrooms = ["Room1", "Room2", "Room3"]
        self.room_capacity = {"Room1": 30, "Room2": 25, "Room3": 40}

        # Data structures for tracking schedules
        self.teacher_schedule = {slot: {} for slot in self.time_slots}
        self.room_schedule = {slot: {} for slot in self.time_slots}
        self.assigned_teachers = {section: {} for section in self.sections}
        self.section_rooms = {section: self.classrooms[i % len(self.classrooms)] for i, section in enumerate(self.sections)}

        # Subject-specific constraints
        self.subject_weekly_quota = {
            "TCS-531": 3,
            "TCS-502": 3,
            "Placement_Class": 1
        }

        self.weekly_assignments = {section: {subject: 0 for subject in self.subject_weekly_quota} for section in self.sections}

        # Teacher constraints
        self.teacher_preferences = {teacher_id: [1, 2, 3, 4, 5, 6, 7] for teacher_id in ["Teacher1", "Teacher2", "Teacher3", "Teacher4"]}
        self.teacher_work_load = {teacher: 5 for teacher in self.teacher_preferences}
        self.teacher_assignments = {}


# Unit Test Class
class TestTimetableFitness(unittest.TestCase):
    def setUp(self):
        # Create an instance of Sections with 5 sections
        self.sections = Sections(5)
        self.timetable_fitness = TimetableFitness(self.sections)

    def test_sections_iterable(self):
        # Test that Sections object is iterable
        sections_list = list(self.sections)
        expected_sections = ["sectionA", "sectionB", "sectionC", "sectionD", "sectionE"]
        self.assertEqual(sections_list, expected_sections)

    def test_section_rooms_mapping(self):
        # Test that each section is mapped to a classroom
        section_rooms = self.timetable_fitness.section_rooms
        self.assertEqual(len(section_rooms), len(self.sections))
        self.assertTrue(all(section in section_rooms for section in self.sections))

    def test_assigned_teachers_structure(self):
        # Test that assigned teachers structure is initialized correctly
        assigned_teachers = self.timetable_fitness.assigned_teachers
        self.assertEqual(len(assigned_teachers), len(self.sections))
        self.assertTrue(all(section in assigned_teachers for section in self.sections))


if __name__ == "__main__":
    unittest.main()

#2. def generate_day_schedule(self, day, half_day_sections, week_number):

import random
from collections import defaultdict

class TimetableGenerator:
    def __init__(self, sections, time_slots, subject_teacher_map, section_rooms, lab):
        self.sections = sections
        self.time_slots = time_slots
        self.subject_teacher_map = subject_teacher_map
        self.section_rooms = section_rooms
        self.lab = lab
        self.weekly_assignments = defaultdict(lambda: defaultdict(int))
        self.teacher_schedule = defaultdict(dict)
        self.room_schedule = defaultdict(dict)
        self.teacher_assignments = defaultdict(dict)

    def generate_day_schedule(self, day, half_day_sections, week_number):
        day_schedule = {}
        subject_teacher_usage = {subject: iter(teachers) for subject, teachers in self.subject_teacher_map.items()}

        for section in self.sections:
            section_schedule = []
            subjects_used_today = set()
            current_room = self.section_rooms[section]
            num_slots = 4 if section in half_day_sections else 7

            index = 1
            while index <= num_slots:
                time_slot = self.time_slots[index]

                # Skip if time_slot is already used
                if any(item['time_slot'] == time_slot for item in section_schedule):
                    index += 1
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

                    if "Lab" in subject:
                        if index + 1 > num_slots:  # Ensure space for double slot
                            available_subjects.remove(subject)
                            continue
                        is_lab = True  # Mark this as a lab

                    if subject not in subjects_used_today:
                        teacher_iter = subject_teacher_usage[subject]
                        try:
                            teacher = next(teacher_iter)
                        except StopIteration:
                            teacher_iter = iter(self.subject_teacher_map[subject])
                            teacher = next(teacher_iter)
                            subject_teacher_usage[subject] = teacher_iter
                        break

                    available_subjects.remove(subject)

                if subject is None or teacher is None:
                    subject, teacher = "Library", "None"

                if subject != "Library":
                    self.weekly_assignments[section][subject] += 1

                subjects_used_today.add(subject)

                # Assign rooms based on whether it's a lab
                assigned_room = random.choice(self.lab) if is_lab else current_room
                self.teacher_schedule[time_slot][teacher] = section
                self.room_schedule[time_slot][assigned_room] = section

                # Handle double slot allocation for labs
                if is_lab:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append({
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": assigned_room,
                            "time_slot": next_time_slot
                        })
                        self.room_schedule[next_time_slot][assigned_room] = section
                        self.teacher_schedule[next_time_slot][teacher] = section
                        index += 1  # Skip the next slot for lab

                section_schedule.append({
                    "teacher_id": teacher,
                    "subject_id": subject,
                    "classroom_id": assigned_room,
                    "time_slot": time_slot
                })

                index += 1

            day_schedule[section] = section_schedule
        return day_schedule
import unittest

class TestGenerateDaySchedule(unittest.TestCase):
    def setUp(self):
        self.sections = ["A", "B", "C"]
        self.time_slots = {
            1: "9:00-10:00",
            2: "10:00-11:00",
            3: "11:00-12:00",
            4: "12:00-1:00",
            5: "2:00-3:00",
            6: "3:00-4:00",
            7: "4:00-5:00"
        }
        self.subject_teacher_map = {
            "Math": ["T1", "T2"],
            "Physics": ["T3"],
            "Chemistry Lab": ["T4"],
            "Placement_Class": ["T5"],
        }
        self.section_rooms = {"A": "R1", "B": "R2", "C": "R3"}
        self.lab = ["Lab1", "Lab2"]
        self.tt = TimetableGenerator(
            self.sections, self.time_slots, self.subject_teacher_map, self.section_rooms, self.lab
        )

    def test_schedule_structure(self):
        schedule = self.tt.generate_day_schedule("Monday", ["A"], 1)
        self.assertIsInstance(schedule, dict)
        for section, section_schedule in schedule.items():
            self.assertIsInstance(section_schedule, list)
            for entry in section_schedule:
                self.assertIn("teacher_id", entry)
                self.assertIn("subject_id", entry)
                self.assertIn("classroom_id", entry)
                self.assertIn("time_slot", entry)

    def test_half_day_slots(self):
        schedule = self.tt.generate_day_schedule("Monday", ["A"], 1)
        for section, section_schedule in schedule.items():
            if section == "A":
                self.assertEqual(len(section_schedule), 4)
            else:
                self.assertEqual(len(section_schedule), 7)

    def test_no_repeated_time_slots(self):
        schedule = self.tt.generate_day_schedule("Monday", ["A"], 1)
        for section, section_schedule in schedule.items():
            time_slots = [entry["time_slot"] for entry in section_schedule]
            self.assertEqual(len(time_slots), len(set(time_slots)))

    def test_lab_double_slots(self):
        schedule = self.tt.generate_day_schedule("Monday", ["A"], 1)
        for section, section_schedule in schedule.items():
            for i, entry in enumerate(section_schedule):
                if "Lab" in entry['subject_id']:
                    current_slot = entry['time_slot']
                    current_index = list(self.tt.time_slots.values()).index(current_slot)

                    # Check if the lab occupies the next time slot
                    if current_index + 1 < len(self.tt.time_slots):
                        next_slot = section_schedule[i + 1]['time_slot']
                        expected_next_slot = self.tt.time_slots[current_index + 1]
                        self.assertEqual(
                            next_slot, 
                            expected_next_slot,
                            f"Lab for section {section} did not occupy consecutive slots as expected."
                        )

    def test_teacher_and_room_assignments(self):
        schedule = self.tt.generate_day_schedule("Monday", ["A"], 1)
        for section, section_schedule in schedule.items():
            for entry in section_schedule:
                teacher = entry['teacher_id']
                room = entry['classroom_id']
                time_slot = entry['time_slot']
                self.assertIn(teacher, self.tt.teacher_schedule[time_slot])
                self.assertIn(room, self.tt.room_schedule[time_slot])


if __name__ == "__main__":
    unittest.main()

#3. def create_timetable(self, num_weeks=1):

import unittest
from collections import defaultdict
import random

class TimetableGenerator:
    def __init__(self, sections, time_slots, subject_teacher_map, section_rooms, lab):
        self.sections = sections
        self.time_slots = time_slots
        self.subject_teacher_map = subject_teacher_map
        self.section_rooms = section_rooms
        self.lab = lab
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Ensure days are initialized
        self.weekly_assignments = defaultdict(lambda: defaultdict(int))
        self.teacher_schedule = defaultdict(dict)
        self.room_schedule = defaultdict(dict)
        self.teacher_assignments = defaultdict(dict)

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

                # Skip if time_slot is already used
                if any(item["time_slot"] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None
                is_lab = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    # Handle special rules for Placement_Class and labs
                    if subject == "Placement_Class" and index <= 4:  # Placement classes are after lunch
                        available_subjects.remove(subject)
                        continue

                    if "Lab" in subject:
                        if index + 1 > num_slots:  # Ensure space for double slot
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

                self.teacher_schedule[time_slot][teacher] = section
                self.room_schedule[time_slot][assigned_room] = section

                # Handle double slot allocation for labs
                if is_lab:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]

                        # Assign consecutive slot to the lab
                        section_schedule.append(
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": assigned_room,
                                "time_slot": next_time_slot,
                            }
                        )
                        self.room_schedule[next_time_slot][assigned_room] = section
                        self.teacher_schedule[next_time_slot][teacher] = section
                        index += 1  # Skip the next slot for lab

                section_schedule.append(
                    {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_room,
                        "time_slot": time_slot,
                    }
                )

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


class TestTimetableGenerator(unittest.TestCase):
    def setUp(self):
        self.sections = ["A", "B", "C"]
        self.time_slots = {
            1: "9:00-10:00",
            2: "10:00-11:00",
            3: "11:00-12:00",
            4: "12:00-1:00",
            5: "2:00-3:00",
            6: "3:00-4:00",
            7: "4:00-5:00"
        }
        self.subject_teacher_map = {
            "Math": ["T1", "T2"],
            "Physics": ["T3"],
            "Chemistry Lab": ["T4"],
            "Placement_Class": ["T5"],
        }
        self.section_rooms = {"A": "R1", "B": "R2", "C": "R3"}
        self.lab = ["Lab1", "Lab2"]
        self.tt = TimetableGenerator(
            self.sections, self.time_slots, self.subject_teacher_map, self.section_rooms, self.lab
        )

    def test_create_timetable(self):
        timetable = self.tt.create_timetable(num_weeks=2)
        self.assertIsInstance(timetable, dict)
        self.assertGreater(len(timetable), 0)
        self.assertIn("Week 1", timetable)
        self.assertIn("Week 2", timetable)
        
        # Verify timetable structure
        for week, week_schedule in timetable.items():
            self.assertIsInstance(week_schedule, dict)
            for day, day_schedule in week_schedule.items():
                self.assertIsInstance(day_schedule, dict)
                for section, section_schedule in day_schedule.items():
                    self.assertIsInstance(section_schedule, list)
                    for entry in section_schedule:
                        self.assertIn("teacher_id", entry)
                        self.assertIn("subject_id", entry)
                        self.assertIn("classroom_id", entry)
                        self.assertIn("time_slot", entry)

if __name__ == "__main__":
    unittest.main()

#4.  def calculate_fitness(self, chromosome):

import unittest
from collections import defaultdict
import random

class TimetableGenerator:
    def __init__(self, sections, time_slots, subject_teacher_map, section_rooms, lab, section_strength, room_capacity, teacher_preferences, teacher_work_load):
        self.sections = sections
        self.time_slots = time_slots
        self.subject_teacher_map = subject_teacher_map
        self.section_rooms = section_rooms
        self.lab = lab
        self.section_strength = section_strength
        self.room_capacity = room_capacity
        self.teacher_preferences = teacher_preferences
        self.teacher_work_load = teacher_work_load
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.weekly_assignments = defaultdict(lambda: defaultdict(int))
        self.teacher_schedule = defaultdict(dict)
        self.room_schedule = defaultdict(dict)
        self.teacher_assignments = defaultdict(dict)

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

                if any(item["time_slot"] == time_slot for item in section_schedule):
                    continue

                available_subjects = list(self.subject_teacher_map.keys())
                subject, teacher = None, None
                is_lab = False

                while available_subjects:
                    subject = random.choice(available_subjects)

                    if subject == "Placement_Class" and index <= 4:
                        available_subjects.remove(subject)
                        continue

                    if "Lab" in subject:
                        if index + 1 > num_slots:
                            available_subjects.remove(subject)
                            continue
                        is_lab = True

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

                if is_lab:
                    assigned_room = random.choice(self.lab)
                else:
                    assigned_room = current_room

                self.teacher_schedule[time_slot][teacher] = section
                self.room_schedule[time_slot][assigned_room] = section

                if is_lab:
                    next_slot_index = index + 1
                    if next_slot_index <= num_slots:
                        next_time_slot = self.time_slots[next_slot_index]
                        section_schedule.append(
                            {
                                "teacher_id": teacher,
                                "subject_id": subject,
                                "classroom_id": assigned_room,
                                "time_slot": next_time_slot,
                            }
                        )
                        self.room_schedule[next_time_slot][assigned_room] = section
                        self.teacher_schedule[next_time_slot][teacher] = section
                        index += 1

                section_schedule.append(
                    {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": assigned_room,
                        "time_slot": time_slot,
                    }
                )

            day_schedule[section] = section_schedule
        return day_schedule

    def calculate_fitness(self, chromosome):
        week_fitness_scores = []

        for week_num, (week, week_schedule) in enumerate(chromosome.items(), start=1):
            overall_fitness_score = 0
            section_fitness_scores = {}

            for day, day_schedule in week_schedule.items():
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

                    section_fitness_scores[day][section] = section_score
                    overall_fitness_score += section_score

            week_fitness_scores.append({
                "week": f"Week {week_num}",
                "score": overall_fitness_score
            })

        return week_fitness_scores, section_fitness_scores


class TestTimetableGenerator(unittest.TestCase):
    def setUp(self):
        self.sections = ["A", "B", "C"]
        self.time_slots = {
            1: "9:00-10:00",
            2: "10:00-11:00",
            3: "11:00-12:00",
            4: "12:00-1:00",
            5: "2:00-3:00",
            6: "3:00-4:00",
            7: "4:00-5:00"
        }
        self.subject_teacher_map = {
            "Math": ["T1", "T2"],
            "Physics": ["T3"],
            "Chemistry Lab": ["T4"],
            "Placement_Class": ["T5"],
        }
        self.section_rooms = {"A": "R1", "B": "R2", "C": "R3"}
        self.lab = ["Lab1", "Lab2"]
        self.section_strength = {"A": 40, "B": 35, "C": 50}
        self.room_capacity = {"R1": 40, "R2": 35, "R3": 50}
        self.teacher_preferences = {"T1": ["9:00-10:00", "3:00-4:00"], "T2": ["10:00-11:00"]}
        self.teacher_work_load = {"T1": 10, "T2": 15, "T3": 8, "T4": 12, "T5": 6}

        self.tt = TimetableGenerator(
            self.sections, self.time_slots, self.subject_teacher_map, self.section_rooms,
            self.lab, self.section_strength, self.room_capacity, self.teacher_preferences, self.teacher_work_load
        )

    def test_calculate_fitness(self):
        # Create a mock chromosome with timetable data
        chromosome = {
            "Week 1": {
                "Monday": {
                    "A": [{"teacher_id": "T1", "subject_id": "Math", "classroom_id": "R1", "time_slot": "9:00-10:00"}],
                    "B": [{"teacher_id": "T3", "subject_id": "Physics", "classroom_id": "R2", "time_slot": "10:00-11:00"}],
                },
                "Tuesday": {
                    "C": [{"teacher_id": "T4", "subject_id": "Chemistry Lab", "classroom_id": "Lab1", "time_slot": "11:00-12:00"}],
                }
            }
        }

        week_fitness_scores, section_fitness_scores = self.tt.calculate_fitness(chromosome)

        # Test the overall fitness score for Week 1
        self.assertIsInstance(week_fitness_scores, list)
        self.assertGreater(len(week_fitness_scores), 0)
        self.assertEqual(week_fitness_scores[0]["week"], "Week 1")
        self.assertIn("score", week_fitness_scores[0])

        # Test the section fitness score for a specific day and section
        self.assertIn("Monday", section_fitness_scores)
        self.assertIn("A", section_fitness_scores["Monday"])
        self.assertIsInstance(section_fitness_scores["Monday"]["A"], int)

if __name__ == "__main__":
    unittest.main()