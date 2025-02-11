# SELECTION TESTS

#1.def get_all_time_slots():

import unittest
from Constants.time_intervals import TimeIntervalConstant
class TestTimeIntervalConstant(unittest.TestCase):
    
    def test_get_all_time_slots(self):
        expected_time_slots = ["9:00 - 9:55", "9:55 - 10:50", "11:10 - 12:05", "12:05 - 1:00", "1:20 - 2:15", "2:15 - 3:10", "3:30 - 4:25"]
        self.assertEqual(TimeIntervalConstant.get_all_time_slots(), expected_time_slots)
        
if __name__ == "__main__":
    unittest.main()

import unittest
from Samples.Selection_Files.selection import Timetable  # Correct import
from unittest import mock

class TestTimetable(unittest.TestCase):
    
    def setUp(self):
        # Initialize the object to be tested
        self.timetable = Timetable()  # Initialize the correct class
    
    def test_generate_day_schedule_structure(self):
        # Call the method
        day_schedule = self.timetable.generate_day_schedule()
        
        # Check if the returned day_schedule is a dictionary with sections
        self.assertIsInstance(day_schedule, dict)
        self.assertGreater(len(day_schedule), 0)
        
        for section, schedule in day_schedule.items():
            self.assertIn(section, self.timetable.sections)  # Ensure sections are correct
            self.assertIsInstance(schedule, list)
            self.assertGreater(len(schedule), 0)
    
    def test_teacher_and_classroom_usage(self):
        # Call the method
        day_schedule = self.timetable.generate_day_schedule()

        # Check that no teacher is assigned to the same time slot more than once
        time_slot_teacher_usage = {time_slot: set() for time_slot in self.timetable.time_slots}
        time_slot_classroom_usage = {time_slot: set() for time_slot in self.timetable.time_slots}

        for section, schedule in day_schedule.items():
            for schedule_item in schedule:
                if "Break" not in schedule_item["time_slot"]:
                    self.assertNotIn(schedule_item["teacher_id"], time_slot_teacher_usage[schedule_item["time_slot"]])
                    self.assertNotIn(schedule_item["classroom_id"], time_slot_classroom_usage[schedule_item["time_slot"]])

                    # Track teacher and classroom usage
                    time_slot_teacher_usage[schedule_item["time_slot"]].add(schedule_item["teacher_id"])
                    time_slot_classroom_usage[schedule_item["time_slot"]].add(schedule_item["classroom_id"])

    def test_break_periods(self):
        # Call the method
        day_schedule = self.timetable.generate_day_schedule()

        # Check that "Break" is assigned correctly
        break_found = False
        for section, schedule in day_schedule.items():
            for schedule_item in schedule:
                if "Break" in schedule_item["subject_id"]:
                    break_found = True
                    self.assertEqual(schedule_item["teacher_id"], "None")
                    self.assertEqual(schedule_item["classroom_id"], "N/A")
        
        self.assertTrue(break_found, "No break periods found in the schedule")

if __name__ == "__main__":
    unittest.main()


#2. def create_timetable(self):

import unittest
from Samples.Selection_Files.selection import Timetable  
from unittest import mock  

class TestTimetable(unittest.TestCase):
    
    def setUp(self):
        # Initialize the Timetable object
        self.timetable = Timetable() 
    
    def test_create_timetable_structure(self):
        # Call the method
        timetable = self.timetable.create_timetable()

        # Check if the timetable is a dictionary with days as keys
        self.assertIsInstance(timetable, dict)
        self.assertGreater(len(timetable), 0)  # Ensure timetable is not empty
        
        # Verify that all days are present
        for day in self.timetable.days:
            self.assertIn(day, timetable)
        
        # Verify that each day contains a schedule (which is a dictionary)
        for day, day_schedule in timetable.items():
            self.assertIsInstance(day_schedule, dict)
            self.assertGreater(len(day_schedule), 0)
    
    def test_generate_day_schedule_called(self):
        # Mock the generate_day_schedule method to check if it's called for each day
        with mock.patch.object(self.timetable, 'generate_day_schedule', return_value={}) as mock_method:
            self.timetable.create_timetable()
            
            # Check if generate_day_schedule was called for each day
            self.assertEqual(mock_method.call_count, len(self.timetable.days))
    
    def test_timetable_content(self):
        # Call the method
        timetable = self.timetable.create_timetable()

        # Check that each day's schedule contains sections
        for day, day_schedule in timetable.items():
            for section, schedule in day_schedule.items():
                self.assertIn(section, self.timetable.sections)  # Ensure valid sections
                self.assertIsInstance(schedule, list)
                self.assertGreater(len(schedule), 0)

