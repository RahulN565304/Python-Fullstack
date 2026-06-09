from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel


app = FastAPI()

class CourseSchema(BaseModel):
    course_name: str
    duration_weeks: int

@app.post("/add-course")
def add_new_course(course_data: CourseSchema):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Rahuln04",   
        port="5432"
    )
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO courses(course_name, duration_weeks) VALUES(%s, %s);"
    cursor.execute(insert_query, (course_data.course_name, course_data.duration_weeks))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"status": "Success", "message": f"Course '{course_data.course_name}' saved to database!"}