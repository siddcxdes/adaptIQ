# AdaptIQ – Adaptive Diagnostic Testing Engine

## Source Code
GitHub Repository:  
https://github.com/siddcxdes/adaptIQ

---

#THIS PROJECT USES LOCAL LLM (OLLAMA)

# Project Overview

AdaptIQ is a small adaptive testing system that estimates a student's skill level while they take the test.

Instead of giving the same questions to everyone, the system **changes the difficulty of the next question based on the student's previous answers**.

If the student answers correctly, the next question becomes harder.  
If they answer incorrectly, the next question becomes easier.

The backend is built using **FastAPI**, questions are stored in **MongoDB**, and an optional **local LLM (Ollama)** can generate a study plan after the test.

---

# How the Adaptive Algorithm Works

The system uses a simplified version of **Item Response Theory (IRT)** — a method used in real exams like the **GRE and GMAT**.

### Step 1: Starting Ability

Every student starts with an **ability score of 0.5**.  
This represents the middle of the difficulty range.

---

### Step 2: After Each Answer

We estimate the probability that the student should have answered the question correctly using this formula:

```
P(correct) = 1 / (1 + e^(-1.7 * (ability - difficulty)))
```

Then we update the student's ability score.

If the answer is correct:

```
ability = ability + K * (1 - P)
```

If the answer is wrong:

```
ability = ability - K * P
```

Where **K** is the step size (learning rate).  
It starts at **0.4** and slowly decreases as more questions are answered to keep the score stable.

---

### Step 3: Choosing the Next Question

The system picks the question whose **difficulty is closest to the student's current ability score**.

This allows the test to quickly find the student's real level.

---

### Step 4: AI Study Plan

After the student answers **10 questions**, the system summarizes their performance.

This information is sent to a **local LLM using Ollama**, which generates a **3-step study plan** suggesting what the student should improve.

If Ollama is not running, the system returns a basic rule-based study plan instead.

---

# How to Run the Project

## Prerequisites

Make sure the following are installed:

- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- Ollama (optional)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/adaptiq
cd adaptiq
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` if your MongoDB connection string is different.

---

## 5. Run the Project

A single script handles everything — it seeds the database (if empty) and starts the server:

```bash
python run.py
```

This will:
- Check if questions exist in the database
- Seed 25 GRE-style questions if the database is empty
- Start the server on port 8000

Open the app in your browser:

```
http://localhost:8000
```

---

## 6. Optional: Start Ollama

If you want AI-generated study plans:

```bash
ollama run llama3.2
```

---

# API Documentation

FastAPI automatically generates API docs at:

```
http://localhost:8000/docs
```

### Available Endpoints

| Method | Endpoint | Description |
|------|------|------|
| POST | `/start` | Start a new test session |
| GET | `/next-question/{session_id}` | Get the next adaptive question |
| POST | `/submit-answer` | Submit an answer |
| GET | `/session/{session_id}` | Get current test session status |
| GET | `/study-plan/{session_id}` | Generate a study plan after the test |

---

# Project Structure

```
assignment/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── adaptive.py
│   └── ai_helper.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── seed.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# Tech Stack

Backend  
- Python
- FastAPI

Database  
- MongoDB

AI  
- Ollama (local LLM)

Frontend  
- HTML
- CSS
- JavaScript

Algorithm  
- Simplified **1-Parameter Logistic IRT Model**

---

# AI Log

### How AI Helped During Development

AI tools like **Cursor and ChatGPT** helped speed up development in several areas:

- Generating initial FastAPI route structures
- Writing Pydantic models
- Setting up MongoDB queries
- Creating sample GRE-style questions
- Helping structure the project folders

This saved time on repetitive boilerplate code.

---

### Things AI Could Not Solve

Some parts still required manual thinking and experimentation:

**1. Tuning the step size (K)**  
The ability update step size needed testing to avoid unstable ability scores.

**2. Question difficulty calibration**  
AI generated questions, but assigning realistic difficulty values still required manual judgment.

**3. Prompt design for the study plan**  
The Ollama prompt needed multiple adjustments to make the generated study plan specific and useful instead of generic.

---

# Summary

AdaptIQ demonstrates how **adaptive testing systems work** using:

- IRT-based ability estimation  
- Dynamic question selection  
- Optional AI-generated study plans  

It is a lightweight example of how modern learning platforms can personalize assessments for each student.