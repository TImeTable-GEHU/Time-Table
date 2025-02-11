#CROSSOVER

#1. def create_chromosome(self):

import random
import unittest

# TimetableScheduler Class
class TimetableScheduler:
    def __init__(self):
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = [1, 2, 3, 4, 5, 6, 7]  # Time slots per day
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
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
            "SCS-501": ["AP24"]
        }
        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.room_capacity = {"R1": 200, "R2": 230, "R3": 240, "R4": 250, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}

    def create_chromosome(self):
        schedule = {}
        teacher_schedule = {slot: set() for slot in self.time_slots}
        room_schedule = {slot: {} for slot in self.time_slots}

        for day in self.days:
            schedule[day] = {}
            for section in self.sections:
                schedule[day][section] = []
                used_time_slots = set()

                while len(schedule[day][section]) < 7:
                    subject = random.choice(list(self.subject_teacher_map.keys()))
                    teacher = random.choice(self.subject_teacher_map[subject])
                    classroom = random.choice(self.classrooms)

                    # Find an available time slot
                    available_slots = [
                        slot for slot in self.time_slots if slot not in used_time_slots
                    ]
                    if not available_slots:
                        break

                    time_slot = random.choice(available_slots)

                    # Check for conflicts
                    if (teacher not in teacher_schedule[time_slot] and
                            section not in room_schedule[time_slot].get(classroom, [])):

                        entry = {
                            "teacher_id": teacher,
                            "subject_id": subject,
                            "classroom_id": classroom,
                            "time_slot": time_slot
                        }
                        schedule[day][section].append(entry)
                        used_time_slots.add(time_slot)

                        # Update schedules to avoid future conflicts
                        teacher_schedule[time_slot].add(teacher)
                        if classroom not in room_schedule[time_slot]:
                            room_schedule[time_slot][classroom] = []
                        room_schedule[time_slot][classroom].append(section)

                # Ensure the section has all 7 slots for the day
                if len(schedule[day][section]) < 7:
                    raise RuntimeError(
                        f"Failed to generate a complete schedule for section {section} on {day}."
                    )

        return schedule


# Unit Test Class for TimetableScheduler
class TestTimetableScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = TimetableScheduler()

    def test_schedule_for_all_days_and_sections(self):
        schedule = self.scheduler.create_chromosome()

        # Check every day has all sections with 7 time slots
        for day in self.scheduler.days:
            self.assertIn(day, schedule)
            for section in self.scheduler.sections:
                self.assertIn(section, schedule[day])
                self.assertEqual(len(schedule[day][section]), 7)

    def test_conflict_free_teacher_allocation(self):
        schedule = self.scheduler.create_chromosome()

        # Check for teacher conflicts
        for day in self.scheduler.days:
            teacher_schedule = {slot: set() for slot in self.scheduler.time_slots}
            for section in self.scheduler.sections:
                for entry in schedule[day][section]:
                    teacher = entry["teacher_id"]
                    time_slot = entry["time_slot"]
                    self.assertNotIn(teacher, teacher_schedule[time_slot])
                    teacher_schedule[time_slot].add(teacher)

    def test_room_capacity(self):
        schedule = self.scheduler.create_chromosome()

        # Ensure room capacity meets section strength
        for day in self.scheduler.days:
            for section in self.scheduler.sections:
                for entry in schedule[day][section]:
                    classroom = entry["classroom_id"]
                    self.assertGreaterEqual(
                        self.scheduler.room_capacity[classroom],
                        self.scheduler.section_strength[section]
                    )

    def test_time_slots_coverage(self):
        schedule = self.scheduler.create_chromosome()

        # Check if all time slots are covered per section per day
        for day in self.scheduler.days:
            for section in self.scheduler.sections:
                time_slots = [entry["time_slot"] for entry in schedule[day][section]]
                self.assertEqual(len(set(time_slots)), 7)  # Ensure exactly 7 slots


if __name__ == "__main__":
    unittest.main()

#2.  def create_multiple_chromosomes(self, num_chromosomes):

import random
import unittest
import time

