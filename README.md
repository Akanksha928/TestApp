# Quiz App API Documentation

This project implements a simple Quiz application using Flask, SQLite, and REST API principles. It allows users to register, log in, take quizzes, and view their quiz scores. The application provides endpoints for user authentication, quiz data retrieval, submitting quiz answers, and viewing user profiles.

## Features
User Registration and Authentication: Allows users to create accounts and log in using their email and password.

Quiz Management: Users can access quiz questions, submit answers, and calculate scores.

User Profile: After taking the quiz, users can view their past scores and quiz attempts.

Cross-Origin Resource Sharing (CORS): The app allows cross-origin requests for use with a frontend.


## API Endpoints
### 1. User Registration
   
POST /register

Description: Registers a new user.

Request Body:

```
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

201 Created: User registered successfully.

400 Bad Request: Missing email or password or user already exists.

### 2. User Login
   
POST /login

Description: Logs in an existing user.

Request Body:

```
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

200 OK: Login successful, returns a cookie with user ID.

401 Unauthorized: Invalid credentials.

### 3. Get Quiz Questions

GET /quiz

Description: Fetches all quiz questions with multiple-choice options.

Response:

```
[
  {
    "id": 1,
    "question": "What is the capital of France?",
    "option1": "Berlin",
    "option2": "Madrid",
    "option3": "Paris",
    "option4": "Rome"
  },
  ...
]

```
### 4. Submit Quiz Answers

POST /submit_quiz

Description: Submits answers for the quiz and calculates the score.

Request Body:

```
{
  "user_id": 1,
  "answers": {
    "1": "3",
    "2": "4"
  }
}
```
Where:

"1": "3" means question 1, answer option 3 (the answer choice).

Response:

200 OK: Score returned.

```
{
  "score": 2,
  "total": 5
}
```

400 Bad Request: Missing user ID or answers.

500 Internal Server Error: Issues with the quiz or database.

### 5. User Profile
   
GET /user_profile/<user_id>

Description: Fetches the user's past quiz scores.

Response:

200 OK: User profile returned.

```
<html>
  <body>
    <h1>User Profile</h1>
    <ul>
      <li>Score: 5, Date: 2025-03-23 12:30:00</li>
      ...
    </ul>
  </body>
</html>

```