if __name__ == "__main__":
    unittest.main()

#3.   def create_multiple_timelines(self, num_chromosomes):

import unittest
from Samples.Selection_Files.selection import Timetable  # Adjust the import as necessary

class TestTimetable(unittest.TestCase):
    
    def setUp(self):
        # Initialize the object to be tested
        self.timetable = Timetable()  # Ensure this is the correct class that has create_multiple_timelines method
    
    def test_create_multiple_timelines(self):
        num_chromosomes = 5  # You can change this number to test with different sizes
        
        # Call the method
        timelines = self.timetable.create_multiple_timelines(num_chromosomes)
        
        # Check if the returned value is a list
        self.assertIsInstance(timelines, list)
        
        # Check if the list has the correct number of timetables
        self.assertEqual(len(timelines), num_chromosomes)
        
        # Optionally, check if each element in the list is a timetable (or has the correct structure)
        for timetable in timelines:
            self.assertIsInstance(timetable, dict)  # Assuming the timetable is a dictionary as in your previous methods
            # Check that the timetable contains valid data, like sections
            for section, schedule in timetable.items():
                self.assertIn(section, self.timetable.sections)
                self.assertIsInstance(schedule, list)
                self.assertGreater(len(schedule), 0)
    
if __name__ == "__main__":
    unittest.main()

#4. def calculate_fitness(self, chromosome):

import unittest
from Samples.Selection_Files.selection import Timetable  # Adjust the import path