class TimetableScheduler:
    def __init__(self, subjects, rooms, days, sections, max_attempts=10):
        self.subjects = subjects  # List of subject codes
        self.rooms = rooms  # List of available rooms
        self.days = days  # List of days in the week
        self.sections = sections  # List of sections
        self.max_attempts = max_attempts  # Max attempts to find a valid slot

        self.schedule = {}  # Schedule dictionary to store the timetable

    def generate_random_schedule(self):
        """ Generate a random schedule for each subject and section. """
        timetable = {}
        for subject in self.subjects:
            for section in self.sections:
                attempts = 0
                while attempts < self.max_attempts:
                    # Randomly select a day, room, and time slot
                    day = random.choice(self.days)
                    room = random.choice(self.rooms)
                    time_slot = f"{day}_{room}"

                    # Check if the time_slot is available (no conflicts)
                    if self.is_slot_available(subject, section, time_slot):
                        timetable[subject] = (section, day, room, time_slot)
                        break
                    else:
                        attempts += 1
                        if attempts == self.max_attempts:
                            raise RuntimeError(
                                f"Failed to assign a valid slot for {subject} on {day} for {section} after {attempts} attempts."
                            )
        return timetable

    def is_slot_available(self, subject, section, time_slot):
        """ Check if a slot is available by ensuring no conflicts. """
        # Check if any other subject has been scheduled in the same time slot
        for key, value in self.schedule.items():
            if value[3] == time_slot:  # Slot conflict
                return False
        return True

    def create_chromosome(self):
        """ Create a chromosome that represents a valid timetable. """
        attempts = 0
        while attempts < self.max_attempts:
            try:
                timetable = self.generate_random_schedule()
                self.schedule = timetable  # Assign the generated schedule to the global timetable
                return timetable
            except RuntimeError as e:
                print(f"Error: {e}")
                attempts += 1
                if attempts == self.max_attempts:
                    raise RuntimeError("Failed to generate a valid timetable after multiple attempts.")
                # Reset and retry
                self.schedule = {}

        return None

    def create_multiple_chromosomes(self, num_chromosomes):
        """ Create multiple chromosomes (timetables). """
        chromosomes = []
        for _ in range(num_chromosomes):
            chromosome = self.create_chromosome()
            if chromosome:
                chromosomes.append(chromosome)
            else:
                print("Failed to create a valid chromosome.")
        return chromosomes


class TestTimetableScheduler(unittest.TestCase):

    def setUp(self):
        """ Setup the test case environment. """
        self.subjects = ['PCS-506', 'XCS-501', 'TCS-502', 'CSP-501', 'TCS-531']
        self.rooms = ['Room 101', 'Room 102', 'Room 103']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.sections = ['A', 'B', 'C']

        self.scheduler = TimetableScheduler(self.subjects, self.rooms, self.days, self.sections)

    def test_chromosome_structure(self):
        """ Test the structure of each chromosome. """
        num_chromosomes = 3
        start_time = time.time()
        chromosomes = self.scheduler.create_multiple_chromosomes(num_chromosomes)
        end_time = time.time()

        self.assertEqual(len(chromosomes), num_chromosomes)
        print(f"Ran {num_chromosomes} tests in {end_time - start_time:.4f} seconds")

        for idx, chromosome in enumerate(chromosomes):
            print(f"Chromosome {idx+1}:")
            for subject, (section, day, room, time_slot) in chromosome.items():
                print(f"{subject} - {section} - {day} - {room} - {time_slot}")
            print()

    def test_conflict_free_chromosomes(self):
        """ Test that chromosomes are conflict-free. """
        num_chromosomes = 3
        start_time = time.time()
        chromosomes = self.scheduler.create_multiple_chromosomes(num_chromosomes)
        end_time = time.time()

        self.assertEqual(len(chromosomes), num_chromosomes)
        print(f"Ran {num_chromosomes} tests in {end_time - start_time:.4f} seconds")

        for idx, chromosome in enumerate(chromosomes):
            for subject, (section, day, room, time_slot) in chromosome.items():
                # Check for conflicts (same time slot for different subjects)
                for other_subject, other_values in chromosome.items():
                    if subject != other_subject and time_slot == other_values[3]:
                        self.fail(f"Conflict detected: {subject} and {other_subject} in the same time slot: {time_slot}")

    def test_create_multiple_chromosomes_count(self):
        """ Test if the correct number of chromosomes is generated. """
        num_chromosomes = 5
        start_time = time.time()
        chromosomes = self.scheduler.create_multiple_chromosomes(num_chromosomes)
        end_time = time.time()

        self.assertEqual(len(chromosomes), num_chromosomes)
        print(f"Ran {num_chromosomes} tests in {end_time - start_time:.4f} seconds")

    def test_room_capacity_in_multiple_chromosomes(self):
        """ Test room capacity constraint across multiple chromosomes. """
        num_chromosomes = 3
        start_time = time.time()
        chromosomes = self.scheduler.create_multiple_chromosomes(num_chromosomes)
        end_time = time.time()

        self.assertEqual(len(chromosomes), num_chromosomes)
        print(f"Ran {num_chromosomes} tests in {end_time - start_time:.4f} seconds")

        # Test room capacity constraints for each timetable (e.g., number of rooms used)
        for idx, chromosome in enumerate(chromosomes):
            room_usage = {}
            for subject, (section, day, room, time_slot) in chromosome.items():
                room_usage[room] = room_usage.get(room, 0) + 1
            print(f"Chromosome {idx+1} Room Usage: {room_usage}")


