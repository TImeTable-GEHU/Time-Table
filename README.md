# Timetable Scheduling Project

## 📚 Overview
Welcome to the **Timetable Scheduling Project**! This repository documents research, findings, discussions, and progress on creating an efficient timetable scheduling system that addresses real-world challenges in academic scheduling. Our goal is to develop a scheduling model that optimally assigns rooms, teachers, and time slots while accommodating various constraints.

## 🔍 Project Goals
- **Optimal Assignment**: Effectively allocate rooms, teachers, and time slots.
- **Constraint Management**: Consider teacher preferences, student load, room capacities, and subject assignments.
- **Dynamic Adaptability**: Adjust to changes, such as adding new rooms or teachers, without complete model retraining.
- **Simplicity and Flexibility**: Simplify complex constraints while remaining adaptable to real-world needs.

## 🧬 Genetic Algorithm
The project employs a Genetic Algorithm (GA) to solve the scheduling problem, inspired by the principles of natural selection. Key modules in our GA include:

1. **Data Encoding and Decoding**: Converting solutions into chromosomes for efficiency.
2. **Initial Population**: Generating a diverse set of potential solutions under specified constraints.
3. **Evaluation of Population**: Using a fitness function to assess solution quality.
4. **Crossover Evolution**: Creating new solutions by combining existing ones.
5. **Mutation**: Introducing random changes to explore new potential solutions.

### Advantages
- Flexibility compared to manual systems
- Reduced processing power requirements
- Quick generation of accurate timetables
- User-friendly data entry and revision
- Improved productivity and minimal paperwork

### Disadvantages
- Requires initial raw content input
- High memory consumption
- Internet connectivity needed

## 📋 Applications
The genetic algorithm can efficiently create various timetables, including:
- University Timetable
- Exam Timetable
- School Timetable
- College Timetable
- Teacher Timetable

## 📊 Results
The system generates distinct timetables for each class, faculty member, and lab, preventing slot conflicts and allowing customization. The program meets both hard and soft scheduling constraints.

## ⚙️ Fitness Function
The fitness function is a critical component of our Genetic Algorithm, as it evaluates the quality of each timetable solution. It incorporates both hard and soft constraints to ensure a balanced and effective scheduling outcome.

### Hard Constraints
These are strict requirements that must be satisfied for a solution to be considered valid:

1. **No Overlap**: 
   - Teachers cannot be assigned to multiple classes at the same time.
   - Time slots must not overlap for the same section.
   - The same classroom cannot be allocated to multiple sections during the same time slot.

2. **Room Capacity**:
   - Each classroom's capacity must accommodate the number of students assigned to that class.

3. **Time Slot Allocation**:
   - Classes must be scheduled within designated time slots.

4. **Teacher Load Distribution**:
   - The total hours assigned to a teacher should not exceed their maximum allowable teaching hours.

### Soft Constraints
These are preferences that enhance the quality of the solution but are not mandatory:

1. **Teacher Preferences**: 
   - Assignments should consider teacher preferences for certain time slots or days.

2. **Gaps Between Classes**:
   - Minimizing the number of gaps between classes for teachers is preferred.

3. **Balanced Workload**:
   - Aim for a balanced distribution of classes among teachers to prevent overloading any single teacher.

4. **Half Days for Sections**
   - Every section should be provided half days so that resources can be utilised properly and also labs and calsses should be balanced.

### Fitness Score Calculation
The fitness score is calculated based on the following criteria:

- Each hard constraint violation deducts a significant penalty from the score (e.g., -100 points for each violation).
- Soft constraint preferences add to the score (e.g., +10 points for each preference met).
- The final score is a reflection of both the number of constraints satisfied and the overall quality of the timetable.

A higher fitness score indicates a better solution, leading to more optimal timetables. The Genetic Algorithm iteratively evolves the population of solutions to maximize this fitness score over generations.

## 🚀 Future Scope
This project aims to simplify faculty management by automatically assigning courses, considering workload balance, and tracking expertise. Future enhancements may include a master schedule for departments, integration with university websites, and personalized time slot assignments.

## 🛠️ Installation

To run this project, clone the repository, set up a virtual environment, and install the required dependencies:

```bash
git clone https://github.com/yourusername/timetable-scheduling-project.git
cd timetable-scheduling-project

# Set up a virtual environment
python -m venv venv

# Activate the virtual environment
# For Linux/macOS:
source venv/bin/activate
# For Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optionally, set up environment variables in a .env file (e.g., DATABASE_URL, SECRET_KEY)
# Create and edit .env file with necessary variables
touch .env

echo "Setup complete. You can now run the application."

