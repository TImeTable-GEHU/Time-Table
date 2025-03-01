def update_teacher_availability_matrix(teacher_availability_matrix, best_chromosome):
    for teacher_id, schedule_data in best_chromosome.items():
        if teacher_id in teacher_availability_matrix:
            teacher_availability_matrix[teacher_id] = schedule_data
    return teacher_availability_matrix


def update_matrix_for_best(
    best_chromosome, teacher_availability_matrix, day_map, time_slot_map
):
    for day_name, section_dict in best_chromosome.items():
        if day_name not in day_map:
            continue  # or raise an error
        day_index = day_map[day_name]

        for section_name, schedule_items in section_dict.items():
            for item in schedule_items:
                teacher_id = item["teacher_id"]
                if teacher_id == "None":
                    continue

                time_slot_str = item["time_slot"]
                if time_slot_str not in time_slot_map:
                    continue  # or raise an error
                slot_index = time_slot_map[time_slot_str]

                # Now set availability to False
                teacher_availability_matrix[teacher_id][day_index][
                    slot_index - 1
                ] = False

    return teacher_availability_matrix


def initialize_teacher_availability(teacher_list, num_days=5, num_slots=7):
    return {
        teacher: [[True] * num_slots for _ in range(num_days)]
        for teacher in teacher_list
    }