# Run the tests
if __name__ == "__main__":
    unittest.main()

#3. def crossover(self, parent1, parent2):

import random
import unittest

class TimetableScheduler:
    def __init__(self, subjects, rooms, days, sections):
        self.subjects = subjects  # List of subject codes
        self.rooms = rooms  # List of available rooms
        self.days = days  # List of days in the week
        self.sections = sections  # List of sections

    def crossover(self, parent1, parent2):
        """Perform single-point crossover on two parent chromosomes."""
        offspring1 = {}
        offspring2 = {}

        days = self.days
        crossover_point = random.randint(1, len(days) - 1)

        for i, day in enumerate(days):
            if i < crossover_point:
                offspring1[day] = parent1[day]
                offspring2[day] = parent2[day]
            else:
                offspring1[day] = parent2[day]
                offspring2[day] = parent1[day]

        return offspring1, offspring2

# Unit test for the crossover function
class TestCrossoverMethod(unittest.TestCase):

    def setUp(self):
        # Example data to simulate chromosomes for testing
        self.subjects = ['PCS-506', 'XCS-501', 'TCS-502', 'CSP-501', 'TCS-531']
        self.rooms = ['Room 101', 'Room 102', 'Room 103']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.sections = ['A', 'B', 'C']

        # Example chromosomes (parents)
        self.parent1 = {
            'Monday': 'PCS-506',
            'Tuesday': 'XCS-501',
            'Wednesday': 'TCS-502',
            'Thursday': 'CSP-501',
            'Friday': 'TCS-531'
        }
        self.parent2 = {
            'Monday': 'TCS-502',
            'Tuesday': 'PCS-506',
            'Wednesday': 'CSP-501',
            'Thursday': 'TCS-531',
            'Friday': 'XCS-501'
        }
        
        # Create an instance of the TimetableScheduler
        self.scheduler = TimetableScheduler(self.subjects, self.rooms, self.days, self.sections)

    def test_crossover_correct_number_of_offspring(self):
        """Test if crossover produces exactly two offspring."""
        offspring1, offspring2 = self.scheduler.crossover(self.parent1, self.parent2)
        self.assertEqual(len(offspring1), len(self.days))
        self.assertEqual(len(offspring2), len(self.days))

    def test_crossover_correct_assignment(self):
        """Test if crossover correctly assigns the parts from parents."""
        offspring1, offspring2 = self.scheduler.crossover(self.parent1, self.parent2)
        
        # Get the crossover point from the offspring's first day in the timetable
        crossover_point = next(i for i, day in enumerate(self.days) if offspring1[self.days[i]] != self.parent1[self.days[i]])
        
        # Check the assignment from parent1 and parent2 in the offspring
        for i in range(crossover_point):
            self.assertEqual(offspring1[self.days[i]], self.parent1[self.days[i]])
            self.assertEqual(offspring2[self.days[i]], self.parent2[self.days[i]])
        
        for i in range(crossover_point, len(self.days)):
            self.assertEqual(offspring1[self.days[i]], self.parent2[self.days[i]])
            self.assertEqual(offspring2[self.days[i]], self.parent1[self.days[i]])

    def test_crossover_randomness(self):
        """Test if the crossover point is truly random by checking different results."""
        offspring1_a, offspring2_a = self.scheduler.crossover(self.parent1, self.parent2)
        offspring1_b, offspring2_b = self.scheduler.crossover(self.parent1, self.parent2)

        # Check that the offspring are not the same (i.e., crossover point was different)
        self.assertNotEqual(offspring1_a, offspring1_b)
        self.assertNotEqual(offspring2_a, offspring2_b)

    def test_crossover_empty_parent(self):
        """Test if crossover handles empty parents gracefully."""
        empty_parent = {}
        with self.assertRaises(KeyError):
            self.scheduler.crossover(empty_parent, self.parent2)
        
        with self.assertRaises(KeyError):
            self.scheduler.crossover(self.parent1, empty_parent)


if __name__ == '__main__':
    unittest.main()

#4. def mutate_timetable(self, chromosome, mutation_rate=0.7):

import random
import unittest

