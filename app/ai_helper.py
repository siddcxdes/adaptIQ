import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def generate_study_plan(student_name, final_ability, total_correct, total_questions, weak_topics, responses_detail):
    missed_summary = ""
    for response in responses_detail:
        if not response["is_correct"]:
            missed_summary += f"- Missed a {response['topic']} question (difficulty: {response['difficulty']})\n"

    prompt = f"""You are an educational tutor. A student named {student_name} just completed an adaptive diagnostic test.

Here are their results:
- Final ability score: {final_ability:.2f} out of 1.00
- Correct answers: {total_correct} out of {total_questions}
- Weak topics: {', '.join(weak_topics) if weak_topics else 'None identified'}

Questions they got wrong:
{missed_summary if missed_summary else 'They got all questions correct!'}

Based on these results, create a personalized 3-step study plan. Each step should:
1. Focus on a specific weakness
2. Suggest a concrete action (like practice problems, watching a video, reading a chapter)
3. Be encouraging and motivating

Keep it concise and practical. Format it as 3 numbered steps."""

    try:
        api_url = f"{OLLAMA_URL}/api/generate"

        request_body = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(api_url, json=request_body, timeout=60)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Could not generate study plan.")
        else:
            return create_fallback_plan(student_name, weak_topics, final_ability)

    except requests.exceptions.ConnectionError:
        return create_fallback_plan(student_name, weak_topics, final_ability)

    except Exception as error:
        return create_fallback_plan(student_name, weak_topics, final_ability)


def create_fallback_plan(student_name, weak_topics, final_ability):
    plan = f"Study Plan for {student_name} (Ability Score: {final_ability:.2f})\n\n"

    if len(weak_topics) == 0:
        plan += "Great job! You performed well across all topics.\n\n"
        plan += "1. Review advanced problems in all topics to push your skills further.\n"
        plan += "2. Try timed practice tests to improve your speed.\n"
        plan += "3. Teach the concepts to someone else - teaching is the best way to learn.\n"
    else:
        plan += f"You need to focus on: {', '.join(weak_topics)}\n\n"
        plan += f"1. Start with the basics of {weak_topics[0]}. "
        plan += "Go back to fundamentals and practice 10-15 simple problems.\n"

        if len(weak_topics) > 1:
            plan += f"2. Move on to {weak_topics[1]}. "
            plan += "Watch tutorial videos and take notes on key formulas.\n"
        else:
            plan += "2. Once basics are solid, try medium-difficulty problems. "
            plan += "Time yourself to build confidence.\n"

        plan += "3. Take another practice test in a week to measure your improvement.\n"

    return plan
