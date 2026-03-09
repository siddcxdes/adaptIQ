from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.models import (
    StartSessionRequest,
    SubmitAnswerRequest,
    QuestionResponse,
    AnswerResult,
    SessionResponse,
    StudyPlanResponse,
)
from app.adaptive import update_ability, pick_next_question
from app.ai_helper import generate_study_plan

app = FastAPI(
    title="Adaptive Diagnostic Engine",
    description="An AI-driven adaptive testing system that adjusts question difficulty based on student performance.",
    version="1.0.0",
)

db = get_database()
questions_collection = db["questions"]
sessions_collection = db["sessions"]

TOTAL_QUESTIONS = 10
STARTING_ABILITY = 0.5


def make_question_response(question):
    return QuestionResponse(
        question_id=str(question["_id"]),
        question_text=question["question_text"],
        options=question["options"],
        topic=question["topic"],
        difficulty=question["difficulty"],
    )


def get_answered_question_ids(session):
    answered_ids = []
    for response in session["responses"]:
        answered_ids.append(response["question_id"])
    return answered_ids


def get_available_questions(answered_ids):
    answered_object_ids = []
    for qid in answered_ids:
        answered_object_ids.append(ObjectId(qid))

    if len(answered_object_ids) > 0:
        available = list(questions_collection.find({"_id": {"$nin": answered_object_ids}}))
    else:
        available = list(questions_collection.find())

    return available


@app.post("/start")
def start_session(request: StartSessionRequest):
    new_session = {
        "student_name": request.student_name,
        "current_ability": STARTING_ABILITY,
        "responses": [],
        "is_finished": False,
        "total_questions": TOTAL_QUESTIONS,
        "created_at": datetime.now().isoformat(),
    }

    result = sessions_collection.insert_one(new_session)
    session_id = str(result.inserted_id)

    all_questions = list(questions_collection.find())
    first_question = pick_next_question(all_questions, STARTING_ABILITY)

    if first_question is None:
        raise HTTPException(
            status_code=500,
            detail="No questions found in database. Run seed.py first."
        )

    return {
        "session_id": session_id,
        "message": f"Test started for {request.student_name}",
        "total_questions": TOTAL_QUESTIONS,
        "current_ability": STARTING_ABILITY,
        "question": make_question_response(first_question),
    }


@app.get("/next-question/{session_id}")
def get_next_question(session_id: str):
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session["is_finished"]:
        raise HTTPException(status_code=400, detail="This test is already finished.")

    answered_ids = get_answered_question_ids(session)
    available = get_available_questions(answered_ids)

    if len(available) == 0:
        raise HTTPException(status_code=400, detail="No more questions available.")

    next_question = pick_next_question(available, session["current_ability"])

    return {
        "session_id": session_id,
        "current_ability": session["current_ability"],
        "questions_answered": len(session["responses"]),
        "total_questions": TOTAL_QUESTIONS,
        "question": make_question_response(next_question),
    }


@app.post("/submit-answer")
def submit_answer(request: SubmitAnswerRequest):
    try:
        session = sessions_collection.find_one({"_id": ObjectId(request.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session["is_finished"]:
        raise HTTPException(status_code=400, detail="This test is already finished.")

    try:
        question = questions_collection.find_one({"_id": ObjectId(request.question_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid question ID format.")

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found.")

    is_correct = request.selected_answer == question["correct_answer"]

    previous_ability = session["current_ability"]
    question_number = len(session["responses"]) + 1

    new_ability = update_ability(
        current_ability=previous_ability,
        difficulty=question["difficulty"],
        is_correct=is_correct,
        question_number=question_number,
    )

    response_record = {
        "question_id": request.question_id,
        "selected_answer": request.selected_answer,
        "correct_answer": question["correct_answer"],
        "is_correct": is_correct,
        "difficulty": question["difficulty"],
        "topic": question["topic"],
    }

    is_finished = question_number >= TOTAL_QUESTIONS

    sessions_collection.update_one(
        {"_id": ObjectId(request.session_id)},
        {
            "$set": {
                "current_ability": new_ability,
                "is_finished": is_finished,
            },
            "$push": {
                "responses": response_record,
            },
        },
    )

    return AnswerResult(
        is_correct=is_correct,
        correct_answer=question["correct_answer"],
        previous_ability=previous_ability,
        new_ability=new_ability,
        questions_answered=question_number,
        total_questions=TOTAL_QUESTIONS,
        is_finished=is_finished,
    )


@app.get("/session/{session_id}")
def get_session(session_id: str):
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    return SessionResponse(
        session_id=str(session["_id"]),
        student_name=session["student_name"],
        current_ability=session["current_ability"],
        questions_answered=len(session["responses"]),
        total_questions=session["total_questions"],
        is_finished=session["is_finished"],
    )


@app.get("/study-plan/{session_id}")
def get_study_plan(session_id: str):
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID format.")

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    if not session["is_finished"]:
        raise HTTPException(
            status_code=400,
            detail="Test is not finished yet. Answer all questions first."
        )

    weak_topics = []
    total_correct = 0

    for response in session["responses"]:
        if response["is_correct"]:
            total_correct += 1
        else:
            if response["topic"] not in weak_topics:
                weak_topics.append(response["topic"])

    study_plan_text = generate_study_plan(
        student_name=session["student_name"],
        final_ability=session["current_ability"],
        total_correct=total_correct,
        total_questions=session["total_questions"],
        weak_topics=weak_topics,
        responses_detail=session["responses"],
    )

    return StudyPlanResponse(
        student_name=session["student_name"],
        final_ability=session["current_ability"],
        total_correct=total_correct,
        total_questions=session["total_questions"],
        weak_topics=weak_topics,
        study_plan=study_plan_text,
    )


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
