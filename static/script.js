const baseURL = "http://127.0.0.1:5000"; // Flask backend URL

const errorMessageContainer = document.getElementById("error-message");

// Handle login/register toggle
document.getElementById("toggle-form")?.addEventListener("click", function () {
    let formTitle = document.getElementById("form-title");
    let submitButton = document.querySelector("button");
    let toggleText = document.getElementById("toggle-form");

    if (formTitle.innerText === "Login") {
        formTitle.innerText = "Register";
        submitButton.innerText = "Register";
        toggleText.innerHTML = 'Already have an account? <a href="#">Login</a>';
    } else {
        formTitle.innerText = "Login";
        submitButton.innerText = "Login";
        toggleText.innerHTML = 'Don\'t have an account? <a href="#">Register</a>';
    }
});

// Handle login/register form submission
document.getElementById("auth-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const formTitle = document.getElementById("form-title").innerText;
    const endpoint = formTitle === "Login" ? "/login" : "/register";

    const response = await fetch(`${baseURL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (response.ok) {
        if (formTitle === "Login") {
            const userId = result.user_id;
            localStorage.setItem("userId", userId);
            window.location.replace("/dashboard");
        } else {
            errorMessageContainer.innerText = "Registration successful! Log in now!";
            errorMessageContainer.style.color = "green"; // Optionally change the color for success
        }
    } else {
        errorMessageContainer.innerText = result.error;
        errorMessageContainer.style.color = "#d32f2f";  // Change color to red for error messages
    }
});


document.getElementById("start-quiz-btn")?.addEventListener("click", async () => {
    const quizContainer = document.getElementById("quiz-container");
    const quizQuestionsDiv = document.getElementById("quiz-questions");
    const submitQuizButton = document.getElementById("submit-quiz-btn");

    try {
        const response = await fetch(`${baseURL}/quiz`);
        questions = await response.json();

        if (questions.length > 0) {
            quizContainer.style.display = "block";
            document.getElementById("start-quiz-btn").style.display = "none";
            submitQuizButton.style.display = "none";
            showQuestion(currentQuestionIndex);
        }
    } catch (error) {
        console.error("Error fetching quiz questions:", error);
    }
});


let currentQuestionIndex = 0;
let questions = [];
const answers = {}; // Store selected answers


// Function to show a question with a flip transition
function showQuestion(index) {
    const quizQuestionsDiv = document.getElementById("quiz-questions");
    quizQuestionsDiv.innerHTML = ""; // Clear previous question

    if (index < questions.length) {
        const q = questions[index];
        const questionElem = document.createElement("div");
        questionElem.classList.add("flip-container");
        questionElem.innerHTML = `
            <div class="flip-card">
                <div class="flip-card-front">
                    <p><strong>Q${index + 1}: ${q.question}</strong></p>
                    <ul>
                        <li><input type="radio" name="q${q.id}" value="1"> ${q.option1}</li>
                        <li><input type="radio" name="q${q.id}" value="2"> ${q.option2}</li>
                        <li><input type="radio" name="q${q.id}" value="3"> ${q.option3}</li>
                        <li><input type="radio" name="q${q.id}" value="4"> ${q.option4}</li>
                    </ul>
                </div>
            </div>
        `;

        quizQuestionsDiv.appendChild(questionElem);

        // Attach event listener to radio buttons
        document.querySelectorAll(`input[name="q${q.id}"]`).forEach((radio) => {
            radio.addEventListener("change", () => {
                answers[q.id] = radio.value; // Save answer
                currentQuestionIndex++;

                // Flip the card before showing the next question
                const flipCard = questionElem.querySelector(".flip-card");
                flipCard.classList.add("flip");

                setTimeout(() => {
                    if (currentQuestionIndex < questions.length) {
                        showQuestion(currentQuestionIndex); // Show next question after the flip
                    } else {
                        submitQuiz();
                    }
                }, 600); // Wait for the flip to finish before showing the next question
            });
        });
    }
}

// Handle quiz submission
async function submitQuiz() {

    const userId = localStorage.getItem("userId");
    if (!userId) {
        alert("User not found. Please log in again.");
        return;
    }

    try {
        const response = await fetch(`${baseURL}/submit_quiz`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, answers })
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById("quiz-result").innerText = `Quiz submitted! Your score is ${result.score}/${result.total}`;
            document.getElementById("quiz-container").style.display = "none";
            confetti({
                particleCount: 200,
                spread: 150,
                origin: { y: 0.6 }  // Confetti falls from slightly below the top
            });
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error submitting quiz:", error);
    }
}
