import psycopg2
from Samples.samples import SampleChromosome


class IsConflict:
    def __init__(
        self,
        dbname="timetable_postgres_db",
        user="postgres",
        password="13989333",
        host="localhost",
        port="5432",
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect_to_database(self):
        """Establishes a connection to the database."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.conn.cursor()
            print("Database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.conn = None
            self.cursor = None
            raise

    def insert_schedule(self, timetable, chromosome_name):
        """Inserts the given schedule into the database."""
        if not self.conn or not self.cursor:
            self.connect_to_database()

        try:
            for day, sections in timetable.items():
                for section, classes in sections.items():
                    for cls in classes:
                        self.cursor.execute(
                            """ 
                            INSERT INTO schedule (chromosome, day, section, teacher_id, subject_id, classroom_id, time_slot)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """,
                            (
                                chromosome_name,
                                day,
                                section,
                                cls["teacher_id"],
                                cls["subject_id"],
                                cls["classroom_id"],
                                cls["time_slot"],
                            ),
                        )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting schedule: {e}")
            raise

    def detect_teacher_conflicts(self):
        """Detects scheduling conflicts for teachers."""
        if not self.conn or not self.cursor:
            self.connect_to_database()

        try:
            self.cursor.execute(
                """ 
                SELECT s1.teacher_id, s1.day, s1.time_slot
                FROM schedule s1
                JOIN schedule s2
                ON s1.teacher_id = s2.teacher_id
                   AND s1.time_slot = s2.time_slot
                   AND s1.day = s2.day
                   AND s1.chromosome != s2.chromosome
                GROUP BY s1.teacher_id, s1.day, s1.time_slot;
            """
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error detecting teacher conflicts: {e}")
            raise

    def detect_classroom_conflicts(self):
        """Detects scheduling conflicts for classrooms."""
        if not self.conn or not self.cursor:
            self.connect_to_database()

        try:
            self.cursor.execute(
                """ 
                SELECT s1.classroom_id, s1.day, s1.time_slot
                FROM schedule s1
                JOIN schedule s2
                ON s1.classroom_id = s2.classroom_id
                   AND s1.time_slot = s2.time_slot
                   AND s1.day = s2.day
                   AND s1.chromosome != s2.chromosome
                GROUP BY s1.classroom_id, s1.day, s1.time_slot;
            """
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error detecting classroom conflicts: {e}")
            raise

    def truncate_schedule(self):
        """Clears the schedule table."""
        if not self.conn or not self.cursor:
            self.connect_to_database()

        try:
            self.cursor.execute("TRUNCATE TABLE schedule;")
            self.conn.commit()
        except Exception as e:
            print(f"Error truncating schedule table: {e}")
            raise

    def close_connection(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")

    def process_schedules(self, timetable1, timetable2):
        """Processes schedules and detects conflicts."""
        print("Processing schedules...")
        try:
            self.connect_to_database()

            # Insert schedules
            self.insert_schedule(timetable1, "Week 1")
            self.insert_schedule(timetable2, "Week 2")

            # Detect conflicts
            teacher_conflicts = self.detect_teacher_conflicts()
            classroom_conflicts = self.detect_classroom_conflicts()

            conflicts = []

            for conflict in teacher_conflicts:
                conflicts.append(
                    {
                        "type": "Teacher Conflict",
                        "teacher": conflict[0],
                        "day": conflict[1],
                        "time_slot": conflict[2],
                    }
                )

            for conflict in classroom_conflicts:
                conflicts.append(
                    {
                        "type": "Classroom Conflict",
                        "classroom": conflict[0],
                        "day": conflict[1],
                        "time_slot": conflict[2],
                    }
                )

            return conflicts if conflicts else [{"message": "No conflicts found."}]

        except Exception as e:
            print(f"Error in process_schedules: {e}")
            return [{"error": str(e)}]

        finally:
            if self.conn and self.cursor:
                self.truncate_schedule()
                self.close_connection()


if __name__ == "__main__":
    timetable_processor = IsConflict()

    # Sample timetable instances
    try:
        sample_chromosome_1 = SampleChromosome()
        sample_chromosome_2 = SampleChromosome()

        chromosome1 = sample_chromosome_1.schedule1
        chromosome2 = sample_chromosome_2.schedule2

        conflicts = timetable_processor.process_schedules(chromosome1, chromosome2)

        print(conflicts)
    except Exception as e:
        print(f"Error in main execution: {e}")
