
### **1. Flow Overview**

The system generates optimized weekly timetables for a university or institution based on various constraints using Genetic Algorithms (GA). The entire workflow is divided into **Front-End**, **Back-End**, **Database Management**, and **Algorithm Processing**.

---

### **2. Front-End Components**

#### **Modules:**
1. **Login Page:**
   - Differentiates between *Admin* and *Teacher*.
   - Ensures data persistence (previous entries are retained).

2. **Constraints Management through Surveys:**
   - Teachers’ preferences:
     - Name
     - Preferred Subject(s)
     - Department, Year, Semester
     - Designation (e.g., HOD for time-slot priority)
     - Email
     - Preferred Time Slots
   - Interfaces for:
     - Adding teachers and assigning subjects.
     - Adding classrooms and labs.

3. **Subject Allocation:**
   - Assign subjects with details like:
     - Subject Code
     - Year & Semester
     - Weekly credits (derived quota).

---

### **3. Back-End Logic**

#### **Database Setup**
- **Classrooms and Capacities:**
  ```python
  classrooms = ["LTB-05", "Civil Lab", "LTB-07", "CLA 07(B)", "R5"]
  room_capacity = {"LTB-05": 200, "Civil Lab": 230, "LTB-07": 240, "CLA 07(B)": 250, "R5": 250}
  ```
- **Subjects and Mappings:**
  ```python
  subject_teacher_map = {
      "TCS-531": ["AB01", "PK02"],
      "TCS-502": ["SS03", "AA04", "AC05"],
      ...
  }
  subject_weekly_quota = {
      "TCS-531": 3,
      "TMA-502": 3,
      ...
  }
  ```
- **Sections and Strength:**
  ```python
  sections = ["A", "B", "C", "D"]
  section_strength = {"A": 200, "B": 200, "C": 200, "D": 100}
  ```

#### **Constraints**
- **Days:**
  ```python
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  ```
- **Time Slots:**
  ```python
  time_slots = {
      1: "9:00 - 9:55",
      2: "9:55 - 10:50",
      ...
  }
  ```

#### **GA Workflow**
1. **Population Initialization:**
   - Chromosomes represent timetable arrangements.

2. **Fitness Function:**
   - Evaluates constraints like:
     - Teacher availability.
     - Room capacity.
     - Overlapping classes.

3. **Selection:**
   - Top 30% of the best chromosomes are passed to crossover.

4. **Crossover:**
   - Combines chromosomes to produce offspring with better scores.

5. **Mutation:**
   - Randomly adjusts schedules to introduce diversity.

6. **Termination:**
   - Best timetable with the highest fitness score is finalized.

---

### **4. Output**
- **Timetable Format:**
  - Weekly schedule per section, listing subjects, teachers, and rooms for each time slot.

---

### **5. Flowchart**
Below is a simplified flowchart:

```
Start
  ↓
Login → Admin/Teacher?
  ↓
Add Constraints (Subjects, Teachers, Classes, etc.)
  ↓
Save Data to Database
  ↓
Initialize Population (Timetable Chromosomes)
  ↓
Evaluate Fitness
  ↓
Selection → Crossover → Mutation
  ↓
Best Chromosome = Optimal Timetable
  ↓
Output Timetable
  ↓
End
```

---

### **6. `README.md`**

```markdown
# Timetable Generator Using Genetic Algorithms

## Overview
This project generates optimized weekly timetables for an institution based on user-defined constraints using a Genetic Algorithm (GA).

## Features
- **Login System**:
  - Differentiates between Admin and Teacher.
  - Saves previous entries to avoid re-entering data.

- **Constraint Management**:
  - Allows input of:
    - Teachers’ preferences (subject, time slots, etc.).
    - Subject details (code, year, semester, credits).
    - Room capacities and section strengths.

- **Timetable Generation**:
  - Ensures constraints like teacher availability, room capacity, and no overlaps.
  - Outputs an optimal timetable per section.

## Workflow
1. **Front-End**:
   - Input constraints via a user-friendly interface.
   - Manage data for teachers, subjects, and classes.

2. **Back-End**:
   - Store input data in structured Python dictionaries.
   - Run GA to generate timetables.

3. **Genetic Algorithm**:
   - Initial population of random timetables.
   - Iterative fitness evaluation, selection, crossover, and mutation.
   - Outputs the timetable with the highest fitness score.

## Example Input Data
- **Rooms**:
  ```json
  {"LTB-05": 200, "Civil Lab": 230, ...}
  ```

- **Subjects**:
  ```json
  {"TMA-502": {"teachers": ["BJ10", "RS11"], "credits": 3}, ...}
  ```

## Example Output
Timetable:
```
--- Weekly Timetable ---

