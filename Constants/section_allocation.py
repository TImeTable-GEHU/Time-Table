import random
from collections import defaultdict
from typing import Dict, List

from Constants.constant import Defaults, SectionsConstants


class StudentScorer:
    def __init__(self, attribute_weights: Dict[str, int] = None):
        """
        Initialize the scorer with attribute weights.

        Defaults to SectionsConstants.ATTRIBUTE_WEIGHTS if not provided.
        """

        self.attribute_weights = (
            attribute_weights or SectionsConstants.ATTRIBUTE_WEIGHTS
        )

    def calculate_dynamic_cgpa_threshold(
        self, students: List[Dict], top_percentage: int = 30
    ) -> float:
        """
        Calculate the CGPA threshold for the top X% of students.

        Args:
            students (List[Dict]): List of student dictionaries with 'CGPA'.
            top_percentage (int): Percentage of students considered top.

        Returns:
            float: The CGPA threshold.

        """

        sorted_cgpas = sorted((student["cgpa"] for student in students), reverse=True)

        threshold_index = max(1, int(len(sorted_cgpas) * top_percentage / 100)) - 1
        return sorted_cgpas[threshold_index]

    def assign_dynamic_conditions(self, cgpa_threshold: float):
        """
        Assign a dynamic condition for CGPA based on the threshold.

        Args:
            cgpa_threshold (float): The CGPA threshold for "good_cgpa".
        """
        SectionsConstants.ATTRIBUTE_CONDITIONS["good_cgpa"] = (
            lambda student: student["cgpa"] >= cgpa_threshold
        )

    def calculate_student_score(self, student: Dict) -> int:
        """
        Calculate the score for a student based on attribute weights.

        Args:
            student (Dict): A dictionary representing a student.

        Returns:
            int: The student's score.
        """

        return sum(
            weight
            for attribute, weight in self.attribute_weights.items()
            if SectionsConstants.ATTRIBUTE_CONDITIONS.get(attribute, lambda x: False)(
                student
            )
        )

    def assign_scores_to_students(self, students: List[Dict]) -> List[Dict]:
        """
            Assign scores to all students.

        Args:
            students (List[Dict]): List of student dictionaries.

        Returns:
            List[Dict]: The updated list of students with scores.
        """

        for student in students:
            student["score"] = self.calculate_student_score(student)
        return students

    def divide_students_into_sections(
        self, students: List[Dict], class_strength: int
    ) -> List[List[Dict]]:
        """
        Divide students into sections based on their scores and class strength.

        Args:
            students (List[Dict]): List of student dictionaries with scores.
            class_strength (int): Maximum number of students per section.

        Returns:
            List[List[Dict]]: List of sections containing students.
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
            "ID": i,
            "CGPA": round(random.uniform(6.0, 9.8), 2),
            "Hostler": random.choice([True, False]),
        }
        for i in range(1, num_students + 1)
    ]


if __name__ == "__main__":
    # Initialize constants and scorer
    scorer = StudentScorer()
    students = generate_students(num_students=500)

    # Calculate the dynamic CGPA threshold
    cgpa_threshold = scorer.calculate_dynamic_cgpa_threshold(
        students, top_percentage=30
    )
    print(f"Dynamic CGPA Threshold (Top 30%): {cgpa_threshold}")

    # Assign conditions and scores
    scorer.assign_dynamic_conditions(cgpa_threshold)
    students_with_scores = scorer.assign_scores_to_students(students)

    # Divide students into sections
    sections = scorer.divide_students_into_sections(
        students_with_scores, Defaults.class_strength
    )

    # Display the sections
    for i, section in enumerate(sections, 1):
        print(f"Section {i} (Total Students: {len(section)}):")
        for student in section:
            print(
                f"  Student ID: {student['ID']}, CGPA: {student['CGPA']}, "
                f"Hostler: {student['Hostler']}, score: {student['score']}"
            )
