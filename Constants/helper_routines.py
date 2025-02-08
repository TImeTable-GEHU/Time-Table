def update_teacher_availability_matrix(teacher_availability_matrix, best_chromosome):

    for teacher_id, schedule_data in best_chromosome.items():
        if teacher_id in teacher_availability_matrix:
            teacher_availability_matrix[teacher_id] = schedule_data
    return teacher_availability_matrix
