from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/courses")
def get_all_courses():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Rahuln04",   
        port="5432"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM courses;")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    
    courses_list = []
    for row in rows:
        courses_list.append({
            "course_id": row[0],
            "course_name": row[1],
            "duration_weeks": row[2]
        })
        
    return {"status": "Success", "data": courses_list}