import psycopg2

try:

    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "Rahuln04"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM courses;")

    all_courses = cursor.fetchall()

    print("=== COVRED COURSES REPORT ===")
     
    for row in all_courses:
        print(f"Course ID: {row[0]} | Name: {row[1]} | Duration:{row[2]} Weeks")

    print("=============================")

except Exception as error:
    print("Something went wrong:", error)

finally:
    # 5. Always unplug your cables when finished to save memory
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

