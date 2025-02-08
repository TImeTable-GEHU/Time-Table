import json
from Samples.samples import (SubjectTeacherMap, WorkingDays, SampleChromosome)

class TeacherTimetable:
    def __init__(self):
        # Create timetable for each teacher
        self.teacher_timetable = {
            teacher: {day: [] for day in WorkingDays.days} 
            for teachers in SubjectTeacherMap.subject_teacher_map.values() 
            for teacher in teachers
        }
        self.teacher_assignments = {teacher: {} for teachers in SubjectTeacherMap.subject_teacher_map.values() for teacher in teachers}

    def generate_teacher_timetable(self, chromosome):
        """
        Populate the teacher's timetable based on the provided chromosome schedule.
        Now includes the course (Week 1, Week 2, etc.) information.
        """
        for week, days in chromosome.items():
            for day, sections in days.items():
                for section, classes in sections.items():
                    for entry in classes:
                        teacher_id = entry["teacher_id"]
                        subject_id = entry["subject_id"]
                        time_slot = entry["time_slot"]
                        classroom_id = entry["classroom_id"]

                        # Conflict check: Ensure the teacher is not already assigned at this time slot
                        if teacher_id in self.teacher_assignments and time_slot in self.teacher_assignments[teacher_id]:
                            continue  # Skip this assignment if there's a conflict

                        # Add the class to the teacher's timetable
                        self.teacher_timetable[teacher_id][day].append({
                            "course": week,  # Include course information (Week 1, Week 2)
                            "section": section,
                            "subject_id": subject_id,
                            "time_slot": time_slot,
                            "classroom_id": classroom_id,
                        })
                        
                        # Update the teacher's assignments to reflect the added class
                        if teacher_id not in self.teacher_assignments:
                            self.teacher_assignments[teacher_id] = {}
                        self.teacher_assignments[teacher_id][time_slot] = {
                            "course": week,
                            "section": section,
                            "subject_id": subject_id,
                            "classroom_id": classroom_id,
                            "day": day
                        }

        return self.teacher_timetable

    def save_timetable_to_json(self, file_path="Constants/teacher_timetable.json"):
        """
        Create a dictionary and save the teacher's timetable to a JSON file.
        """
        try:
            # Create a dictionary explicitly from the teacher timetable
            timetable_dict = {
                teacher: {
                    day: classes
                    for day, classes in days.items()
                }
                for teacher, days in self.teacher_timetable.items()
            }
            
            # Save the dictionary to a JSON file
            with open(file_path, "w") as json_file:
                json.dump(timetable_dict, json_file, indent=4)
                
            print(f"Timetable successfully saved to '{file_path}'.")
        except Exception as e:
            print(f"Error saving timetable to '{file_path}': {e}")

if __name__ == "__main__":
    teacher_timetable = TeacherTimetable()
    # Generate timetable from the sample chromosome (Week 1 and Week 2)
    w = {
        "Week 2": SampleChromosome.schedule2,
        "Week 1": SampleChromosome.schedule1
    }
    
    teacher_tt=teacher_timetable.generate_teacher_timetable(w)
    print(teacher_tt)
    # Save timetable to a JSON file
    teacher_timetable.save_timetable_to_json()
