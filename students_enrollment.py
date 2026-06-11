from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/students-enrollment")
def get_all_students_enrollment():

    conn = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "Rahuln04",
        port = "5432"
    )

    cursor = conn.cursor()

    join_query = """

        SELECT students.student_name, courses.course_name, courses.duration_weeks
        FROM students
        INNER JOIN courses
        ON students.enrolled_course_id = courses.course_id;
    """
    cursor.execute(join_query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    enrollment_list = []
    for row in rows:
        enrollment_list.append({
            "student_name" : row[0],
            "course_name" : row[1],
            "duration_weeks" : row[2]
        })

    return {"status": "Success", "data": enrollment_list}
