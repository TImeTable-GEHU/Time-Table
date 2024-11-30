from samples import SubjectTeacherMap, WorkingDays, SampleChromosome

class TeacherTimetable:
    def __init__(self):
        # Creating timetable for each teacher
        self.teacher_timetable = {
            teacher: {day: [] for day in WorkingDays.days} 
            for teachers in SubjectTeacherMap.subject_teacher_map.values()  # Iterate over list of teachers
            for teacher in teachers  # Iterate over individual teachers in the list
        }
    
  
    def generate_teacher_timetable(self, chromosome):
        """
        Populate the teacher's timetable based on the provided chromosome schedule.
        Now includes the course (Week 1, Week 2, etc.) information.
        """
        for week, days in chromosome.items():  # week corresponds to "Week 1", "Week 2", etc.
            for day, sections in days.items():  # day corresponds to Monday, Tuesday, etc.
                for section, classes in sections.items():
                    for entry in classes:
                        teacher_id = entry["teacher_id"]
                        subject_id = entry["subject_id"]
                        time_slot = entry["time_slot"]
                        classroom_id = entry["classroom_id"]
                        
                        # Add this slot to the teacher's timetable
                        self.teacher_timetable[teacher_id][day].append({
                            "course": week,  # Include the course name (Week 1, Week 2, etc.)
                            "section": section,
                            "subject_id": subject_id,
                            "time_slot": time_slot,
                            "classroom_id": classroom_id,
                        })


    def display_timetable(self):
        for teacher, days in self.teacher_timetable.items():
            print(f"Teacher: {teacher}")
            for day, classes in days.items():
                print(f"  {day}:")
                for class_entry in classes:
                    print(f"    {class_entry['course']} - Section: {class_entry['section']}, Subject: {class_entry['subject_id']}, Time: {class_entry['time_slot']}, Classroom: {class_entry['classroom_id']}")

if __name__ == "__main__":
    # Initialize timetable
    teacher_timetable = TeacherTimetable()
    
    # Generate timetable from the sample chromosome
    w = {
        "Week 1": SampleChromosome.schedule1,
        "Week 2": SampleChromosome.schedule1
    }
    teacher_timetable.generate_teacher_timetable(w)

    teacher_timetable.display_timetable()                

