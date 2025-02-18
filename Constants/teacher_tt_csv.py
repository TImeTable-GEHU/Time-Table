import os
import json
import csv
from Samples.samples import (WorkingDays, SampleChromosome)
from Constants.teachers_tt import TeacherTimetable

# Predefined time slots mapping
time_slots = {
    1: "08:00 - 09:00",
    2: "09:00 - 10:00",
    3: "11:00 - 12:00",
    4: "12:00 - 13:00",
    5: "16:50 - 17:50",
}

# Reverse lookup to get slot number from time string
time_slot_order = {v: k for k, v in time_slots.items()}

# List of days in the correct order
days_of_week_order = WorkingDays.days

def extract_time_slots(timetable):
    """Extract and sort time slots without inserting breaks or lunch."""
    unique_slots = set()

    # Collect all unique time slots from timetable
    for day_data in timetable.values():
        for slots in day_data.values():
            for entry in slots:
                unique_slots.add(entry["time_slot"])

    # Sort slots based on predefined order
    sorted_slots = sorted(unique_slots, key=lambda slot: time_slot_order.get(slot, float('inf')))
    
    # Only include class slots
    final_slots = [("CLASS", slot) for slot in sorted_slots]
    
    return final_slots

def teacher_json_to_csv(teacher_timetable, output_folder):
    """Convert teacher timetable dictionary to CSV."""
    os.makedirs(output_folder, exist_ok=True)
    
    for teacher_id, schedule in teacher_timetable.items():
        final_slots = extract_time_slots(schedule)
        csv_file = os.path.join(output_folder, f"{teacher_id}.csv")
        header = ["DAY"] + [slot[1] for slot in final_slots]
        rows = []

        # Sort days correctly
        sorted_days = sorted(schedule.items(), key=lambda x: days_of_week_order.index(x[0]))

        for day, day_data in sorted_days:
            row = [day] + ["" for _ in final_slots]  # Empty slots initially
            
            for section, classes in day_data.items():
                for entry in classes:
                    for i, slot in enumerate(final_slots):
                        if entry["time_slot"] == slot[1]:
                            row[i + 1] = f"{entry['subject_id']} ({section}, {entry['classroom_id']})"
            
            rows.append(row)
            
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        
if __name__ == "__main__":
    # Generate teacher-wise timetable
    teacher_timetable = TeacherTimetable()
    w = {
        "Week 2": SampleChromosome.schedule2,
        "Week 1": SampleChromosome.schedule1
    }
    teacher_tt = teacher_timetable.generate_teacher_timetable(w)

    # Convert generated timetable to CSVs
    output_folder = "tt_csvs"  # Folder to save CSVs
    teacher_json_to_csv(teacher_tt, output_folder)
w