Week 1

Day: Week 1 - Monday
  Section: A
    9:00 - 9:55: TMA-502 (Teacher: BJ10, Room: LTB-05)
    9:55 - 10:50: TCS-502 (Teacher: SS03, Room: LTB-05)
    11:10 - 12:05: TCS-509 (Teacher: SJ16, Room: LTB-05)
    12:05 - 1:00: TCS-503 (Teacher: SP06, Room: LTB-05)
  ----------------------------------------
  Section: B
    9:00 - 9:55: SCS-501 (Teacher: AP24, Room: Civil Lab)
    9:55 - 10:50: TCS-531 (Teacher: AB01, Room: Civil Lab)
    11:10 - 12:05: TCS-502 (Teacher: AA04, Room: Civil Lab)
    12:05 - 1:00: XCS-501 (Teacher: DT20, Room: Civil Lab)
    1:20 - 2:15: TMA-502 (Teacher: RS11, Room: Civil Lab)
    2:15 - 3:10: TCS-509 (Teacher: AB17, Room: Civil Lab)
    3:30 - 4:25: CSP-501 (Teacher: AK23, Room: Civil Lab)
  ----------------------------------------
  Section: C
    9:00 - 9:55: TMA-502 (Teacher: JM12, Room: LTB-07)
    9:55 - 10:50: TCS-502 (Teacher: AC05, Room: LTB-07)
    11:10 - 12:05: TCS-509 (Teacher: HP18, Room: LTB-07)
    12:05 - 1:00: TCS-531 (Teacher: PK02, Room: LTB-07)
    1:20 - 2:15: XCS-501 (Teacher: PA21, Room: LTB-07)
    2:15 - 3:10: TCS-503 (Teacher: DP07, Room: LTB-07)
    3:30 - 4:25: Library (Teacher: None, Room: LTB-07)
  ----------------------------------------
  Section: D
    9:00 - 9:55: TCS-509 (Teacher: SG19, Room: CLA 07(B))
    9:55 - 10:50: TCS-503 (Teacher: AC05, Room: CLA 07(B))
    11:10 - 12:05: XCS-501 (Teacher: NB22, Room: CLA 07(B))
    12:05 - 1:00: TMA-502 (Teacher: NJ13, Room: CLA 07(B))
  ----------------------------------------

Day: Week 1 - Tuesday
  Section: A
    9:55 - 10:50: PCS-503 (Teacher: RS11, Room: LTB-05)
    9:00 - 9:55: PCS-503 (Teacher: RS11, Room: LTB-05)
    11:10 - 12:05: CSP-501 (Teacher: AK23, Room: LTB-05)
    12:05 - 1:00: SCS-501 (Teacher: AP24, Room: LTB-05)
  ----------------------------------------
  Section: B
    9:55 - 10:50: PCS-503 (Teacher: DP07, Room: Civil Lab)
    9:00 - 9:55: PCS-503 (Teacher: DP07, Room: Civil Lab)
    11:10 - 12:05: XCS-501 (Teacher: DT20, Room: Civil Lab)
    12:05 - 1:00: TMA-502 (Teacher: RS11, Room: Civil Lab)
  ----------------------------------------
  Section: C
    9:00 - 9:55: TCS-503 (Teacher: DP07, Room: LTB-07)
    9:55 - 10:50: TCS-502 (Teacher: AC05, Room: LTB-07)
    12:05 - 1:00: PCS-503 (Teacher: SP06, Room: LTB-07)
    11:10 - 12:05: PCS-503 (Teacher: SP06, Room: LTB-07)
    1:20 - 2:15: XCS-501 (Teacher: PA21, Room: LTB-07)
    2:15 - 3:10: TMA-502 (Teacher: JM12, Room: LTB-07)
    3:30 - 4:25: TCS-531 (Teacher: PK02, Room: LTB-07)
  ----------------------------------------
  Section: D
    9:00 - 9:55: TCS-509 (Teacher: SG19, Room: CLA 07(B))
    9:55 - 10:50: TCS-503 (Teacher: AC05, Room: CLA 07(B))
    11:10 - 12:05: XCS-501 (Teacher: NB22, Room: CLA 07(B))
    12:05 - 1:00: TCS-531 (Teacher: AB01, Room: CLA 07(B))
    2:15 - 3:10: PMA-502 (Teacher: PM14, Room: CLA 07(B))
    1:20 - 2:15: PMA-502 (Teacher: PM14, Room: CLA 07(B))
    3:30 - 4:25: TMA-502 (Teacher: NJ13, Room: CLA 07(B))
  ----------------------------------------

