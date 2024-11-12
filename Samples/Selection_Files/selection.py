import random

class TimeIntervalConstant:
    @staticmethod
    def get_all_time_slots():
        return ["9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-1:00", "1:00-2:00", "2:00-3:00", "3:00-4:00", "4:00-5:00"]

class Timetable:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = TimeIntervalConstant.get_all_time_slots()
        self.teachers = ["T1", "T2", "T3", "T4", "T5"]
        self.subjects = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
        self.classrooms = ["R1", "R2", "R3"]
        self.teacher_subject_map = {
            "T1": ["S1", "S3"],
            "T2": ["S2", "S4", "S6"],
            "T3": ["S2", "S5"],
            "T4": ["S7", "S6"],
            "T5": ["S5", "S1"]
        }
        self.teacher_max_hours = {"T1": 4, "T2": 5, "T3": 4, "T4": 3, "T5": 4}
        self.room_capacity = {"R1": 30, "R2": 25, "R3": 20}
        self.section_strength = {"A": 30, "B": 25, "C": 20, "D": 15}

    def generate_day_schedule(self):
        day_schedule = {}
        time_slot_classroom_usage = {time_slot: set() for time_slot in self.time_slots}
        time_slot_teacher_usage = {time_slot: set() for time_slot in self.time_slots}
        
        for section in self.sections:
            section_schedule = []
            for time_slot in self.time_slots:
                if "Break" in time_slot:
                    schedule_item = {
                        "teacher_id": "None",
                        "subject_id": "Break",
                        "classroom_id": "N/A",
                        "time_slot": time_slot
                    }
                else:
                    teacher, subject, classroom = None, None, None
                    attempts = 0
                    while attempts < 10:
                        teacher = random.choice(self.teachers)
                        subject = random.choice(self.teacher_subject_map[teacher])
                        classroom = random.choice(self.classrooms)
                        if teacher not in time_slot_teacher_usage[time_slot] and \
                           classroom not in time_slot_classroom_usage[time_slot]:
                            break
                        attempts += 1

                    time_slot_teacher_usage[time_slot].add(teacher)
                    time_slot_classroom_usage[time_slot].add(classroom)

                    schedule_item = {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": classroom,
                        "time_slot": time_slot
                    }
                section_schedule.append(schedule_item)
            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self):
        timetable = {}
        for day in self.days:
            timetable[day] = self.generate_day_schedule()
        return timetable

    def create_multiple_timelines(self, num_chromosomes):
        return [self.create_timetable() for _ in range(num_chromosomes)]

    def calculate_fitness(self, chromosome):
        overall_fitness_score = 0
        for day, day_schedule in chromosome.items():
            for section, section_schedule in day_schedule.items():
                section_score = 100
                teacher_time_slots = {}
                classroom_time_slots = {}
                teacher_load = {}

                for item in section_schedule:
                    teacher = item['teacher_id']
                    classroom = item['classroom_id']
                    time_slot = item['time_slot']
                    strength = self.section_strength[section]

                    if "Break" in time_slot:
                        continue

                    if (teacher, time_slot) in teacher_time_slots:
                        section_score -= 30
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section

                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 20
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section

                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)

                    if strength > self.room_capacity[classroom]:
                        section_score -= 25

                for teacher, slots in teacher_load.items():
                    if len(slots) > self.teacher_max_hours[teacher]:
                        section_score -= 15

                    for i in range(1, len(slots)):
                        if "Break" not in slots[i - 1] and "Break" not in slots[i]:
                            section_score -= 10

                overall_fitness_score += max(section_score, 0)

        return overall_fitness_score

    def select_top_chromosomes(self, population: list, percentage=0.30) -> list:
        """
        Selects the top chromosomes based on their fitness scores from the population.
        
        :param population: List of chromosomes (each chromosome is a dictionary representing a timetable).
        :param percentage: The proportion of chromosomes to select (default is 30%).
        :return: A list of selected chromosomes.
        """
        num_to_select = int(len(population) * percentage)
        fitness_scores = [(chromosome, self.calculate_fitness(chromosome)) for chromosome in population]
        sorted_chromosomes = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
        
        best_num = int(num_to_select * 0.20)
        worst_num = int(num_to_select * 0.10)
        middle_num = num_to_select - (best_num + worst_num)
        
        best_chromosomes = sorted_chromosomes[:best_num]
        worst_chromosomes = sorted_chromosomes[-worst_num:]
        middle_chromosomes = sorted_chromosomes[best_num:best_num + middle_num]
        
        roulette_num = int(middle_num * 0.70)
        rank_num = middle_num - roulette_num
        
        total_fitness = sum(fitness for _, fitness in middle_chromosomes)
        roulette_chromosomes = random.choices(middle_chromosomes, weights=[fitness / total_fitness for _, fitness in middle_chromosomes], k=roulette_num)
        
        total_rank = sum(range(1, len(middle_chromosomes) + 1))
        rank_probabilities = [i / total_rank for i in range(1, len(middle_chromosomes) + 1)]
        rank_chromosomes = random.choices(middle_chromosomes, weights=rank_probabilities, k=rank_num)
        
        selected_chromosomes = [chromosome for chromosome, _ in best_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in worst_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in roulette_chromosomes]
        selected_chromosomes += [chromosome for chromosome, _ in rank_chromosomes]
        
        # Output the breakdown
        print(f"Total Number of Chromosomes: {len(population)}")
        print(f"30% of Total Chromosomes: {num_to_select}")
        print(f"Number of Best Chromosomes: {best_num}")
        print(f"Number of Worst Chromosomes: {worst_num}")
        print(f"Number of Chromosomes for Roulette: {roulette_num}")
        print(f"Number of Chromosomes for Rank: {rank_num}")
        
        return selected_chromosomes

# Example usage
timetable_obj = Timetable()
num_chromosomes = 1000
chromosomes = timetable_obj.create_multiple_timelines(num_chromosomes)
selected_chromosomes = timetable_obj.select_top_chromosomes(chromosomes, percentage=0.30)

# Output selected chromosomes
for chromosome in selected_chromosomes[:5]:  # Displaying the first 5 selected chromosomes
    print(chromosome)
