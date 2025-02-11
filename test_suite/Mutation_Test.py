#MUTATION TESTS

#1. def mutate_time_slots_in_section(self, schedule, section):

import unittest
import random

class TestMutateTimeSlots(unittest.TestCase):
    def setUp(self):
        # Initialize a mock schedule for testing
        self.schedule = {
            "SectionA": [
                {"subject": "Math", "time_slot": "9:00-10:00"},
                {"subject": "English", "time_slot": "10:00-11:00"},
                {"subject": "Science", "time_slot": "11:00-12:00"}
            ],
            "SectionB": [
                {"subject": "History", "time_slot": "9:00-10:00"},
            ],
            "SectionC": []  # Empty section
        }

    def mutate_time_slots_in_section(self, schedule, section):
        """
        Mutates the time slots within a particular section by shuffling them.

        Args:
            schedule (dict): The schedule containing sections and their data.
            section (str): The section in which mutation should occur.

        Returns:
            bool: True if mutation was performed, False otherwise.
        """
        if section in schedule:
            section_list = schedule[section]

            if len(section_list) < 2: 
                return False

            time_slots = [entry["time_slot"] for entry in section_list]
            random.shuffle(time_slots)

            for i, entry in enumerate(section_list):
                entry["time_slot"] = time_slots[i]

            return True
        return False

    def test_valid_mutation(self):
        # Test a valid mutation for SectionA
        original_schedule = [entry["time_slot"] for entry in self.schedule["SectionA"]]
        result = self.mutate_time_slots_in_section(self.schedule, "SectionA")
        self.assertTrue(result, "Mutation should occur with valid input")
        mutated_schedule = [entry["time_slot"] for entry in self.schedule["SectionA"]]

        # Check if time slots were shuffled
        self.assertNotEqual(original_schedule, mutated_schedule, "Schedules should differ after mutation")
        self.assertCountEqual(original_schedule, mutated_schedule, "Schedules should have the same elements after mutation")

    def test_not_enough_time_slots(self):
        # Test mutation for SectionB (not enough time slots to shuffle)
        result = self.mutate_time_slots_in_section(self.schedule, "SectionB")
        self.assertFalse(result, "Mutation should not occur for single-element sections")

    def test_empty_section(self):
        # Test mutation for SectionC (empty section)
        result = self.mutate_time_slots_in_section(self.schedule, "SectionC")
        self.assertFalse(result, "Mutation should not occur for empty sections")

    def test_non_existent_section(self):
        # Test mutation for a section not in the schedule
        result = self.mutate_time_slots_in_section(self.schedule, "SectionD")
        self.assertFalse(result, "Mutation should not occur for non-existent sections")

if __name__ == "__main__":
    unittest.main(verbosity=2)



#2. def mutate_schedule_for_week(self, weekly_schedule):

import unittest
import random
import copy
from unittest.mock import patch


class Mutator:
    def __init__(self, mutation_rate=0.5):
        self.mutation_rate = mutation_rate

    def mutate_time_slots_in_section(self, schedule, section):
        """
        Mutates the time slots within a particular section by shuffling them.

        Args:
            schedule (dict): The schedule containing sections and their data.
            section (str): The section in which mutation should occur.

        Returns:
            bool: True if mutation was performed, False otherwise.
        """
        if section in schedule:
            section_list = schedule[section]
            if len(section_list) < 2:
                return False  # Not enough time slots to shuffle.

            original_slots = [entry["time_slot"] for entry in section_list]
            mutated_slots = original_slots[:]
            attempt_count = 0

            while mutated_slots == original_slots and attempt_count < 5:  # Ensure mutation occurs
                random.shuffle(mutated_slots)
                attempt_count += 1

            if mutated_slots != original_slots:
                for i, entry in enumerate(section_list):
                    entry["time_slot"] = mutated_slots[i]
                return True

        return False

    def mutate_schedule_for_week(self, weekly_schedule):
        """
        Mutates the time slots for all weekdays in the weekly schedule.

        Args:
            weekly_schedule (dict): The weekly schedule containing days, sections, and data.

        Returns:
            dict: The mutated weekly schedule.
        """
        mutated_weekly_schedule = copy.deepcopy(weekly_schedule)
        has_mutation = False  # Track if any mutation occurs

        for day, day_schedule in mutated_weekly_schedule.items():
            total_sections = list(day_schedule.keys())
            num_to_mutate = max(1, int(self.mutation_rate * len(total_sections)))

            sections_to_mutate = random.sample(total_sections, num_to_mutate)

            for section in sections_to_mutate:
                if self.mutate_time_slots_in_section(day_schedule, section):
                    has_mutation = True

        if not has_mutation:  # Ensure at least one mutation occurs
            random_section = random.choice(list(mutated_weekly_schedule.values()))
            random_section_name = random.choice(list(random_section.keys()))
            self.mutate_time_slots_in_section(random_section, random_section_name)

        return mutated_weekly_schedule

    def print_weekly_schedule(self, weekly_schedule):
        """
        Prints the weekly schedule in a readable format.

        Args:
            weekly_schedule (dict): The weekly schedule to print.
        """
        print("\nWeekly Schedule:")
        print("=" * 50)
        for day, day_schedule in weekly_schedule.items():
            print(f"Day: {day}")
            print("-" * 30)
            for section, entries in day_schedule.items():
                print(f"  Section {section}:")
                for entry in entries:
                    print(
                        f"    Teacher: {entry['teacher_id']}, Subject: {entry['subject_id']}, "
                        f"Time Slot: {entry['time_slot']}"
                    )
            print("=" * 50)


