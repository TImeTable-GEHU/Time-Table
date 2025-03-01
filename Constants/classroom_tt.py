import json
from Samples.samples import (WorkingDays, SampleChromosome)

class ClassroomTimetable:
    def __init__(self):
        # Dictionary to hold timetables for each classroom
        self.classroom_timetable = {}
        
    def generate_classroom_timetable(self, chromosome):
        for week, days in chromosome.items():
            for day, sections in days.items():
                for section, classes in sections.items():
                    for entry in classes:
                        classroom_id = entry["classroom_id"]

                        if classroom_id not in self.classroom_timetable:
                            self.classroom_timetable[classroom_id] = {day: {} for day in WorkingDays.days}
                        
                        if section not in self.classroom_timetable[classroom_id][day]:
                            self.classroom_timetable[classroom_id][day][section] = []
                        
                        self.classroom_timetable[classroom_id][day][section].append({
                            "subject_id": entry["subject_id"],
                            "teacher_id": entry["teacher_id"],
                            "time_slot": entry["time_slot"],
                        })
        
        return self.classroom_timetable
    
    def save_timetable_to_json(self, file_path="Constants/classroom_timetable.json"):
        try:
            with open(file_path, "w") as json_file:
                json.dump(self.classroom_timetable, json_file, indent=4)
            # print(f"Timetable successfully saved to '{file_path}'.")
        except Exception as e:
            print(f"Error saving timetable to '{file_path}': {e}")

# if __name__ == "__main__":
#     # Generate classroom-wise timetable
#     classroom_timetable = ClassroomTimetable()
#     w = {
#         "Week 2": SampleChromosome.schedule2,
#         "Week 1": SampleChromosome.schedule1
#     }
#     classroom_tt = classroom_timetable.generate_classroom_timetable(w)
#     print(classroom_tt)
#     # Save as JSON
#     classroom_timetable.save_timetable_to_json()
