from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.delete("/delete-course/{course_id}")
def delete_course_by_id(course_id: int):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Rahuln04",   
        port="5432"
    )
    cursor = conn.cursor()
    
    delete_query = "DELETE FROM courses WHERE course_id = %s;"
    cursor.execute(delete_query, (course_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"status": "Success", "message": f"Course with ID {course_id} has been deleted."}