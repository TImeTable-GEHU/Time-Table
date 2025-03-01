import os
import json
import csv
from datetime import datetime

# Predefined time slots mapping
time_slots = {
    1: "8:00 - 9:00",
    2: "9:00 - 10:00",
    3: "11:10 - 12:05",
    4: "12:05 - 1:00",
    5: "1:20 - 2:15",
    6: "2:15 - 3:10",
    7: "3:30 - 4:25",
}

# Reverse lookup to get slot number from time string
time_slot_order = {v: k for k, v in time_slots.items()}

# List of days in the order we want them to appear
days_of_week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def parse_time(time_slot):
    """Extract start and end times from a time slot string."""
    start_time_str, end_time_str = time_slot.split(" - ")
    start_time = datetime.strptime(start_time_str.strip(), "%I:%M").time()
    end_time = datetime.strptime(end_time_str.strip(), "%I:%M").time()
    return start_time, end_time

def extract_time_slots(timetable):
    """Extract, sort time slots, and insert BREAK/LUNCH where needed."""
    unique_slots = set()

    # Collect all unique time slots from timetable
    for day_data in timetable.values():
        for slots in day_data.values():
            for entry in slots:
                unique_slots.add(entry["time_slot"])

    # Sort slots based on predefined order
    sorted_slots = sorted(unique_slots, key=lambda slot: time_slot_order[slot])

    # Insert BREAK and LUNCH dynamically based on gaps
    final_slots = []
    last_end_time = None
    break_lunch_counter = 0

    for slot in sorted_slots:
        start_time, end_time = parse_time(slot)

        if last_end_time:
            gap = (datetime.combine(datetime.today(), start_time) - datetime.combine(datetime.today(), last_end_time)).seconds / 60

            if gap > 5:  # If there's a gap greater than 5 minutes
                break_time = f"{last_end_time.strftime('%I:%M')} - {start_time.strftime('%I:%M')}"
                if break_lunch_counter == 0:
                    final_slots.append(("BREAK", break_time))
                elif break_lunch_counter == 1:
                    final_slots.append(("LUNCH", break_time))
                else:
                    final_slots.append(("BREAK", break_time))

                break_lunch_counter += 1  # Increment counter

        final_slots.append(("CLASS", slot))
        last_end_time = end_time  # Update last_end_time

    return final_slots

def json_to_csv(input_folder, json_filename, output_folder):
    """Convert JSON timetable to CSV with breaks and lunches inserted."""
    json_file = os.path.join(input_folder, json_filename)

    with open(json_file, "r", encoding="utf-8") as file:
        timetable = json.load(file)

    sections = set()
    final_slots = extract_time_slots(timetable)

    os.makedirs(output_folder, exist_ok=True)

    # Identify all sections
    for day_data in timetable.values():
        for section in day_data.keys():
            sections.add(section)

    # Sort days in the correct order
    sorted_days = sorted(timetable.items(), key=lambda x: days_of_week_order.index(x[0]))

    for section in sections:
        csv_file = os.path.join(output_folder, f"{section}.csv")
        header = ["DAY"] + [slot[1] for slot in final_slots]  # Extract only time for header
        rows = []

        # Iterate over sorted days in the correct order
        for day, day_data in sorted_days:  # Sorted days based on days_of_week_order
            # Initialize row with blank spaces
            row = [day] + [""] * len(final_slots)  # Initially empty for each time slot

            if section in day_data:
                for entry in day_data[section]:
                    for i, slot in enumerate(final_slots):
                        # Compare and add the class schedule, BREAK, or LUNCH
                        if entry["time_slot"] == slot[1] and slot[0] == "CLASS":
                            row[i + 1] = f"{entry['subject_id']} ({entry['teacher_id']}, {entry['classroom_id']})"
                        elif slot[0] == "BREAK" or slot[0] == "LUNCH":
                            # Add BREAK and LUNCH to appropriate slots
                            row[i + 1] = slot[0]

            rows.append(row)

        # Write the row into CSV
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"CSV file '{csv_file}' has been created successfully!")

if __name__ == "_main_":
    input_folder = "."  # Your input folder where the JSON file is located
    json_filename = "new.json"  # Replace with your actual JSON filename
    output_folder = "output_csvs"  # Output folder where CSV files will be saved
    json_to_csv(input_folder, json_filename, output_folder)