from pydantic import BaseModel
from typing import List, Optional


class StartSessionRequest(BaseModel):
    student_name: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_answer: str


class QuestionResponse(BaseModel):
    question_id: str
    question_text: str
    options: List[str]
    topic: str
    difficulty: float


class AnswerResult(BaseModel):
    is_correct: bool
    correct_answer: str
    previous_ability: float
    new_ability: float
    questions_answered: int
    total_questions: int
    is_finished: bool


class SessionResponse(BaseModel):
    session_id: str
    student_name: str
    current_ability: float
    questions_answered: int
    total_questions: int
    is_finished: bool


class StudyPlanResponse(BaseModel):
    student_name: str
    final_ability: float
    total_correct: int
    total_questions: int
    weak_topics: List[str]
    study_plan: str
