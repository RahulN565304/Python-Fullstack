from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

# 1. Initialize the API application instance
app = FastAPI()

class CourseSchema(BaseModel):
    course_name: str
    duration_weeks: int

@app.put("/update-course/{course_id}")
def update_course_by_id(course_id: int, updated_data: CourseSchema):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",      
        user="postgres",
        password="Rahuln04",  
    )
    
    cursor = conn.cursor()
    
    update_query = """
        UPDATE courses
        SET course_name = %s, duration_weeks = %s
        WHERE course_id = %s;
    """
   
    cursor.execute(update_query, (updated_data.course_name, updated_data.duration_weeks, course_id,))
    
    conn.commit()

    cursor.close()
    conn.close()
      
    return {"status": "Success", "message": f"Course {course_id} has been updated successfully!"}