import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost", 
        database="postgres", 
        user="postgres", 
        password="Rahuln04"
    )
    cursor = connection.cursor()

    
    target_course = "Data Structures"
    updated_weeks = 10

   
    update_query = "UPDATE courses SET duration_weeks = %s WHERE course_name = %s;"

  
    cursor.execute(update_query, (updated_weeks, target_course))

    connection.commit()
    print("Update successful and fully secure!")

except Exception as error:
    print("Error:", error)

finally:

    if 'cursor' in locals(): 
        cursor.close()
    if 'connection' in locals(): 
        connection.close()