import psycopg2

try:
    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "Rahuln04"
    )
    
    cursor = connection.cursor()

    search_input = "Data Structures"

    select_query = "SELECT * FROM courses WHERE course_name = %s;" 

    cursor.execute(select_query, (search_input,))

    matched_courses = cursor.fetchall()

    print("=== SEARCH RESULTS ===")
    for course_id, course_name, duration_weeks in matched_courses:
        print(f"Found: {course_name} ({duration_weeks} Weeks long)")
    print("======================")

except Exception as error:
    print("Something went wrong: ", error)

finally:
    
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
