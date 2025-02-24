import random
from collections import defaultdict
from typing import Dict, List
from Constants.constant import SectionsConstants


class StudentScorer:
    def __init__(self, attribute_weights: Dict[str, int] = None):
        """
        Initialize the scorer with attribute weights.
        Defaults to SectionsConstants.ATTRIBUTE_WEIGHTS if not provided.
        """
        self.attribute_weights = attribute_weights or SectionsConstants.ATTRIBUTE_WEIGHTS

    def calculate_dynamic_cgpa_threshold(self, students: List[Dict], top_percentage: int = 30) -> float:
        """
        Calculate the CGPA threshold for the top X% of students.
        """
        valid_cgpas = [student.get("cgpa", 0) for student in students if isinstance(student.get("cgpa"), (int, float))]
        if not valid_cgpas:
            return 0  # Default if no valid CGPAs
        sorted_cgpas = sorted(valid_cgpas, reverse=True)
        threshold_index = max(1, int(len(sorted_cgpas) * top_percentage / 100)) - 1
        return sorted_cgpas[threshold_index]

    def assign_dynamic_conditions(self, cgpa_threshold: float):
        """
        Assign a dynamic condition for CGPA based on the threshold.
        """
        SectionsConstants.ATTRIBUTE_CONDITIONS["good_cgpa"] = lambda student: student.get("cgpa", 0) >= cgpa_threshold

    def calculate_student_score(self, student: Dict) -> int:
        """
        Calculate the score for a student based on attribute weights.
        """
        total_score = 0
        for attribute, weight in self.attribute_weights.items():
            condition_func = SectionsConstants.ATTRIBUTE_CONDITIONS.get(attribute, lambda x: False)
            if condition_func(student):    
                total_score += weight
        return total_score

    def assign_scores_to_students(self, students):
        # Step 1: Calculate CGPA threshold
        cgpa_threshold = self.calculate_dynamic_cgpa_threshold(students)
        self.assign_dynamic_conditions(cgpa_threshold)  # Ensure the condition is updated

        print(f"CGPA threshold set at: {cgpa_threshold}")

        # Step 2: Assign scores
        for student in students:
            student["score"] = self.calculate_student_score(student)
            print(f"Assigned Score: {student['student_name']} - {student['score']}")

        return students

    def divide_students_into_sections(self, students: List[Dict], class_strength: int = 50) -> List[List[Dict]]:
        """
        Divide students into sections based on their scores and class strength.
        """
        grouped_by_score = defaultdict(list)
        for student in students:
            grouped_by_score[student["score"]].append(student)

        sections = []
        current_section = []

        for score_group in grouped_by_score.values():
            for student in score_group:
                current_section.append(student)
                if len(current_section) == class_strength:
                    sections.append(current_section)
                    current_section = []

        if current_section:
            sections.append(current_section)

        return sections
<<<<<<< HEAD
=======


def generate_students(num_students: int = 500) -> List[Dict]:
    """
    Generate a list of random students with CGPA and hostler status.

    Args:
        num_students (int): Number of students to generate.

    Returns:
        List[Dict]: List of student dictionaries.
    """

    return [
        {
            'ID': i,
            'CGPA': round(random.uniform(6.0, 9.8), 2),
            'Hostler': random.choice([True, False])
        }
        for i in range(1, num_students + 1)
    ]


if __name__ == "__main__":
    # Initialize constants and scorer
    scorer = StudentScorer()
    students = generate_students(num_students=500)

    # Calculate the dynamic CGPA threshold
    cgpa_threshold = scorer.calculate_dynamic_cgpa_threshold(students, top_percentage=30)
    print(f"Dynamic CGPA Threshold (Top 30%): {cgpa_threshold}")

    # Assign conditions and scores
    scorer.assign_dynamic_conditions(cgpa_threshold)
    students_with_scores = scorer.assign_scores_to_students(students)

    # Divide students into sections
    sections = scorer.divide_students_into_sections(students_with_scores, Defaults.class_strength)

    # Display the sections
    for i, section in enumerate(sections, 1):
        print(f"Section {i} (Total Students: {len(section)}):")
        for student in section:
            print(
                f"  Student ID: {student['ID']}, CGPA: {student['CGPA']}, "
                f"Hostler: {student['Hostler']}, score: {student['score']}"
            )
>>>>>>> 89e907051dd54e4748a9dd197f4b4cd9d0da4c30
