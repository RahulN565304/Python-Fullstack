from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- 1. IMPORT THE TOOL
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# --- THE CORS GUEST LIST ---
origins = [
    "http://127.0.0.1:5500",  # VS Code Live Server (Where your frontend will run)
    "http://localhost:5500",  # Alternative local address
    "*"                       # The wildcard: Allows absolute freedom during learning
]

# --- CONNECT THE GUEST LIST TO YOUR APP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows these websites to talk to your backend
    allow_credentials=True,
    allow_methods=["*"],              # Allows GET, POST, PUT, DELETE operations
    allow_headers=["*"],              # Allows all extra data headers
)

# --- 1. THE SCHEMAS (DATA BLUEPRINTS) ---
class StudentSchema(BaseModel):
    student_name: str
    enrolled_course_id: int

class UpdateCourseSchema(BaseModel):
    student_name: str
    new_course_id: int


# --- 2. THE WRITE OPER (POST) ---
@app.post("/add-student")
def create_new_student(student_data: StudentSchema):
    try:
        conn = psycopg2.connect(
            host="localhost", database="postgres", user="postgres", password="Rahuln04", port="5432"
        )
        cursor = conn.cursor()
        insert_query = "INSERT INTO students (student_name, enrolled_course_id) VALUES (%s, %s);"
        cursor.execute(insert_query, (student_data.student_name, student_data.enrolled_course_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "Success", "message": f"Student {student_data.student_name} enrolled successfully!"}
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Error: The enrolled_course_id you provided does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# --- 3. THE UPDATE OPER (PUT) ---
@app.put("/update-student-course")
def update_student_course(update_data: UpdateCourseSchema):
    try:
        conn = psycopg2.connect(
            host="localhost", database="postgres", user="postgres", password="Rahuln04", port="5432"
        )
        cursor = conn.cursor()
        
        # Check if student exists
        check_query = "SELECT * FROM students WHERE student_name = %s;"
        cursor.execute(check_query, (update_data.student_name,))
        student = cursor.fetchone()
        
        if student is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"Student '{update_data.student_name}' not found.")
            
        # Update query
        update_query = "UPDATE students SET enrolled_course_id = %s WHERE student_name = %s;"
        cursor.execute(update_query, (update_data.new_course_id, update_data.student_name))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "Success", "message": f"Successfully updated {update_data.student_name}'s course."}
    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="Error: The new_course_id you provided does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# --- 4. THE READ OPER (GET) ---
# --- 4. THE READ OPER (GET) WITH QUERY FILTER ---
@app.get("/see-students")
def get_all_students(course: str = None): # <--- We added 'course: str = None' here!
    try:
        conn = psycopg2.connect(
            host="localhost", database="postgres", user="postgres", password="Rahuln04", port="5432"
        )
        cursor = conn.cursor()
        
        # If the user typed a course name in the search bar, filter the results!
        if course:
            join_query = """
                SELECT students.student_name, courses.course_name, courses.duration_weeks
                FROM students
                INNER JOIN courses ON students.enrolled_course_id = courses.course_id
                WHERE courses.course_name ILIKE %s;
            """
            cursor.execute(join_query, (f"%{course}%",))
        else:
            # Otherwise, just show everything like normal
            join_query = """
                SELECT students.student_name, courses.course_name, courses.duration_weeks
                FROM students
                INNER JOIN courses ON students.enrolled_course_id = courses.course_id;
            """
            cursor.execute(join_query)
            
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        enrollment_list = []
        for row in rows:
            enrollment_list.append({"student_name": row[0], "course_name": row[1], "duration_weeks": row[2]})
        return {"status": "Success", "data": enrollment_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    
# --- 5. THE DELETE OPER (DELETE) ---
@app.delete("/remove-student/{name}")
def delete_student(name: str):
    try:
        conn = psycopg2.connect(
            host="localhost", database="postgres", user="postgres", password="Rahuln04", port="5432"
        )
        cursor = conn.cursor()
        
        # 1. Check if the student exists before trying to delete
        check_query = "SELECT * FROM students WHERE student_name = %s;"
        cursor.execute(check_query, (name,))
        student = cursor.fetchone()
        
        if student is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"Student '{name}' not found.")
            
        # 2. If they exist, delete them
        delete_query = "DELETE FROM students WHERE student_name = %s;"
        cursor.execute(delete_query, (name,))
        
        # 3. Commit the change to the hard drive
        conn.commit()
        
        cursor.close()
        conn.close()
        return {"status": "Success", "message": f"Student '{name}' has been completely removed from the database."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")