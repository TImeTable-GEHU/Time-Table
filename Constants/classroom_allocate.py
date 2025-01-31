from ortools.sat.python import cp_model

def assign_section_to_classes(x_section, y_classrooms, z_time_slots):
    # Create a CP-SAT model
    model = cp_model.CpModel()

    # Decision variables
    classrooms = [
        model.NewIntVar(0, y_classrooms - 1, f'classroom_{i}') for i in range(x_section)
    ]
    timeslots = [
        model.NewIntVar(0, z_time_slots - 1, f'timeslot_{i}') for i in range(x_section)
    ]

    # Constraints
    # 1. No two section can share the same classroom and time slot
    for i in range(x_section):
        for j in range(i + 1, x_section):
            # Define a Boolean variable for the condition (timeslots[i] == timeslots[j])
            same_timeslot = model.NewBoolVar(f'same_timeslot_{i}_{j}')
            model.Add(timeslots[i] == timeslots[j]).OnlyEnforceIf(same_timeslot)
            model.Add(timeslots[i] != timeslots[j]).OnlyEnforceIf(same_timeslot.Not())

            # Enforce classroom difference if the timeslot is the same
            model.Add(classrooms[i] != classrooms[j]).OnlyEnforceIf(same_timeslot)


    # Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Check results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(x_section):
            assigned_classroom = solver.Value(classrooms[i])
            assigned_timeslot = solver.Value(timeslots[i])
            print(f"Subject {i + 1} -> Classroom {assigned_classroom}, Timeslot {assigned_timeslot}")
    else:
        print("No feasible solution found.")

from datetime import datetime


start_time = datetime.now()

X = 80  # Number of section
Y = 50  # Number of classrooms
Z = 7   # Number of time slots

assign_section_to_classes(X, Y, Z)

end_time = datetime.now()

print(end_time - start_time)