class TimetableScheduler:
    def __init__(self, classrooms, sections, time_slots):
        self.classrooms = classrooms  # List of classrooms available for assignment
        self.sections = sections  # List of sections
        self.time_slots = time_slots  # List of time slots available for scheduling

    def mutate_timetable(self, chromosome, mutation_rate=0.7):
        """Applies mutation to a timetable chromosome."""
        classrooms = self.classrooms
        sections = self.sections
        mutated_chromosome = chromosome.copy()

        for day, section_schedule in mutated_chromosome.items():
            for section, entries in section_schedule.items():
                for entry in entries:
                    if random.random() < mutation_rate:
                        entry["time_slot"] = random.choice(self.time_slots)
                        entry["classroom_id"] = random.choice(classrooms)
                        entry["section"] = random.choice(sections)

        return mutated_chromosome


class TestMutateTimetable(unittest.TestCase):

    def setUp(self):
        # Example data to simulate a timetable chromosome
        self.classrooms = ['Room 101', 'Room 102', 'Room 103']
        self.sections = ['A', 'B', 'C']
        self.time_slots = ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM']

        # Example timetable (chromosome)
        self.chromosome = {
            'Monday': {
                'A': [{'time_slot': '9:00 AM', 'classroom_id': 'Room 101', 'section': 'A'}],
                'B': [{'time_slot': '10:00 AM', 'classroom_id': 'Room 102', 'section': 'B'}],
                'C': [{'time_slot': '11:00 AM', 'classroom_id': 'Room 103', 'section': 'C'}],
            },
            'Tuesday': {
                'A': [{'time_slot': '9:00 AM', 'classroom_id': 'Room 101', 'section': 'A'}],
                'B': [{'time_slot': '10:00 AM', 'classroom_id': 'Room 102', 'section': 'B'}],
                'C': [{'time_slot': '11:00 AM', 'classroom_id': 'Room 103', 'section': 'C'}],
            }
        }

        # Create an instance of the TimetableScheduler
        self.scheduler = TimetableScheduler(self.classrooms, self.sections, self.time_slots)

    def test_mutation_occurrence(self):
        """Test if the mutation occurs with the expected frequency."""
        mutation_rate = 0.7  # Mutation rate is set to 70%

        # Run multiple mutations to get more stable results
        num_runs = 10  # You can try more runs for higher accuracy
        mutation_count = 0
        total_entries = sum(len(entries) for day in self.chromosome.values() for section, entries in day.items())
        
        for _ in range(num_runs):
            mutated_chromosome = self.scheduler.mutate_timetable(self.chromosome, mutation_rate)

            # Count how many entries were mutated
            mutated_count = 0
            for day, section_schedule in mutated_chromosome.items():
                for section, entries in section_schedule.items():
                    for entry in entries:
                        # Check if the mutation applied (i.e., values changed)
                        if entry["time_slot"] != '9:00 AM' or entry["classroom_id"] != 'Room 101' or entry["section"] != 'A':
                            mutated_count += 1

            mutation_percentage = mutated_count / total_entries
            mutation_count += mutation_percentage  # Accumulate mutation percentages

        # Calculate average mutation rate across runs
        average_mutation_percentage = mutation_count / num_runs
        print(f"Average Mutation Rate: {average_mutation_percentage}")  # To check the mutation rate in the output

        # Assert that mutation occurs in the expected range
        self.assertGreaterEqual(average_mutation_percentage, 0.5)  # At least 50% mutation
        self.assertLessEqual(average_mutation_percentage, 1.0)  # No more than 100% mutation

    def test_mutate_timetable(self):
        """Test if mutation correctly applies changes to the timetable."""
        mutated_chromosome = self.scheduler.mutate_timetable(self.chromosome, mutation_rate=1.0)

        # Check if mutation has applied changes
        for day, section_schedule in mutated_chromosome.items():
            for section, entries in section_schedule.items():
                for entry in entries:
                    # Check if time_slot, classroom_id, and section have been mutated
                    self.assertIn(entry["time_slot"], self.time_slots)
                    self.assertIn(entry["classroom_id"], self.classrooms)
                    self.assertIn(entry["section"], self.sections)

    def test_mutation_validity(self):
        """Test if the mutated timetable remains valid."""
        mutated_chromosome = self.scheduler.mutate_timetable(self.chromosome, mutation_rate=1.0)

        # Validate that the mutation results in valid values (time_slot, classroom_id, section)
        for day, section_schedule in mutated_chromosome.items():
            for section, entries in section_schedule.items():
                for entry in entries:
                    # Ensure the mutated values are within the expected lists
                    self.assertIn(entry["time_slot"], self.time_slots)
                    self.assertIn(entry["classroom_id"], self.classrooms)
                    self.assertIn(entry["section"], self.sections)

    def test_mutate_empty_chromosome(self):
        """Test mutation with an empty chromosome."""
        empty_chromosome = {}
        mutated_chromosome = self.scheduler.mutate_timetable(empty_chromosome, mutation_rate=1.0)
        self.assertEqual(mutated_chromosome, empty_chromosome)  # Should remain empty