class TestMutation(unittest.TestCase):
    def setUp(self):
        self.weekly_schedule = {
            "Monday": {
                "A": [
                    {"teacher_id": "T1", "subject_id": "Math", "time_slot": "9:00 - 9:55"},
                    {"teacher_id": "T2", "subject_id": "Physics", "time_slot": "9:55 - 10:50"},
                ],
                "B": [
                    {"teacher_id": "T3", "subject_id": "Chemistry", "time_slot": "11:10 - 12:05"},
                    {"teacher_id": "T4", "subject_id": "Biology", "time_slot": "12:05 - 1:00"},
                ],
            },
            "Tuesday": {
                "A": [
                    {"teacher_id": "T5", "subject_id": "History", "time_slot": "1:20 - 2:15"},
                ]
            },
        }
        self.mutator = Mutator()

    def test_default_mutation_rate(self):
        self.assertEqual(self.mutator.mutation_rate, 0.5)

    def test_mutate_time_slots_in_section(self):
        section_schedule = [
            {"teacher_id": "T1", "subject_id": "Math", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "T2", "subject_id": "Physics", "time_slot": "9:55 - 10:50"},
        ]
        original_schedule = copy.deepcopy(section_schedule)
        result = self.mutator.mutate_time_slots_in_section({"A": section_schedule}, "A")
        self.assertTrue(result)
        mutated_schedule = section_schedule
        self.assertNotEqual(
            [entry["time_slot"] for entry in original_schedule],
            [entry["time_slot"] for entry in mutated_schedule],
            "Time slots were not mutated",
        )

    @patch("random.shuffle")
    def test_mutate_schedule_for_week(self, mock_shuffle):
        # Mock shuffle to ensure mutation logic works.
        def mock_shuffle_fn(lst):
            lst.reverse()

        mock_shuffle.side_effect = mock_shuffle_fn

        mutated_schedule = self.mutator.mutate_schedule_for_week(self.weekly_schedule)
        self.assertIsInstance(mutated_schedule, dict)

        # Ensure the time slots are not identical
        original_time_slots = [
            entry["time_slot"]
            for day in self.weekly_schedule.values()
            for section in day.values()
            for entry in section
        ]
        mutated_time_slots = [
            entry["time_slot"]
            for day in mutated_schedule.values()
            for section in day.values()
            for entry in section
        ]
        self.assertNotEqual(original_time_slots, mutated_time_slots, "Mutation did not occur.")

    def test_print_weekly_schedule(self):
        # This is primarily for manual verification; ensure no exceptions occur
        self.mutator.print_weekly_schedule(self.weekly_schedule)


if __name__ == "__main__":
    unittest.main()


#3. def print_weekly_schedule(self, weekly_schedule):

import unittest
from unittest.mock import patch
import random
import copy
from Samples.Mutation_Files.mutation import Mutation 

