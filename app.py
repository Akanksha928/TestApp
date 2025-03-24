from flask import Flask, request, jsonify, render_template, make_response
import sqlite3
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)  # Allow cross-origin requests (for frontend use)

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                option3 TEXT NOT NULL,
                option4 TEXT NOT NULL,
                correct_option INTEGER NOT NULL)''')
    
    # Create a table to store quiz scores and timestamps
    c.execute('''CREATE TABLE IF NOT EXISTS user_scores (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 score INTEGER NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()  # Create DB if not exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    user_id = request.cookies.get('user_id')  # or session['user_id'] depending on your setup
    
    if user_id:
        return render_template('dashboard.html', user_id=user_id)
    else:
        return render_template('error.html', message="Please log in to access the dashboard.")

# Function to connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        return jsonify({"error": "User already exists"}), 400

    # Insert new user
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            response = make_response(jsonify({"message": "Login successful", "user_id": user[0]}), 200)
            response.set_cookie("user_id", str(user[0]))  # Set the user ID cookie
            return response
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    

@app.route('/quiz', methods=['GET'])
def get_quiz_questions():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")  # Get all questions from the database
    questions = c.fetchall()
    conn.close()

    # Format the questions into a list of dictionaries
    quiz_data = []
    for question in questions:
        quiz_data.append({
            'id': question[0],
            'question': question[1],
            'option1': question[2],
            'option2': question[3],
            'option3': question[4],
            'option4': question[5],
        })

    return jsonify(quiz_data)

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    try:
        # Get submitted answers and user ID from the request
        data = request.json
        user_id = data.get("user_id")
        answers = data.get("answers")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        if not answers:
            return jsonify({"error": "Answers are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch correct answers from the database
        cursor.execute("SELECT id, correct_option FROM questions")
        correct_answers = {row['id']: row['correct_option'] for row in cursor.fetchall()}
        
        # If no questions are fetched, return error
        if not correct_answers:
            return jsonify({"error": "No quiz questions found in the database"}), 500

        conn.close()

        # Calculate the score
        score = 0
        for question_id, selected_option in answers.items():
            if int(selected_option) == correct_answers.get(int(question_id), None):
                score += 1

        # Store the score in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_scores (user_id, score) VALUES (?, ?)", (user_id, score))
        conn.commit()
        conn.close()

        return jsonify({"score": score, "total": len(correct_answers)})

    except Exception as e:
        print("Error submitting quiz:", str(e))  # Print the error to the console for debugging
        return jsonify({"error": f"Failed to submit quiz: {str(e)}"}), 500

    
@app.route('/user_profile/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Fetch the user's past quiz scores
    c.execute("SELECT score, timestamp FROM user_scores WHERE user_id=?", (user_id,))
    scores = c.fetchall()
    
    conn.close()

    return render_template('user_profile.html', scores=scores, user_id=user_id)



if __name__ == "__main__":
    app.run(debug=True)