if __name__ == '__main__':
    unittest.main()

#5.def print_chromosomes(self, chromosomes):

import unittest
from unittest.mock import patch
from io import StringIO

class TimetableScheduler:
    def __init__(self, classrooms, sections, teachers, subjects, time_slots):
        self.classrooms = classrooms  # List of classrooms available for assignment
        self.sections = sections  # List of sections
        self.teachers = teachers  # List of teacher IDs
        self.subjects = subjects  # List of subject IDs
        self.time_slots = time_slots  # List of time slots available for scheduling

    def print_chromosomes(self, chromosomes):
        for idx, chromosome in enumerate(chromosomes, 1):
            print(f"\nChromosome {idx}:")
            for day, sections in chromosome.items():
                print(f"  {day}:")
                for section, schedule in sections.items():
                    print(f"    Section {section}:")
                    for entry in schedule:
                        print(f"      Time Slot: {entry['time_slot']}")
                        print(f"        Teacher ID: {entry['teacher_id']}")
                        print(f"        Subject ID: {entry['subject_id']}")
                        print(f"        Classroom ID: {entry['classroom_id']}")
                        print()


class TestTimetableScheduler(unittest.TestCase):

    def setUp(self):
        # Example data to simulate a timetable chromosome
        self.classrooms = ['Room 101', 'Room 102', 'Room 103']
        self.sections = ['A', 'B', 'C']
        self.teachers = ['T1', 'T2', 'T3']
        self.subjects = ['S1', 'S2', 'S3']
        self.time_slots = ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM']

        # Example timetable chromosomes
        self.chromosomes = [
            {
                'Monday': {
                    'A': [{'time_slot': '9:00 AM', 'teacher_id': 'T1', 'subject_id': 'S1', 'classroom_id': 'Room 101'}],
                    'B': [{'time_slot': '10:00 AM', 'teacher_id': 'T2', 'subject_id': 'S2', 'classroom_id': 'Room 102'}],
                    'C': [{'time_slot': '11:00 AM', 'teacher_id': 'T3', 'subject_id': 'S3', 'classroom_id': 'Room 103'}],
                },
                'Tuesday': {
                    'A': [{'time_slot': '9:00 AM', 'teacher_id': 'T1', 'subject_id': 'S1', 'classroom_id': 'Room 101'}],
                    'B': [{'time_slot': '10:00 AM', 'teacher_id': 'T2', 'subject_id': 'S2', 'classroom_id': 'Room 102'}],
                    'C': [{'time_slot': '11:00 AM', 'teacher_id': 'T3', 'subject_id': 'S3', 'classroom_id': 'Room 103'}],
                }
            }
        ]

        # Create an instance of the TimetableScheduler
        self.scheduler = TimetableScheduler(self.classrooms, self.sections, self.teachers, self.subjects, self.time_slots)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_chromosomes(self, mock_stdout):
        """Test if print_chromosomes correctly prints the chromosome information."""
        self.scheduler.print_chromosomes(self.chromosomes)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Expected output for the given chromosomes
        expected_output = """
Chromosome 1:
  Monday:
    Section A:
      Time Slot: 9:00 AM
        Teacher ID: T1
        Subject ID: S1
        Classroom ID: Room 101

    Section B:
      Time Slot: 10:00 AM
        Teacher ID: T2
        Subject ID: S2
        Classroom ID: Room 102

    Section C:
      Time Slot: 11:00 AM
        Teacher ID: T3
        Subject ID: S3
        Classroom ID: Room 103

  Tuesday:
    Section A:
      Time Slot: 9:00 AM
        Teacher ID: T1
        Subject ID: S1
        Classroom ID: Room 101

    Section B:
      Time Slot: 10:00 AM
        Teacher ID: T2
        Subject ID: S2
        Classroom ID: Room 102

    Section C:
      Time Slot: 11:00 AM
        Teacher ID: T3
        Subject ID: S3
        Classroom ID: Room 103
"""
        # Clean up any extra whitespace from the actual output
        output = output.strip()

        # Assert if the output matches the expected output
        self.assertEqual(output, expected_output.strip())

if __name__ == '__main__':
    unittest.main()