Day: Week 1 - Wednesday
  Section: A
    9:00 - 9:55: TCS-509 (Teacher: SJ16, Room: LTB-05)
    9:55 - 10:50: TCS-531 (Teacher: AB01, Room: LTB-05)
    11:10 - 12:05: XCS-501 (Teacher: DT20, Room: LTB-05)
    12:05 - 1:00: CSP-501 (Teacher: AK23, Room: LTB-05)
    1:20 - 2:15: TMA-502 (Teacher: BJ10, Room: LTB-05)
    2:15 - 3:10: TCS-502 (Teacher: SS03, Room: LTB-05)
    3:30 - 4:25: SCS-501 (Teacher: AP24, Room: LTB-05)
  ----------------------------------------
  Section: B
    9:00 - 9:55: TCS-531 (Teacher: AB01, Room: Civil Lab)
    9:55 - 10:50: XCS-501 (Teacher: PA21, Room: Civil Lab)
    12:05 - 1:00: PCS-503 (Teacher: RS11, Room: Civil Lab)
    11:10 - 12:05: PCS-503 (Teacher: RS11, Room: Civil Lab)
  ----------------------------------------
  Section: C
    9:00 - 9:55: TCS-502 (Teacher: AC05, Room: LTB-07)
    9:55 - 10:50: TMA-502 (Teacher: JM12, Room: LTB-07)
    12:05 - 1:00: PCS-506 (Teacher: AD08, Room: LTB-07)
    11:10 - 12:05: PCS-506 (Teacher: AD08, Room: LTB-07)
  ----------------------------------------
  Section: D
    9:00 - 9:55: XCS-501 (Teacher: NB22, Room: CLA 07(B))
    9:55 - 10:50: TMA-502 (Teacher: NJ13, Room: CLA 07(B))
    11:10 - 12:05: TCS-503 (Teacher: AC05, Room: CLA 07(B))
    12:05 - 1:00: TCS-509 (Teacher: SG19, Room: CLA 07(B))
    1:20 - 2:15: TCS-531 (Teacher: AB01, Room: CLA 07(B))
    2:15 - 3:10: TCS-502 (Teacher: SS03, Room: CLA 07(B))
    3:30 - 4:25: Library (Teacher: None, Room: CLA 07(B))
  ----------------------------------------

Day: Week 1 - Thursday
  Section: A
    9:00 - 9:55: CSP-501 (Teacher: AK23, Room: LTB-05)
    9:55 - 10:50: TCS-502 (Teacher: SS03, Room: LTB-05)
    11:10 - 12:05: TCS-503 (Teacher: SP06, Room: LTB-05)
    12:05 - 1:00: TCS-531 (Teacher: AB01, Room: LTB-05)
  ----------------------------------------
  Section: B
    9:00 - 9:55: TCS-509 (Teacher: AB17, Room: Civil Lab)
    9:55 - 10:50: TMA-502 (Teacher: RS11, Room: Civil Lab)
    11:10 - 12:05: TCS-503 (Teacher: SP06, Room: Civil Lab)
    12:05 - 1:00: XCS-501 (Teacher: DT20, Room: Civil Lab)
    1:20 - 2:15: TCS-531 (Teacher: AB01, Room: Civil Lab)
    2:15 - 3:10: TCS-502 (Teacher: AA04, Room: Civil Lab)
    3:30 - 4:25: SCS-501 (Teacher: AP24, Room: Civil Lab)
  ----------------------------------------
  Section: C
    9:00 - 9:55: TCS-503 (Teacher: DP07, Room: LTB-07)
    9:55 - 10:50: XCS-501 (Teacher: PA21, Room: LTB-07)
    11:10 - 12:05: TCS-509 (Teacher: HP18, Room: LTB-07)
    12:05 - 1:00: TMA-502 (Teacher: BJ10, Room: LTB-07)
  ----------------------------------------
  Section: D
    9:00 - 9:55: TCS-509 (Teacher: SJ16, Room: CLA 07(B))
    9:55 - 10:50: XCS-501 (Teacher: NB22, Room: CLA 07(B))
    12:05 - 1:00: PCS-503 (Teacher: RS11, Room: CLA 07(B))
    11:10 - 12:05: PCS-503 (Teacher: RS11, Room: CLA 07(B))
    1:20 - 2:15: TCS-531 (Teacher: AB01, Room: CLA 07(B))
    2:15 - 3:10: TCS-503 (Teacher: DP07, Room: CLA 07(B))
    3:30 - 4:25: TCS-502 (Teacher: SS03, Room: CLA 07(B))
  ----------------------------------------

