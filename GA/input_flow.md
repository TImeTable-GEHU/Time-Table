
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
  {"R1": 200, "R2": 230, ...}
  ```

- **Subjects**:
  ```json
  {"TMA-502": {"teachers": ["BJ10", "RS11"], "credits": 3}, ...}
  ```

## Example Output
[
    {
        "Week 1 - Monday": {
            "A": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R1",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "BJ10",
                    "subject_id": "TMA-502",
                    "classroom_id": "R1",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "SJ16",
                    "subject_id": "TCS-509",
                    "classroom_id": "R1",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "DT20",
                    "subject_id": "XCS-501",
                    "classroom_id": "R1",
                    "time_slot": "12:05 - 1:00"
                }
            ],
            "B": [
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L5",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L5",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AB17",
                    "subject_id": "TCS-509",
                    "classroom_id": "R2",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "PA21",
                    "subject_id": "XCS-501",
                    "classroom_id": "R2",
                    "time_slot": "12:05 - 1:00"
                }
            ],
            "C": [
                {
                    "teacher_id": "SP06",
                    "subject_id": "TCS-503",
                    "classroom_id": "R3",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "TMA-502",
                    "classroom_id": "R3",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L5",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L5",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L4",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L4",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R3",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "D": [
                {
                    "teacher_id": "NB22",
                    "subject_id": "XCS-501",
                    "classroom_id": "R4",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R4",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PMA-502",
                    "classroom_id": "L1",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PMA-502",
                    "classroom_id": "L1",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "TCS-503",
                    "classroom_id": "R4",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "JM12",
                    "subject_id": "TMA-502",
                    "classroom_id": "R4",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "PK02",
                    "subject_id": "TCS-531",
                    "classroom_id": "R4",
                    "time_slot": "3:30 - 4:25"
                }
            ]
        },
        "Week 1 - Tuesday": {
            "A": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R1",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R1",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L5",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L5",
                    "time_slot": "11:10 - 12:05"
                }
            ],
            "B": [
                {
                    "teacher_id": "SP06",
                    "subject_id": "TCS-503",
                    "classroom_id": "R2",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "PK02",
                    "subject_id": "TCS-531",
                    "classroom_id": "R2",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L2",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L2",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R2",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "BJ10",
                    "subject_id": "TMA-502",
                    "classroom_id": "R2",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R2",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "C": [
                {
                    "teacher_id": "SJ16",
                    "subject_id": "TCS-509",
                    "classroom_id": "R3",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "DT20",
                    "subject_id": "XCS-501",
                    "classroom_id": "R3",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "TCS-503",
                    "classroom_id": "R3",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "TMA-502",
                    "classroom_id": "R3",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R3",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R3",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R3",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "D": [
                {
                    "teacher_id": "DP07",
                    "subject_id": "PCS-503",
                    "classroom_id": "L2",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "PCS-503",
                    "classroom_id": "L2",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AC05",
                    "subject_id": "TCS-503",
                    "classroom_id": "R4",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "PA21",
                    "subject_id": "XCS-501",
                    "classroom_id": "R4",
                    "time_slot": "12:05 - 1:00"
                }
            ]
        },
        "Week 1 - Wednesday": {
            "A": [
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L3",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L3",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R1",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "SJ16",
                    "subject_id": "TCS-509",
                    "classroom_id": "R1",
                    "time_slot": "12:05 - 1:00"
                }
            ],
            "B": [
                {
                    "teacher_id": "BJ10",
                    "subject_id": "TMA-502",
                    "classroom_id": "R2",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "SS03",
                    "subject_id": "TCS-502",
                    "classroom_id": "R2",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "SP06",
                    "subject_id": "TCS-503",
                    "classroom_id": "R2",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "DT20",
                    "subject_id": "XCS-501",
                    "classroom_id": "R2",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L1",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "PCS-503",
                    "classroom_id": "L1",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "AB17",
                    "subject_id": "TCS-509",
                    "classroom_id": "R2",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "C": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R3",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "HP18",
                    "subject_id": "TCS-509",
                    "classroom_id": "R3",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "TCS-503",
                    "classroom_id": "R3",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "TMA-502",
                    "classroom_id": "R3",
                    "time_slot": "12:05 - 1:00"
                }
            ],
            "D": [
                {
                    "teacher_id": "DP07",
                    "subject_id": "PCS-503",
                    "classroom_id": "L4",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "PCS-503",
                    "classroom_id": "L4",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AC05",
                    "subject_id": "TCS-503",
                    "classroom_id": "R4",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R4",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "PK02",
                    "subject_id": "TCS-531",
                    "classroom_id": "R4",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "AA04",
                    "subject_id": "TCS-502",
                    "classroom_id": "R4",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "PA21",
                    "subject_id": "XCS-501",
                    "classroom_id": "R4",
                    "time_slot": "3:30 - 4:25"
                }
            ]
        },
        "Week 1 - Thursday": {
            "A": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R1",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "DT20",
                    "subject_id": "XCS-501",
                    "classroom_id": "R1",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L4",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L4",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R1",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "SS03",
                    "subject_id": "TCS-502",
                    "classroom_id": "R1",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R1",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "B": [
                {
                    "teacher_id": "SJ16",
                    "subject_id": "TCS-509",
                    "classroom_id": "R2",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "BJ10",
                    "subject_id": "TMA-502",
                    "classroom_id": "R2",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "SP06",
                    "subject_id": "TCS-503",
                    "classroom_id": "R2",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "PK02",
                    "subject_id": "TCS-531",
                    "classroom_id": "R2",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AA04",
                    "subject_id": "TCS-502",
                    "classroom_id": "R2",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "PA21",
                    "subject_id": "XCS-501",
                    "classroom_id": "R2",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R2",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "C": [
                {
                    "teacher_id": "DP07",
                    "subject_id": "TCS-503",
                    "classroom_id": "R3",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AC05",
                    "subject_id": "TCS-502",
                    "classroom_id": "R3",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R3",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "TMA-502",
                    "classroom_id": "R3",
                    "time_slot": "12:05 - 1:00"
                }
            ],
            "D": [
                {
                    "teacher_id": "SS03",
                    "subject_id": "TCS-502",
                    "classroom_id": "R4",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R4",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "RD09",
                    "subject_id": "PCS-506",
                    "classroom_id": "L3",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "RD09",
                    "subject_id": "PCS-506",
                    "classroom_id": "L3",
                    "time_slot": "11:10 - 12:05"
                }
            ]
        },
        "Week 1 - Friday": {
            "A": [
                {
                    "teacher_id": "SP06",
                    "subject_id": "TCS-503",
                    "classroom_id": "R1",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "SS03",
                    "subject_id": "TCS-502",
                    "classroom_id": "R1",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "DT20",
                    "subject_id": "XCS-501",
                    "classroom_id": "R1",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "BJ10",
                    "subject_id": "TMA-502",
                    "classroom_id": "R1",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "AB01",
                    "subject_id": "TCS-531",
                    "classroom_id": "R1",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R1",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "SJ16",
                    "subject_id": "TCS-509",
                    "classroom_id": "R1",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "B": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R2",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "PA21",
                    "subject_id": "XCS-501",
                    "classroom_id": "R2",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AB17",
                    "subject_id": "TCS-509",
                    "classroom_id": "R2",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R2",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "PK02",
                    "subject_id": "TCS-531",
                    "classroom_id": "R2",
                    "time_slot": "1:20 - 2:15"
                },
                {
                    "teacher_id": "DP07",
                    "subject_id": "TCS-503",
                    "classroom_id": "R2",
                    "time_slot": "2:15 - 3:10"
                },
                {
                    "teacher_id": "AA04",
                    "subject_id": "TCS-502",
                    "classroom_id": "R2",
                    "time_slot": "3:30 - 4:25"
                }
            ],
            "C": [
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L1",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AD08",
                    "subject_id": "PCS-506",
                    "classroom_id": "L1",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L1",
                    "time_slot": "12:05 - 1:00"
                },
                {
                    "teacher_id": "PM14",
                    "subject_id": "PMA-502",
                    "classroom_id": "L1",
                    "time_slot": "11:10 - 12:05"
                }
            ],
            "D": [
                {
                    "teacher_id": "AK23",
                    "subject_id": "CSP-501",
                    "classroom_id": "R4",
                    "time_slot": "9:00 - 9:55"
                },
                {
                    "teacher_id": "NB22",
                    "subject_id": "XCS-501",
                    "classroom_id": "R4",
                    "time_slot": "9:55 - 10:50"
                },
                {
                    "teacher_id": "AP24",
                    "subject_id": "SCS-501",
                    "classroom_id": "R4",
                    "time_slot": "11:10 - 12:05"
                },
                {
                    "teacher_id": "RS11",
                    "subject_id": "TMA-502",
                    "classroom_id": "R4",
                    "time_slot": "12:05 - 1:00"
                }
            ]
        }

## Technologies Used
- **Front-End**: Html,CSS and JavaScript.
- **Back-End**: Django,Python with GA.
- **Database**: MongoDB.


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
