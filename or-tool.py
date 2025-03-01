import random

from ortools.sat.python import cp_model

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = [
    "9:00 - 9:55",
    "9:55 - 10:50",
    "11:10 - 12:05",
    "12:05 - 1:00",
    "1:20 - 2:15",
    "2:15 - 3:10",
    "3:30 - 4:25",
]
sections = ["A", "B", "C", "D"]
rooms = [
    ("R2", 100, "regular"),
    ("R3", 100, "regular"),
    ("R4", 100, "regular"),
    ("R5", 100, "regular"),
    ("L1", 30, "lab"),
    ("L2", 30, "lab"),
    ("L3", 30, "lab"),
    ("L4", 30, "lab"),
    ("L5", 30, "lab"),
    ("L6", 30, "lab"),
]
# Sample subjects and teachers.
subjects = [
    "TCS-509",
    "TCS-503",
    "TCS-502",
    "TCS-531",
    "TMA-502",
    "PCS-503",
    "PCS-506",
    "CSP-501",
    "XCS-501",
    "SCS-501",
    "PMA-502",
    "Placement_Class",
    "Library",
]
teachers = [
    "HP18",
    "AC05",
    "JM12",
    "RS11",
    "DT20",
    "AB17",
    "DP07",
    "AA04",
    "AB01",
    "SS03",
    "SP06",
    "NJ13",
    "PA21",
    "AK23",
    "RD09",
    "PM14",
    "AK26",
    "AA15",
    "None",
]

# For demonstration we create a list of events.
# Each event has a fixed day, section, period, subject, teacher and group.
# Group 'all' (≈60 students) requires a regular room (capacity ≥60)
# Numeric group (e.g. 1 or 2, ≈30 students) requires a lab (capacity ≥30)
events = []
for d in days:
    for s in sections:
        for p in range(len(periods)):
            subj = random.choice(subjects)
            teach = random.choice(teachers)
            group = random.choice(["all", 1, 2])
            events.append(
                {
                    "day": d,
                    "section": s,
                    "period": p,
                    "subject": subj,
                    "teacher": teach,
                    "group": group,
                }
            )

model = cp_model.CpModel()
vars_rooms = []
for i, ev in enumerate(events):
    allowed = []
    for r_idx, (rname, cap, rtype) in enumerate(rooms):
        if ev["group"] == "all":
            if rtype == "regular" and cap >= 60:
                allowed.append(r_idx)
        else:
            if rtype == "lab" and cap >= 30:
                allowed.append(r_idx)
    if not allowed:
        allowed = list(range(len(rooms)))
    v = model.NewIntVarFromDomain(cp_model.Domain.FromValues(allowed), f"room_{i}")
    vars_rooms.append(v)

# No two events in the same day and period can share a room.
for d in days:
    for p in range(len(periods)):
        idxs = [
            i for i, ev in enumerate(events) if ev["day"] == d and ev["period"] == p
        ]
        if len(idxs) > 1:
            model.AddAllDifferent([vars_rooms[i] for i in idxs])

# For teacher conflicts (ignoring 'None').
for d in days:
    for p in range(len(periods)):
        teach_to_ids = {}
        for i, ev in enumerate(events):
            if ev["day"] == d and ev["period"] == p and ev["teacher"] != "None":
                teach_to_ids.setdefault(ev["teacher"], []).append(i)
        for ids in teach_to_ids.values():
            if len(ids) > 1:
                # If a teacher is scheduled twice at the same time, the model becomes infeasible.
                # In practice, input data should avoid such conflicts.
                model.AddAllDifferent([vars_rooms[i] for i in ids])

solver = cp_model.CpSolver()
status = solver.Solve(model)

schedule = {}
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    for ev, var in zip(events, vars_rooms):
        room_id = rooms[solver.Value(var)][0]
        d, s, p = ev["day"], ev["section"], ev["period"]
        schedule.setdefault(d, {}).setdefault(s, []).append(
            {
                "classroom_id": room_id,
                "group": ev["group"],
                "subject_id": ev["subject"],
                "teacher_id": ev["teacher"],
                "time_slot": periods[p],
            }
        )
    for d in schedule:
        for s in schedule[d]:
            schedule[d][s].sort(key=lambda x: periods.index(x["time_slot"]))
    from icecream import ic

    ic(schedule)

else:
    print("No solution found.")
