import psycopg2

try:
    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "Rahuln04"
    )
    
    cursor = connection.cursor()

    new_course = "Data Structures"
    new_duration = 8

    safe_query = "INSERT INTO courses (course_name, duration_weeks) VALUES (%s, %s);" 

    cursor.execute(safe_query, (new_course, new_duration))

    connection.commit()
    print(f"Success! Safely inserted '{new_course}' without any SQL injection risk.")

except Exception as error:
    print("Something went wrong: ", error)

finally:
    
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

