import json
import os
from Samples.samples import (WorkingDays, SampleChromosome)

class ClassTimetable:
    def __init__(self):
        """
        Initializes a timetable dictionary dynamically based on the class IDs found in the input chromosome.
        """
        self.class_timetable = {}

    def generate_class_timetable(self, chromosome):
        """
        Populates the class timetable based on the provided chromosome schedule and returns it.
        """
        timetable_dict = {}

        for week, days in chromosome.items():
            for day, sections in days.items():
                for section, classes in sections.items():
                    for entry in classes:
                        classroom_id = entry["classroom_id"]
                        teacher_id = entry["teacher_id"]
                        subject_id = entry["subject_id"]
                        time_slot = entry["time_slot"]

                        # If the classroom_id is not in the timetable_dict, initialize it with an empty day-wise structure
                        if classroom_id not in timetable_dict:
                            timetable_dict[classroom_id] = {day: [] for day in WorkingDays.days}

                        # Iterate through each class in the section
                        for entry in classes:
                            # Ensure the entry has all the necessary keys
                            if not all(k in entry for k in ["teacher_id", "subject_id", "time_slot"]):
                                print(f"Skipping invalid entry (Missing keys): {entry}")
                                continue

                            # Extract values from the class entry
                            teacher_id = entry["teacher_id"]
                            subject_id = entry["subject_id"]
                            time_slot = entry["time_slot"]

                            # Check if the section is already present for the given classroom and day
                            section_entry = {
                                "section": section,
                                "course": week,
                                "teacher_id": teacher_id,
                                "subject_id": subject_id,
                                "time_slot": time_slot
                            }

                            # Add the section to the timetable for the respective classroom and day
                            timetable_dict[classroom_id][day].append(section_entry)

        self.class_timetable = timetable_dict
        return timetable_dict

    def save_timetable_to_json(self, file_path="Constants/class_timetable.json"):
        """
        Saves the class timetable to a JSON file.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w") as json_file:
                json.dump(self.class_timetable, json_file, indent=4)
            
        except Exception as e:
            print(f"Error saving timetable to '{file_path}': {e}")

if __name__ == "__main__":
    class_timetable = ClassTimetable()

    # Verify that SampleChromosome contains the required schedules
    if not hasattr(SampleChromosome, "schedule1") or not hasattr(SampleChromosome, "schedule2"):
        print("Error: SampleChromosome is missing schedule1 or schedule2.")
        exit(1)

    # Generate timetable from the sample chromosome (Week 1 and Week 2)
    week_data = {
        "Week 1": SampleChromosome.schedule1,
        "Week 2": SampleChromosome.schedule2
    }

    # Generate the class timetable
    timetable_dict = class_timetable.generate_class_timetable(week_data)

    # Save the timetable to a JSON file
    class_timetable.save_timetable_to_json()
