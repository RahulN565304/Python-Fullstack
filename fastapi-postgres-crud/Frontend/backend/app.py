from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Rahuln04",
    "host": "localhost",
    "port": 5432
}

@app.route('/')
def home():
    return "New Clean Server is officially alive!"

@app.route('/add_student', methods=['POST'])
def add_student():
    student_data = request.get_json()

    name = student_data.get('name')
    course = student_data.get('course')
    age = student_data.get('age')

    print(f"\n Attempting to save to DB: {name}, {course}, {age}")

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO dashboard_students (student_name, course_id, student_age)
            VALUES (%s, %s, %s);
        """
        cur.execute(insert_query, (name, course, int(age)))
        conn.commit()

        cur.close()
        conn.close()

        print("SUCCESS: Saved permanently to the database!\n")
        return jsonify({"message": f"{name} successfully saved to the database!"}), 200
                        
    except Exception as error:
        print(f"DATABASE ERROR: {error}\n")
        return jsonify({"message": "Backend caught data, but database failed.", "error": str(error)}), 500
    
@app.route('/get_students', methods=['GET'])
def get_students():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("SELECT id, student_name, course_id, student_age FROM dashboard_students;")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        students_list = []
        for row in rows:
            students_list.append({
                "id": row[0],
                "name": row[1],
                "course": row[2],
                "age": row[3]
            })

        return jsonify(students_list), 200
        
    except Exception as error:
        print(f"FETCH ERROR: {error}")
        return jsonify({"message": "Failed to read data from database."}), 500
    
@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        cur.execute("DELETE FROM dashboard_students WHERE id = %s;", (student_id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Student deleted successfully!"}), 200
    
    except Exception as error:
        print(f"DELETE ERROR: {error}")
        return jsonify({"message": "Failed to delete student from database."}), 500
    
@app.route('/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        name = data.get('name')
        course = data.get('course')
        age = data.get('age')

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        query = """
            UPDATE dashboard_students
            SET student_name = %s, course_id = %s, student_age = %s
            WHERE id = %s;
        """
        cur.execute(query, (name, course, int(age), student_id))

        conn.commit()
        cur.close()
        conn.close()  

        return jsonify({"message": "Students Updated Successfully!"}), 200
    
    except Exception as error:
        print(f"UPDATEERROR: {error}")
        return jsonify({"message": "Failed to update Student!"}), 500
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT id FROM dashboard_users WHERE username = %s;", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({"error": "Username is already taken"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor.execute(
            "INSERT INTO dashboard_users (username, password_hash) VALUES (%s, %s);",
            (username, hashed_password)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    
    except Exception as error:
        print(f"Error during signup: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and Password are required"}), 400
    
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT id , password_hash FROM dashboard_users WHERE username = %s;", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401
        
        db_password_hash = user[1]

        if bcrypt.check_password_hash(db_password_hash, password):
            return jsonify({
                "message": "Login Successful!",
                "user_id": user[0]
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
        
    except Exception as error:
        print(f"Error during login: {error}")
        return jsonify({"error": "Internal Server error"}), 500

    
if __name__ == '__main__':
    app.run(debug=True, port=5000)