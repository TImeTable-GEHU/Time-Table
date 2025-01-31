import random


def generate_students(num_students: int = 500) -> list:
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
