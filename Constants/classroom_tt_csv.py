import os
import csv
from Samples.samples import (SampleChromosome,WorkingDays)
from Constants.classroom_tt import ClassroomTimetable  # Ensure correct import

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
days_of_week_order =WorkingDays.days

def extract_time_slots(timetable):
    """Extract and sort time slots from timetable."""
    unique_slots = set()

    # Collect all unique time slots
    for day_data in timetable.values():
        for slots in day_data.values():
            for entry in slots:
                if isinstance(entry, dict) and "time_slot" in entry:  # ✅ Ensure correct structure
                    unique_slots.add(entry["time_slot"])
                else:
                    print(f"⚠️ ERROR: Unexpected entry format -> {entry}")

    # Sort slots based on predefined order
    sorted_slots = sorted(unique_slots, key=lambda slot: time_slot_order.get(slot, float('inf')))
    
    return [("CLASS", slot) for slot in sorted_slots]  # Only include class slots

def classroom_json_to_csv(classroom_timetable, output_folder):
    """Convert classroom timetable JSON to CSV."""
    os.makedirs(output_folder, exist_ok=True)
    
    for classroom_id, schedule in classroom_timetable.items():
        final_slots = extract_time_slots(schedule)
        csv_file = os.path.join(output_folder, f"{classroom_id}.csv")
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
                            row[i + 1] = f"{entry['subject_id']} ({section}, {entry['teacher_id']})"
            
            rows.append(row)

        # Write to CSV
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

if __name__ == "__main__":
    # Generate classroom-wise timetable
    classroom_timetable = ClassroomTimetable()
    weekly_schedule = {
        "Week 2": SampleChromosome.schedule2,
        "Week 1": SampleChromosome.schedule1
    }

    classroom_tt = classroom_timetable.generate_classroom_timetable(weekly_schedule)

    # Output folder for CSV files
    output_folder = "output_csvs"

    # Convert the generated timetable to CSV
    classroom_json_to_csv(classroom_tt, output_folder)
