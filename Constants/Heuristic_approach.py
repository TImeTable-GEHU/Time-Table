from typing import List, Dict
from ortools.sat.python import cp_model
from datetime import datetime

# ---------------------- Heuristic-Based Room Allocation ----------------------
class Event:
    def _init_(self, id: int, name: str, duration: int, attendees: int, preferred_slots: List[str]):
        self.id = id
        self.name = name
        self.duration = duration
        self.attendees = attendees
        self.preferred_slots = preferred_slots

class Room:
    def _init_(self, id: int, name: str, capacity: int, availability: Dict[str, List[str]]):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.availability = availability  # {"Monday": ["09:00-10:00", "10:00-11:00"], ...}

class Timetable:
    def _init_(self):
        self.schedule = {}  # {room_id: {day: [event_ids]}}

    def is_room_available(self, room: Room, day: str, slot: str) -> bool:
        """Check if a room is available for a given day and time slot."""
        return day in room.availability and slot in room.availability[day]

    def allocate_room(self, event: Event, rooms: List[Room]) -> Dict[str, str]:
        """Heuristic-based room allocation for an event."""
        for room in rooms:
            if room.capacity >= event.attendees:  # Check capacity
                for day, slots in room.availability.items():
                    for slot in slots:
                        if slot in event.preferred_slots and self.is_room_available(room, day, slot):
                            # Allocate room
                            if room.id not in self.schedule:
                                self.schedule[room.id] = {}
                            if day not in self.schedule[room.id]:
                                self.schedule[room.id][day] = []

                            # Conflict check: If another event already scheduled at the same time in the room
                            if slot in self.schedule[room.id][day]:
                                return {"room": None, "day": None, "slot": None}  # Conflict detected

                            self.schedule[room.id][day].append(slot)
                            return {"room": room.name, "day": day, "slot": slot}
        return {"room": None, "day": None, "slot": None}  # No room available

# ---------------------- OR-Tools Constraint-Based Room Allocation ----------------------
def assign_section_to_classes(x_section, y_classrooms, z_time_slots):
    model = cp_model.CpModel()

    # Decision variables
    classrooms = [model.NewIntVar(0, y_classrooms - 1, f'classroom_{i}') for i in range(x_section)]
    timeslots = [model.NewIntVar(0, z_time_slots - 1, f'timeslot_{i}') for i in range(x_section)]

    # Constraints: No two sections in the same room and time slot
    for i in range(x_section):
        for j in range(i + 1, x_section):
            same_timeslot = model.NewBoolVar(f'same_timeslot_{i}_{j}')
            model.Add(timeslots[i] == timeslots[j]).OnlyEnforceIf(same_timeslot)
            model.Add(timeslots[i] != timeslots[j]).OnlyEnforceIf(same_timeslot.Not())
            model.Add(classrooms[i] != classrooms[j]).OnlyEnforceIf(same_timeslot)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Check results
    results = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(x_section):
            results.append({
                "section": i + 1,
                "classroom": solver.Value(classrooms[i]),
                "timeslot": solver.Value(timeslots[i])
            })
    return results

# ---------------------- Hybrid Allocation System ----------------------
def main():
    events = [
        Event(1, "TCS 501", 60, 30, ["09:00-10:00", "10:00-11:00"]),
        Event(2, "TCS 602", 90, 20, ["10:00-11:30", "14:00-15:30"]),
        
    ]

    rooms = [
        Room(1, "CR 101", 50, {"Monday": ["09:00-10:00", "10:00-11:00", "14:00-15:00"]}),
        Room(2, "CR 102", 30, {"Monday": ["10:00-11:00", "14:00-15:30"]}),
    ]

    timetable = Timetable()

    # Heuristic-based allocation first
    conflicts = []
    for event in events:
        allocation = timetable.allocate_room(event, rooms)
        if allocation["room"]:
            print(f"Event '{event.name}' allocated to {allocation['room']} on {allocation['day']} at {allocation['slot']}.")
        else:
            conflicts.append(event)

    # If conflicts exist, resolve them with OR-Tools
    if conflicts:
        print("\n Conflicts detected! Resolving with OR-Tools...\n")
        X = len(conflicts)  # Number of conflicting events
        Y = len(rooms)      # Number of available rooms
        Z = 7               # Number of available time slots (adjust as needed)

        resolved_allocations = assign_section_to_classes(X, Y, Z)

        # Print OR-Tools optimized results
        for idx, conflict in enumerate(conflicts):
            print(f"Event '{conflict.name}' allocated to Room {resolved_allocations[idx]['classroom']} at Time Slot {resolved_allocations[idx]['timeslot']}.")

# Run the system
if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("\nExecution Time:", end_time - start_time)