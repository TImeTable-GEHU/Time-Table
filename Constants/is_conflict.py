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
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def insert_schedule(self, timetable, chromosome_name):
        try:
            for day, classes in timetable.items():
                for cls in classes:
                    self.cursor.execute(
                        """ 
                        INSERT INTO schedule (chromosome, day, teacher_id, subject_id, classroom_id, time_slot)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                        (
                            chromosome_name,
                            day,
                            cls["teacher_id"],
                            cls["subject_id"],
                            "N/A",
                            cls["time_slot"],
                        ),
                    )
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting schedule: {e}")
            self.conn.rollback()

    def detect_teacher_conflicts(self):
        try:
            self.cursor.execute(
                """ 
                SELECT s1.teacher_id, s1.day, s1.time_slot
                FROM schedule s1
                JOIN schedule s2
                ON s1.teacher_id = s2.teacher_id
                   AND s1.time_slot = s2.time_slot
                   AND s1.day = s2.day
                   AND (
                        s1.chromosome != s2.chromosome  -- Conflict across chromosomes
                        OR s1.chromosome = s2.chromosome  -- Conflict within the same chromosome
                   )
                GROUP BY s1.teacher_id, s1.day, s1.time_slot
                HAVING COUNT(s1.teacher_id) > 1;  -- More than one class for the same teacher at the same time
            """
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error detecting teacher conflicts: {e}")
            return []

    def truncate_schedule(self):
        try:
            self.cursor.execute("TRUNCATE TABLE schedule;")
            self.conn.commit()
        except Exception as e:
            print(f"Error truncating schedule: {e}")
            self.conn.rollback()

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")

    def process_schedules(self, timetable1, timetable2):
        try:
            self.connect_to_database()

            self.insert_schedule(timetable1, "Week 1")
            self.insert_schedule(timetable2, "Week 2")

            teacher_conflicts = self.detect_teacher_conflicts()
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

            return conflicts
        finally:
            self.truncate_schedule()
            self.close_connection()


if __name__ == "__main__":
    timetable_processor = IsConflict()
    sample_chromosome_1 = SampleChromosome()
    sample_chromosome_2 = SampleChromosome()
    chromosome1 = sample_chromosome_1.schedule1
    chromosome2 = sample_chromosome_2.schedule2

    # Process the timetables and check for conflicts
    conflicts = timetable_processor.process_schedules(chromosome1, chromosome2)

    # Print the detected conflicts (if any)
    print("Conflicts detected:")
    print(conflicts)
