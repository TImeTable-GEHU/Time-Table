import random
from collections import defaultdict

ATTRIBUTE_WEIGHTS = {
    'good_cgpa': 1,         # 2^0
    'average_cgpa': 2,      # 2^1
    'hostler': 4,           # 2^2
    'non_hostler': 8        # 2^3
}

CGPA_THRESHOLD = 9.0

def calculate_student_score(student):
    score = 0
    if student['CGPA'] >= CGPA_THRESHOLD:
        score += ATTRIBUTE_WEIGHTS['good_cgpa']
    else:
        score += ATTRIBUTE_WEIGHTS['average_cgpa']

    if student['Hostler']:
        score += ATTRIBUTE_WEIGHTS['hostler']
    else:
        score += ATTRIBUTE_WEIGHTS['non_hostler']
    return score

def divide_students(students, class_strength):
    # Group students by score
    grouped_by_score = defaultdict(list)
    for student in students:
        score = calculate_student_score(student)
        student['Score'] = score
        grouped_by_score[score].append(student)

    sections = []
    current_section = []

    for score_group in grouped_by_score.values():
        for student in score_group:
            if len(current_section) < class_strength:
                current_section.append(student)
            else:
                sections.append(current_section)
                current_section = [student]

    if current_section:
        sections.append(current_section)

    return sections

def generate_students(num_students=500):
    students = []
    for i in range(1, num_students + 1):
        student = {
            'ID': i,
            'CGPA': round(random.uniform(5.0, 9.8), 2),
            'Hostler': random.choice([True, False])
        }
        students.append(student)
    return students

students = generate_students(500)
class_strength = 100
sections = divide_students(students, class_strength)

for i, section in enumerate(sections):
    print(f"Section {i + 1} (Total Students: {len(section)}):")
    for student in section:
        print(f"  Student ID: {student['ID']}, CGPA: {student['CGPA']}, Hostler: {student['Hostler']}, Score: {student['Score']}")
