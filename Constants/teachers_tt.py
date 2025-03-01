import json
from Samples.samples import ( WorkingDays, SampleChromosome)

class TeacherTimetable:
    def __init__(self):
        # Dictionary to hold timetables for each teacher
        self.teacher_timetable = {}
    
    def generate_teacher_timetable(self, chromosome):
        for week, days in chromosome.items():
            for day, sections in days.items():
                for section, classes in sections.items():
                    for entry in classes:
                        teacher_id = entry["teacher_id"]
                        
                        if teacher_id not in self.teacher_timetable:
                            self.teacher_timetable[teacher_id] = {day: {} for day in WorkingDays.days}
                        
                        if section not in self.teacher_timetable[teacher_id][day]:
                            self.teacher_timetable[teacher_id][day][section] = []
                        
                        self.teacher_timetable[teacher_id][day][section].append({
                            "subject_id": entry["subject_id"],
                            "classroom_id": entry["classroom_id"],
                            "time_slot": entry["time_slot"],
                        })
        
        return self.teacher_timetable
    
    def save_timetable_to_json(self, file_path="Constants/teacher_timetable.json"):
        try:
            with open(file_path, "w") as json_file:
                json.dump(self.teacher_timetable, json_file, indent=4)
            print(f"Timetable successfully saved to '{file_path}'.")
        except Exception as e:
            print(f"Error saving timetable to '{file_path}': {e}")

if __name__ == "__main__":
    teacher_timetable = TeacherTimetable()
    w = {
        "Week 2": SampleChromosome.schedule2,
        "Week 1": SampleChromosome.schedule1
    }
    teacher_tt = teacher_timetable.generate_teacher_timetable(w)
    # print(json.dumps(teacher_tt, indent=4))  # Print formatted JSON output
    teacher_timetable.save_timetable_to_json()
