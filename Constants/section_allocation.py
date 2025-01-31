import random
from collections import defaultdict
from typing import List, Dict
from Constants.constant import SectionsConstants, Defaults
from Samples.Adhocs.common import generate_students


class StudentScorer:
    def __init__(self, students: list, attribute_weights: Dict[str, int] = None):
        """
            Initialize the scorer with attribute weights.

            Defaults to SectionsConstants.ATTRIBUTE_WEIGHTS if not provided.
        """

        self.attribute_weights = attribute_weights or SectionsConstants.ATTRIBUTE_WEIGHTS
        self.students = students


    def calculate_dynamic_cgpa_threshold(self, students: List[Dict], top_percentage: int = 30) -> float:
        """
            Calculate the CGPA threshold for the top X% of students.

            Args:
                students (List[Dict]): List of student dictionaries with 'CGPA'.
                top_percentage (int): Percentage of students considered top.

            Returns:
                float: The CGPA threshold.

        """

        sorted_cgpas = sorted(
            (student['CGPA'] for student in students),
            reverse=True
        )

        threshold_index = max(1, int(len(sorted_cgpas) * top_percentage / 100)) - 1
        return sorted_cgpas[threshold_index]


    def assign_dynamic_conditions(self, cgpa_threshold: float):
        """
        Assign a dynamic condition for CGPA based on the threshold.

        Args:
            cgpa_threshold (float): The CGPA threshold for "good_cgpa".
        """
        SectionsConstants.ATTRIBUTE_CONDITIONS['good_cgpa'] = lambda student: student['CGPA'] >= cgpa_threshold


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
            if SectionsConstants.ATTRIBUTE_CONDITIONS.get(attribute, lambda x: False)(student)
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
            student['score'] = self.calculate_student_score(student)
        return students


    def divide_students_into_sections(self, students: List[Dict], class_strength: int) -> List[List[Dict]]:
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
            grouped_by_score[student['score']].append(student)

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

    def entry_point_for_section_divide(self):

        # Calculate the dynamic CGPA threshold
        cgpa_threshold_calc = self.calculate_dynamic_cgpa_threshold(
            self.students,
            top_percentage=30
        )

        # Assign conditions and scores
        self.assign_dynamic_conditions(cgpa_threshold_calc)
        students_with_scores = self.assign_scores_to_students(self.students)

        # Divide students into sections
        class_strength = Defaults.max_class_capacity
        sections = self.divide_students_into_sections(
            students_with_scores,
            class_strength
        )

        section_allocated_students = list()

        for i, section in enumerate(sections, 1):
            for student in section:
                student["section"] = chr(64 + i)
                section_allocated_students.append(student)

        return section_allocated_students




if __name__ == "__main__":

    scorer = StudentScorer(generate_students(num_students=500))
    from icecream import ic
    ic(scorer.entry_point_for_section_divide())
