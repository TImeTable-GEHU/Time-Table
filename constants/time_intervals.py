from datetime import datetime


class TimeIntervalConstant:
    time_slots = {
        1: "9:00 - 9:55",
        2: "9:55 - 10:50",
        3: "11:10 - 12:05",
        4: "12:05 - 1:00",
        5: "1:20 - 2:15",
        6: "2:15 - 3:10",
        7: "3:30 - 4:25",
    }

    time_mapping = {
        "9:00 - 9:55": 1,
        "9:55 - 10:50": 2,
        "11:10 - 12:05": 3,
        "12:05 - 1:00": 4,
        "1:20 - 2:15": 5,
        "2:15 - 3:10": 6,
        "3:30 - 4:25": 7,
    }

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
            raise ValueError(f"Invalid slot number. Please provide a slot number between 1 and {max_slot + 1}.")


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
                slot_start_time = datetime.strptime(interval.split(" - ")[0], "%H:%M").time()
                slot_end_time = datetime.strptime(interval.split(" - ")[1], "%H:%M").time()

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
