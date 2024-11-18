import random

from collections import defaultdict

from constants.constant import ChromosomeConstants


class SectionAllocationFlow:
    # This flow is responsible for allocating sections based on factors we have pre-set.

    def __init__(self, students: dict):
        self.students = students

        classify = lambda cgpas: (
            sorted(cgpas, reverse=True)[max(1, len(cgpas) // 5) - 1],  # Top 20% threshold
            sorted(cgpas)[max(1, len(cgpas) // 5) - 1]  # Bottom 20% threshold
        )

        self.good_cgpa, self.bad_cgpa = classify([student["cgpa"] for student in self.students.values()])

    def calculate_student_score(self, student: dict, cgpa_threshold = 9.0):
        score = 0

        # 1st year students, or year back students don't have CGPA.
        if student.get('CGPA'):
            if student.get('CGPA') >= cgpa_threshold:
                score += ChromosomeConstants.STUDENT_ATTRIBUTE_WEIGHTS.get('good_cgpa', 0)
            else:
                score += ChromosomeConstants.STUDENT_ATTRIBUTE_WEIGHTS.get('average_cgpa', 0)

        if student['Hostler']:
            score += ChromosomeConstants.STUDENT_ATTRIBUTE_WEIGHTS['hostler']
        else:
            score += ChromosomeConstants.STUDENT_ATTRIBUTE_WEIGHTS['non_hostler']

        return score

    def divide_students(self, class_strength):
        # Group students by score
        grouped_by_score = defaultdict(list)
        for student in students:
            score = self.calculate_student_score(student)
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
            'Student_ID': i,
            'CGPA': round(random.uniform(1.0, 9.8), 2),
            'is_Hostler': random.choice([True, False])
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