Day: Week 1 - Friday
  Section: A
    9:00 - 9:55: TCS-509 (Teacher: SJ16, Room: LTB-05)
    9:55 - 10:50: TCS-503 (Teacher: SP06, Room: LTB-05)
    11:10 - 12:05: TCS-531 (Teacher: AB01, Room: LTB-05)
    12:05 - 1:00: SCS-501 (Teacher: AP24, Room: LTB-05)
    1:20 - 2:15: CSP-501 (Teacher: AK23, Room: LTB-05)
    2:15 - 3:10: TMA-502 (Teacher: BJ10, Room: LTB-05)
    3:30 - 4:25: TCS-502 (Teacher: SS03, Room: LTB-05)
  ----------------------------------------
  Section: B
    9:00 - 9:55: TCS-502 (Teacher: AA04, Room: Civil Lab)
    9:55 - 10:50: TMA-502 (Teacher: BJ10, Room: Civil Lab)
    12:05 - 1:00: PCS-503 (Teacher: RS11, Room: Civil Lab)
    11:10 - 12:05: PCS-503 (Teacher: RS11, Room: Civil Lab)
  ----------------------------------------
  Section: C
    9:00 - 9:55: TCS-531 (Teacher: PK02, Room: LTB-07)
    9:55 - 10:50: TCS-509 (Teacher: HP18, Room: LTB-07)
    11:10 - 12:05: XCS-501 (Teacher: DT20, Room: LTB-07)
    12:05 - 1:00: TCS-503 (Teacher: SP06, Room: LTB-07)
  ----------------------------------------
  Section: D
    9:55 - 10:50: PCS-506 (Teacher: AD08, Room: CLA 07(B))
    9:00 - 9:55: PCS-506 (Teacher: AD08, Room: CLA 07(B))
    11:10 - 12:05: XCS-501 (Teacher: PA21, Room: CLA 07(B))
    12:05 - 1:00: TCS-509 (Teacher: SJ16, Room: CLA 07(B))
    2:15 - 3:10: Placement_Class (Teacher: AK26, Room: CLA 07(B))
    1:20 - 2:15: Placement_Class (Teacher: AK26, Room: CLA 07(B))
    3:30 - 4:25: TCS-531 (Teacher: AB01, Room: CLA 07(B))


## Technologies Used
- **Front-End**: Django.
- **Back-End**: Python with GA.
- **Database**: 


### **7. Code Structure**

<!-- #### **Files**
- `main.py`: Main Flask application.
- `ga.py`: Contains the Genetic Algorithm logic.
- `models.py`: Defines data models (teachers, subjects, rooms).
- `utils.py`: Helper functions for GA operations. -->

#### **Code Snippets**

**Fitness Function:**
```python
def calculate_fitness(chromosome):
    score = 0
    for class_schedule in chromosome:
        # Check constraints
        score += check_constraints(class_schedule)
    return score
```

**Crossover:**
```python
def crossover(parent1, parent2):
    point = random.randint(0, len(parent1))
    return parent1[:point] + parent2[point:]
```

**Mutation:**
```python
def mutate(chromosome):
    if random.random() < mutation_rate:
        # Randomly swap time slots
        random.shuffle(chromosome)
    return chromosome
```
