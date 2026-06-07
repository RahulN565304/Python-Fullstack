import psycopg2

try:
    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres", 
        user = "postgres",
        password = "Rahuln04"
    )

    cursor = connection.cursor()

    course_id = 5
    
    delete_query = "DELETE FROM courses WHERE course_id = %s;" 

    cursor.execute(delete_query, (course_id,))

    connection.commit()
    print(f"Success! Safely deleted the course without any SQL injection risk.")

except Exception as error:
    print("Something went wrong: ", error)

finally:
    
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