class TestTimetableFitness(unittest.TestCase):
    
    def setUp(self):
        # Initialize the object to be tested
        self.timetable = Timetable()  # Ensure this is the class that has calculate_fitness method
    
    def test_fitness_calculation_valid_chromosome(self):
        # Create a valid chromosome structure
        chromosome = {
            "Monday": {
                "A": [
                    {"teacher_id": "T1", "classroom_id": "R1", "time_slot": "9:00-10:00", "subject_id": "S1"},
                    {"teacher_id": "T2", "classroom_id": "R2", "time_slot": "10:00-11:00", "subject_id": "S2"},
                    {"teacher_id": "T3", "classroom_id": "R3", "time_slot": "11:00-12:00", "subject_id": "S3"},
                    {"teacher_id": "None", "classroom_id": "N/A", "time_slot": "Break", "subject_id": "Break"},
                ],
                "B": [
                    {"teacher_id": "T4", "classroom_id": "R1", "time_slot": "9:00-10:00", "subject_id": "S4"},
                    {"teacher_id": "T5", "classroom_id": "R2", "time_slot": "10:00-11:00", "subject_id": "S5"},
                    {"teacher_id": "T1", "classroom_id": "R3", "time_slot": "11:00-12:00", "subject_id": "S6"},
                    {"teacher_id": "None", "classroom_id": "N/A", "time_slot": "Break", "subject_id": "Break"},
                ],
            }
        }

        # Calculate fitness
        fitness_score = self.timetable.calculate_fitness(chromosome)
        
        # Assert fitness score is within expected range
        self.assertIsInstance(fitness_score, int)
        self.assertGreaterEqual(fitness_score, 0)  # Fitness should not be negative

    def test_fitness_calculation_with_violations(self):
        # Create a chromosome with violations (e.g., overlapping time slots)
        chromosome = {
            "Monday": {
                "A": [
                    {"teacher_id": "T1", "classroom_id": "R1", "time_slot": "9:00-10:00", "subject_id": "S1"},
                    {"teacher_id": "T1", "classroom_id": "R2", "time_slot": "9:00-10:00", "subject_id": "S2"},  # Teacher overlap
                    {"teacher_id": "T3", "classroom_id": "R3", "time_slot": "11:00-12:00", "subject_id": "S3"},
                ],
                "B": [
                    {"teacher_id": "T4", "classroom_id": "R1", "time_slot": "9:00-10:00", "subject_id": "S4"},
                    {"teacher_id": "T5", "classroom_id": "R1", "time_slot": "9:00-10:00", "subject_id": "S5"},  # Room overlap
                ],
            }
        }

        # Calculate fitness
        fitness_score = self.timetable.calculate_fitness(chromosome)
        
        # Assert fitness score accounts for penalties
        self.assertIsInstance(fitness_score, int)
        self.assertLess(fitness_score, 100)  # Expect reduced fitness score due to violations

    def test_fitness_calculation_with_over_capacity(self):
        # Create a chromosome where room capacity is exceeded
        chromosome = {
            "Monday": {
                "A": [
                    {"teacher_id": "T1", "classroom_id": "R3", "time_slot": "9:00-10:00", "subject_id": "S1"},  # Over capacity
                ]
            }
        }

        # Calculate fitness
        fitness_score = self.timetable.calculate_fitness(chromosome)
        
        # Assert fitness score is reduced due to capacity violation
        self.assertIsInstance(fitness_score, int)
        self.assertLess(fitness_score, 100)  # Expect reduced fitness score due to capacity penalty
    
    def test_fitness_calculation_no_timetable(self):
        # Test with an empty chromosome
        chromosome = {}

        # Calculate fitness
        fitness_score = self.timetable.calculate_fitness(chromosome)
        
        # Assert fitness score is zero
        self.assertEqual(fitness_score, 0)

if __name__ == "__main__":
    unittest.main()

#5. def select_top_chromosomes(self, population: list, percentage=0.30) -> list:

import random 
def select_top_chromosomes(self, population: list, percentage=0.30) -> list:
    num_to_select = int(len(population) * percentage)
    fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in population]
    sorted_chromosomes = sorted(fitness_scores, key=lambda x: x[1], reverse=True)

    best_num = int(num_to_select * 0.20)
    worst_num = int(num_to_select * 0.10)
    middle_num = num_to_select - (best_num + worst_num)

    best_chromosomes = sorted_chromosomes[:best_num]
    worst_chromosomes = sorted_chromosomes[-worst_num:]
    middle_chromosomes = sorted_chromosomes[best_num:best_num + middle_num]

    roulette_num = int(middle_num * 0.70)
    rank_num = middle_num - roulette_num

    # Handle empty middle_chromosomes for roulette selection
    if middle_chromosomes:
        total_fitness = sum(fitness for _, fitness in middle_chromosomes)
        roulette_chromosomes = random.choices(
            middle_chromosomes,
            weights=[fitness / total_fitness for _, fitness in middle_chromosomes],
            k=roulette_num
        )
    else:
        roulette_chromosomes = []

    if middle_chromosomes:
        total_rank = sum(range(1, len(middle_chromosomes) + 1))
        rank_probabilities = [i / total_rank for i in range(1, len(middle_chromosomes) + 1)]
        rank_chromosomes = random.choices(
            middle_chromosomes,
            weights=rank_probabilities,
            k=rank_num
        )
    else:
        rank_chromosomes = []

    selected_chromosomes = [chromosome for chromosome, _ in best_chromosomes]
    selected_chromosomes += [chromosome for chromosome, _ in worst_chromosomes]
    selected_chromosomes += [chromosome for chromosome, _ in roulette_chromosomes]
    selected_chromosomes += [chromosome for chromosome, _ in rank_chromosomes]

    return selected_chromosomes