import random

def mutate_time_slots_in_section(schedule, section):
    """
    Mutates the time slots within a particular section by shuffling them.

    Args:
        schedule (dict): The schedule containing sections and their data.
        section (str): The section in which mutation should occur.

    Returns:
        bool: True if mutation was performed, False otherwise.
    """
    # Check if the section exists in the schedule
    if section in schedule:
        section_list = schedule[section]

        # Ensure there are enough time slots to shuffle
        if len(section_list) < 2:
            print(f"Not enough time slots to mutate in section '{section}'.")
            return False

        # Extract and shuffle the time slots
        time_slots = [entry["time_slot"] for entry in section_list]
        random.shuffle(time_slots)

        # Assign the shuffled time slots back to the section
        for i, entry in enumerate(section_list):
            entry["time_slot"] = time_slots[i]

        print(f"Mutated section '{section}': Time slots randomized.")
        return True
    else:
        print(f"Section '{section}' not found in the schedule.")
        return False


def mutate_all_sections(schedule):
    """
    Mutates time slots for all sections in the schedule.

    Args:
        schedule (dict): The schedule containing sections and their data.

    Returns:
        list: List of sections where mutations occurred.
    """
    mutated_sections = []

    for section in schedule.keys():
        if mutate_time_slots_in_section(schedule, section):
            mutated_sections.append(section)

    return mutated_sections


# Example schedule (reuse the previously defined schedule)
schedule = {
       "A": [
            {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:55 - 10:50"},
            {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "AP24", "subject_id": "SCS-501", "classroom_id": "R1", "time_slot": "11:10 - 12:05"},
            {"teacher_id": "AK23", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "12:05 - 1:00"},
            {"teacher_id": "SS03", "subject_id": "TCS-502", "classroom_id": "R1", "time_slot": "1:20 - 2:15"},
            {"teacher_id": "SP06", "subject_id": "TCS-503", "classroom_id": "R1", "time_slot": "2:15 - 3:10"},
            {"teacher_id": "DT20", "subject_id": "XCS-501", "classroom_id": "R1", "time_slot": "3:30 - 4:25"},
        ],
        "B": [
            {"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:55 - 10:50"},
            {"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "BJ10", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "11:10 - 12:05"},
            {"teacher_id": "PA21", "subject_id": "XCS-501", "classroom_id": "R2", "time_slot": "12:05 - 1:00"},
        ],
        "C": [
            {"teacher_id": "RS11", "subject_id": "TMA-502", "classroom_id": "R3", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "AA04", "subject_id": "TCS-502", "classroom_id": "R3", "time_slot": "9:55 - 10:50"},
            {"teacher_id": "RD09", "subject_id": "PCS-506", "classroom_id": "L3", "time_slot": "12:05 - 1:00"},
            {"teacher_id": "RD09", "subject_id": "PCS-506", "classroom_id": "L3", "time_slot": "11:10 - 12:05"},
            {"teacher_id": "DP07", "subject_id": "TCS-503", "classroom_id": "R3", "time_slot": "1:20 - 2:15"},
            {"teacher_id": "SJ16", "subject_id": "TCS-509", "classroom_id": "R3", "time_slot": "2:15 - 3:10"},
            {"teacher_id": "AB01", "subject_id": "TCS-531", "classroom_id": "R3", "time_slot": "3:30 - 4:25"},
        ],
        "D": [
            {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:55 - 10:50"},
            {"teacher_id": "AD08", "subject_id": "PCS-506", "classroom_id": "L5", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "AC05", "subject_id": "TCS-502", "classroom_id": "R4", "time_slot": "11:10 - 12:05"},
            {"teacher_id": "PK02", "subject_id": "TCS-531", "classroom_id": "R4", "time_slot": "12:05 - 1:00"},
        ],
}

# Perform mutations on all sections
mutated_sections = mutate_all_sections(schedule)

# Print all mutated sections
print("\nAll mutated sections:")
for section in mutated_sections:
    print(f"Section '{section}':", schedule[section])
