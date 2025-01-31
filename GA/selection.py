import random


class TimeTableSelection:
    def __init__(self):
        pass


    def select_chromosomes(
        self,
        weekly_fitness_scores,
        top_percentage=0.20,
        roulette_percentage=0.10
    ):
        """
            Entry point for selecting chromosomes.
            Select chromosomes based on top scores and roulette wheel selection.
        """

        if not weekly_fitness_scores:
            print("Weekly fitness scores are empty. Ensure data is loaded correctly!")
            return {}

        top_selected, remaining_scores = self.get_top_and_remaining_items(weekly_fitness_scores, top_percentage)

        roulette_selected = self.roulette_wheel_selection(
            remaining_scores,
            int(
                len(weekly_fitness_scores) * roulette_percentage
            )
        )

        selected_fitness = {**top_selected, **roulette_selected}
        # self.display_selected_chromosomes(selected_fitness)
        return selected_fitness


    @staticmethod
    def calculate_cumulative_probabilities(scores):
        """
            Calculate cumulative probabilities for roulette wheel selection.
        """

        cumulative_probabilities = []
        cumulative_sum = 0

        for week, score in scores.items():
            cumulative_sum += score
            cumulative_probabilities.append((cumulative_sum, week))

        return cumulative_probabilities


    @staticmethod
    def perform_roulette_selection(cumulative_probabilities, total_fitness, num_select):
        """
            Perform roulette wheel selection to choose items.
        """

        selected_items = []
        for _ in range(num_select):
            rand_value = random.uniform(0, total_fitness)
            for cumulative_sum, week in cumulative_probabilities:
                if rand_value <= cumulative_sum:
                    selected_items.append(week)
                    break

        return selected_items


    def roulette_wheel_selection(self, scores, num_select):
        """
            Select items using roulette wheel selection.
        """

        if not scores:
            print("Scores are empty. Cannot perform roulette selection.")
            return {}

        total_fitness = sum(scores.values())
        cumulative_probabilities = self.calculate_cumulative_probabilities(scores)
        selected_items = self.perform_roulette_selection(cumulative_probabilities, total_fitness, num_select)
        return {
            week: scores[week] for week in selected_items
        }


    @staticmethod
    def get_top_and_remaining_items(scores, percentage):
        """
        Select the top percentage of items based on scores and return the remaining items.

        Args:
            scores (dict): A dictionary of items with their scores.
            percentage (float): The percentage of top items to select.

        Returns:
            tuple: A tuple of two dictionaries:
                - Top-selected items and their scores.
                - Remaining items and their scores.
        """

        # at least 1 chromosome to select.
        num_select = max(1, int(len(scores) * percentage))
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_selected = dict(sorted_scores[:num_select])
        remaining_items = dict(sorted_scores[num_select:])
        return top_selected, remaining_items


    @staticmethod
    def display_selected_chromosomes(selected_fitness):
        """
            Display the selected chromosomes and their fitness scores.
        """

        print("\n--- Selected Weeks and Fitness Scores ---")
        for week, score in selected_fitness.items():
            print(f"Week: {week}, Score: {score}")
