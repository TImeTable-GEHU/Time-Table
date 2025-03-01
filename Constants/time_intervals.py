from datetime import datetime, timedelta


class TimeIntervalConstant:
    time_slots = {}
    time_mapping = {}

    @staticmethod
    def generate_dynamic_schedule(
        start_time,
        period_duration=55,
        total_periods=7,
        break_after_periods=None,
        lunch_after_period=4,
        break_duration=10,
        lunch_duration=30,
    ):
        if break_after_periods is None:
            break_after_periods = set()
        TimeIntervalConstant.time_slots.clear()
        TimeIntervalConstant.time_mapping.clear()

        start_time = datetime.strptime(start_time, "%H:%M")

        current_time = start_time
        period_counter = 1

        while period_counter <= total_periods:
            end_time = current_time + timedelta(minutes=period_duration)
            time_slot = (
                f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            )
            TimeIntervalConstant.time_slots[period_counter] = time_slot
            TimeIntervalConstant.time_mapping[time_slot] = period_counter
            current_time = end_time
            if period_counter in break_after_periods:
                current_time += timedelta(minutes=break_duration)
            if period_counter == lunch_after_period:
                current_time += timedelta(minutes=lunch_duration)

            period_counter += 1

    @staticmethod
    def get_slot(slot_number: int) -> str:
        """Retrieve time slot based on slot number.

        Args:
            slot_number (int): The slot number corresponding to a time interval.

        Returns:
            str: The time interval for the given slot number.

        Raises:
            ValueError: If the slot number is out of the valid range.
        """

        if slot_number in TimeIntervalConstant.time_slots:
            return TimeIntervalConstant.time_slots[slot_number]

        else:
            max_slot = len(TimeIntervalConstant.time_slots)
            raise ValueError(
                f"Invalid slot number. Please provide a slot number between 1 and {max_slot + 1}."
            )

    @classmethod
    def get_slot_number(cls, start_time: str, end_time: str):
        """Get the slot number for a given start and end time.

        Args:
            start_time (str): The start time in "HH:MM" format.
            end_time (str): The end time in "HH:MM" format.

        Returns:
            int or str: The slot number if found; otherwise, returns an error message.
        """

        try:
            # Format start and end times to ensure they only include hours and minutes
            start_time = str(datetime.strptime(start_time, "%H:%M").time()).strip(" ")
            end_time = str(datetime.strptime(end_time, "%H:%M").time()).strip(" ")

            for slot, interval in cls.time_slots.items():
                # Making string in this format: "3:30 - 4:25".
                slot_start_time = datetime.strptime(
                    interval.split(" - ")[0], "%H:%M"
                ).time()
                slot_end_time = datetime.strptime(
                    interval.split(" - ")[1], "%H:%M"
                ).time()

                if start_time == slot_start_time and end_time == slot_end_time:
                    return slot
            raise LookupError("No Time slot for this time interval found!")

        except ValueError:
            raise ValueError("Invalid time format!")

    @staticmethod
    def get_all_slot_numbers():
        """Retrieve all slot numbers."""
        return list(TimeIntervalConstant.time_slots.keys())

    @staticmethod
    def get_all_time_slots():
        """Retrieve all time intervals."""
        return list(TimeIntervalConstant.time_slots.values())


TimeIntervalConstant.generate_dynamic_schedule(
    "8:00",  # Start time (positional argument)
    60,  # Period duration (positional argument)
    7,  # Total periods (positional argument)
    {2, 6},  # Break after periods (positional argument)
    4,  # Lunch after period (positional argument)
    60,  # Break duration (positional argument)
    50,  # Lunch duration (positional argument)
)

slot_numbers = TimeIntervalConstant.get_all_slot_numbers()


time_slots = TimeIntervalConstant.get_all_time_slots()


# print("Slot Numbers:", slot_numbers)
# print("Time Slots:", time_slots)
