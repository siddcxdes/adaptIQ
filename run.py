import subprocess
import sys

from app.database import get_database

db = get_database()
questions_collection = db["questions"]

question_count = questions_collection.count_documents({})

if question_count == 0:
    print("No questions found in database. Seeding now...")
    from seed import seed_database
    seed_database()
    print()
else:
    print(f"Database already has {question_count} questions. Skipping seed.")

print("Starting server on http://localhost:8000")
print()

subprocess.run([
    sys.executable, "-m", "uvicorn",
    "app.main:app",
    "--reload",
    "--port", "8000"
])