class TestMutation(unittest.TestCase):

    def setUp(self):
        """Setup a basic schedule for testing."""
        self.schedule = {
            "Monday": {
                "A": [
                    {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:55 - 10:50"},
                    {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:00 - 9:55"}
                ]
            },
            "Tuesday": {
                "A": [{"teacher_id": "AK22", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"}],
                "B": [{"teacher_id": "BJ16", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:55 - 10:50"}]
            }
        }

    def test_mutate_schedule_for_week(self):
        """
        Test mutation of the entire week's schedule.
        """
        mutation_rate = 0.5  # For testing, we can use a fixed mutation rate (50%)
        mutator = Mutation(mutation_rate=mutation_rate)

        # Make a deep copy of the original schedule to compare later
        original_schedule = copy.deepcopy(self.schedule)

        # Perform mutation
        mutated_schedule = mutator.mutate_schedule_for_week(self.schedule)

        # Test if the mutated schedule is different from the original schedule
        self.assertNotEqual(self.schedule, mutated_schedule, "The mutated schedule should be different from the original schedule.")

        # Test that at least one section was mutated
        for day in mutated_schedule:
            for section in mutated_schedule[day]:
                # Check if time slots were shuffled (i.e., they're different from the original time slots)
                for original_entry, mutated_entry in zip(original_schedule[day][section], mutated_schedule[day][section]):
                    self.assertNotEqual(original_entry['time_slot'], mutated_entry['time_slot'], 
                                        f"Time slot for {section} on {day} should be mutated.")

    def test_mutate_schedule_with_no_mutation(self):
        """
        Test if mutation does not occur when the mutation rate is 0.
        """
        mutation_rate = 0  # No mutation expected
        mutator = Mutation(mutation_rate=mutation_rate)

        # Make a deep copy of the original schedule to compare later
        original_schedule = copy.deepcopy(self.schedule)

        # Perform mutation
        mutated_schedule = mutator.mutate_schedule_for_week(self.schedule)

        # Test that the mutated schedule is the same as the original schedule
        self.assertEqual(self.schedule, mutated_schedule, "The schedule should remain the same if mutation rate is 0.")

    def test_mutate_schedule_with_max_mutation(self):
        """
        Test if mutation affects all sections when mutation rate is 1.
        """
        mutation_rate = 1  # Full mutation expected
        mutator = Mutation(mutation_rate=mutation_rate)

        # Make a deep copy of the original schedule to compare later
        original_schedule = copy.deepcopy(self.schedule)

        # Perform mutation
        mutated_schedule = mutator.mutate_schedule_for_week(self.schedule)

        # Test that the mutated schedule is different from the original schedule
        self.assertNotEqual(self.schedule, mutated_schedule, "The mutated schedule should be different from the original schedule.")
        
        # Check that all time slots were mutated
        for day in mutated_schedule:
            for section in mutated_schedule[day]:
                for original_entry, mutated_entry in zip(original_schedule[day][section], mutated_schedule[day][section]):
                    self.assertNotEqual(original_entry['time_slot'], mutated_entry['time_slot'], 
                                        f"Time slot for {section} on {day} should be mutated.")

    @patch("random.sample")  # Mock random.sample to control which sections get mutated
    def test_mutate_schedule_with_controlled_mutation(self, mock_sample):
        """
        Test mutation when we control which sections are selected for mutation.
        """
        mutation_rate = 0.5
        mutator = Mutation(mutation_rate=mutation_rate)

        # Mock random.sample to return a controlled selection of sections to mutate
        mock_sample.return_value = ["A"]  # Only mutate section A

        # Make a deep copy of the original schedule to compare later
        original_schedule = copy.deepcopy(self.schedule)

        # Perform mutation
        mutated_schedule = mutator.mutate_schedule_for_week(self.schedule)

        # Test that only section A was mutated, and others remain the same
        for day in mutated_schedule:
            for section in mutated_schedule[day]:
                for original_entry, mutated_entry in zip(original_schedule[day][section], mutated_schedule[day][section]):
                    if section == "A":
                        self.assertNotEqual(original_entry['time_slot'], mutated_entry['time_slot'], 
                                            f"Time slot for {section} on {day} should be mutated.")
                    else:
                        self.assertEqual(original_entry['time_slot'], mutated_entry['time_slot'], 
                                         f"Time slot for {section} on {day} should not be mutated.")

if __name__ == "__main__":
    unittest.main()