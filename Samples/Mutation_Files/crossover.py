class ScheduleCrossover:
    def __init__(self):
        #  schedules for week1 and week2
        self.week1 = {
            "Monday": {
                "A": [{"teacher_id": "SP06", "subject_id": "TCS-503", "classroom_id": "R1", "time_slot": "9:55 - 10:50"}],
                "B": [{"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:00 - 9:55"}]
            },
            "Tuesday": {
                "A": [{"teacher_id": "AK24", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"}],
                "B": [{"teacher_id": "BJ11", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:55 - 10:50"}]
            },
            "Wednesday": {
                "A": [{"teacher_id": "DT20", "subject_id": "XCS-501", "classroom_id": "R1", "time_slot": "11:10 - 12:05"}]
            },
            "Thursday": {
                "A": [{"teacher_id": "SJ11", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "12:05 - 1:00"}]
            },
            "Friday": {
                "A": [{"teacher_id": "AB01", "subject_id": "TCS-531", "classroom_id": "R3", "time_slot": "1:20 - 2:15"}]
            },
            "Saturday": {
                "A": [{"teacher_id": "SJ16", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "2:15 - 3:10"}]
            }
        }

        self.week2 = {
            "Monday": {
                "A": [{"teacher_id": "SP06", "subject_id": "TCS-503", "classroom_id": "R1", "time_slot": "9:55 - 10:50"}],
                "B": [{"teacher_id": "PM14", "subject_id": "PMA-502", "classroom_id": "L2", "time_slot": "9:00 - 9:55"}]
            },
            "Tuesday": {
                "A": [{"teacher_id": "AK22", "subject_id": "CSP-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"}],
                "B": [{"teacher_id": "BJ16", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:55 - 10:50"}]
            },
            "Wednesday": {
                "A": [{"teacher_id": "DT20", "subject_id": "XCS-501", "classroom_id": "R1", "time_slot": "11:10 - 12:05"}]
            },
            "Thursday": {
                "A": [{"teacher_id": "SJ12", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "12:05 - 1:00"}]
            },
            "Friday": {
                "A": [{"teacher_id": "AB01", "subject_id": "TCS-531", "classroom_id": "R3", "time_slot": "1:20 - 2:15"}]
            },
            "Saturday": {
                "A": [{"teacher_id": "SJ14", "subject_id": "TCS-509", "classroom_id": "R1", "time_slot": "2:15 - 3:10"}]
            }
        }

        self.new_offspring = None  # Will hold the result after crossover

    def perform_crossover(self):
        # Days for crossover
        crossover_days = ["Tuesday", "Friday", "Saturday"]

        # Perform the crossover between week1 and week2
        for day in crossover_days:
            self.week1[day], self.week2[day] = self.week2[day], self.week1[day]

        # Create a new chromosome structure with the updated schedules
        self.new_offspring = {
            "week1": self.week1,
            "week2": self.week2
            
        }

    def print_schedule(self):
        # Print the new chromosome after crossover
        for week, schedule in self.new_offspring.items():
            print(f"{week}:")
            for day, details in schedule.items():
                print(f"  {day}: {details}")
            print()  # Empty line between weeks


# Instantiate the class and run the crossover
schedule_crossover = ScheduleCrossover()
schedule_crossover.perform_crossover()
schedule_crossover.print_schedule()