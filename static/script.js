var sessionId = "";
var currentQuestion = null;
var questionsAnswered = 0;
var totalQuestions = 10;
var correctAnswers = 0;


function startTest() {
    var nameInput = document.getElementById("student-name");
    var studentName = nameInput.value.trim();

    if (studentName === "") {
        nameInput.style.borderColor = "#c44040";
        nameInput.placeholder = "Please enter your name first...";
        return;
    }

    var startBtn = document.getElementById("start-btn");
    startBtn.disabled = true;
    startBtn.textContent = "Starting...";

    fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_name: studentName })
    })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Failed to start test. Is the database seeded?");
            }
            return response.json();
        })
        .then(function (data) {
            sessionId = data.session_id;
            totalQuestions = data.total_questions;
            questionsAnswered = 0;
            correctAnswers = 0;

            currentQuestion = data.question;
            showQuizScreen();
            displayQuestion(currentQuestion);
        })
        .catch(function (error) {
            alert("Error: " + error.message);
            startBtn.disabled = false;
            startBtn.textContent = "Start Assessment";
        });
}


function showQuizScreen() {
    document.getElementById("welcome-screen").classList.remove("active");
    document.getElementById("quiz-screen").classList.add("active");
}


function displayQuestion(question) {
    document.getElementById("question-text").textContent = question.question_text;
    document.getElementById("question-topic").textContent = question.topic;
    document.getElementById("question-difficulty").textContent = "Difficulty: " + question.difficulty.toFixed(2);
    document.getElementById("question-counter").textContent = (questionsAnswered + 1) + " / " + totalQuestions;

    var progressPercent = (questionsAnswered / totalQuestions) * 100;
    document.getElementById("progress-bar").style.width = progressPercent + "%";

    var optionsContainer = document.getElementById("options-container");
    optionsContainer.innerHTML = "";

    for (var i = 0; i < question.options.length; i++) {
        var button = document.createElement("button");
        button.className = "option-btn";
        button.textContent = question.options[i];
        button.setAttribute("data-answer", question.options[i]);
        button.onclick = function () {
            selectOption(this);
        };
        optionsContainer.appendChild(button);
    }

    hideFeedback();
}


function selectOption(clickedButton) {
    var selectedAnswer = clickedButton.getAttribute("data-answer");

    var allButtons = document.querySelectorAll(".option-btn");
    for (var i = 0; i < allButtons.length; i++) {
        allButtons[i].disabled = true;
    }

    clickedButton.classList.add("selected");

    fetch("/submit-answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId,
            question_id: currentQuestion.question_id,
            selected_answer: selectedAnswer
        })
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (result) {
            questionsAnswered = result.questions_answered;

            if (result.is_correct) {
                correctAnswers++;
            }

            document.getElementById("ability-score").textContent = result.new_ability.toFixed(2);

            showAnswerFeedback(result, selectedAnswer, clickedButton);
            showFeedbackPopup(result);
        })
        .catch(function (error) {
            alert("Error submitting answer: " + error.message);
        });
}


function showAnswerFeedback(result, selectedAnswer, clickedButton) {
    var allButtons = document.querySelectorAll(".option-btn");
    for (var i = 0; i < allButtons.length; i++) {
        var btn = allButtons[i];
        if (btn.getAttribute("data-answer") === result.correct_answer) {
            btn.classList.add("correct");
        }
    }

    if (!result.is_correct) {
        clickedButton.classList.remove("selected");
        clickedButton.classList.add("wrong");
    }
}


function showFeedbackPopup(result) {
    var popup = document.getElementById("feedback-popup");
    var icon = document.getElementById("feedback-icon");
    var text = document.getElementById("feedback-text");
    var detail = document.getElementById("feedback-detail");

    if (result.is_correct) {
        icon.textContent = "Correct";
        text.textContent = "Nice work!";
        text.className = "feedback-text correct";
        detail.textContent = "Ability: " + result.previous_ability.toFixed(2) + " → " + result.new_ability.toFixed(2);
    } else {
        icon.textContent = "Incorrect";
        text.textContent = "Not quite.";
        text.className = "feedback-text wrong";
        detail.textContent = "Correct answer: " + result.correct_answer + " | Ability: " + result.previous_ability.toFixed(2) + " → " + result.new_ability.toFixed(2);
    }

    if (result.is_finished) {
        var nextBtn = popup.querySelector(".btn-secondary");
        nextBtn.textContent = "View Results";
        nextBtn.onclick = function () {
            showResultsScreen(result);
        };
    }

    popup.classList.remove("hidden");
    popup.classList.add("visible");
}


function hideFeedback() {
    var popup = document.getElementById("feedback-popup");
    popup.classList.remove("visible");
    popup.classList.add("hidden");
}


function loadNextQuestion() {
    fetch("/next-question/" + sessionId)
        .then(function (response) {
            if (!response.ok) {
                throw new Error("No more questions");
            }
            return response.json();
        })
        .then(function (data) {
            currentQuestion = data.question;
            displayQuestion(currentQuestion);
        })
        .catch(function (error) {
            alert("Error loading next question: " + error.message);
        });
}


function showResultsScreen() {
    document.getElementById("quiz-screen").classList.remove("active");
    document.getElementById("results-screen").classList.add("active");

    hideFeedback();

    fetch("/session/" + sessionId)
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            document.getElementById("final-score").textContent = session.current_ability.toFixed(2);
            document.getElementById("correct-count").textContent = correctAnswers;
            document.getElementById("wrong-count").textContent = totalQuestions - correctAnswers;
            document.getElementById("total-count").textContent = totalQuestions;

            document.getElementById("progress-bar").style.width = "100%";
        });

    fetchStudyPlan();
}


function fetchStudyPlan() {
    var planContainer = document.getElementById("study-plan-content");

    planContainer.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><p>Generating your personalized study plan...</p></div>';

    fetch("/study-plan/" + sessionId)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            planContainer.textContent = data.study_plan;

            var weakTopicsList = document.getElementById("weak-topics-list");
            weakTopicsList.innerHTML = "";

            if (data.weak_topics.length === 0) {
                document.getElementById("weak-topics-section").style.display = "none";
            } else {
                for (var i = 0; i < data.weak_topics.length; i++) {
                    var tag = document.createElement("span");
                    tag.className = "topic-tag";
                    tag.textContent = data.weak_topics[i];
                    weakTopicsList.appendChild(tag);
                }
            }
        })
        .catch(function (error) {
            planContainer.textContent = "Could not generate study plan. Error: " + error.message;
        });
}


function restartTest() {
    document.getElementById("results-screen").classList.remove("active");
    document.getElementById("welcome-screen").classList.add("active");

    sessionId = "";
    currentQuestion = null;
    questionsAnswered = 0;
    correctAnswers = 0;

    var startBtn = document.getElementById("start-btn");
    startBtn.disabled = false;
    startBtn.textContent = "Start Assessment";

    document.getElementById("student-name").value = "";
    document.getElementById("student-name").style.borderColor = "#e8e6e1";

    var popup = document.getElementById("feedback-popup");
    var nextBtn = popup.querySelector(".btn-secondary");
    nextBtn.textContent = "Next Question";
    nextBtn.onclick = function () {
        loadNextQuestion();
    };
}
