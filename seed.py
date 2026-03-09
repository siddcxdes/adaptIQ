from app.database import get_database

db = get_database()
questions_collection = db["questions"]

questions = [
    {
        "question_text": "Solve for x: x + 7 = 12",
        "options": ["3", "4", "5", "7"],
        "correct_answer": "5",
        "difficulty": 0.15,
        "topic": "Algebra",
        "tags": ["linear-equations", "basic"]
    },
    {
        "question_text": "What is the value of x if 2x - 4 = 10?",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "7",
        "difficulty": 0.25,
        "topic": "Algebra",
        "tags": ["linear-equations", "basic"]
    },
    {
        "question_text": "If 3x + 2 = 17, what is x?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "5",
        "difficulty": 0.35,
        "topic": "Algebra",
        "tags": ["linear-equations"]
    },
    {
        "question_text": "Solve: x^2 - 9 = 0. What are the values of x?",
        "options": ["3 and -3", "9 and -9", "3 only", "0 and 9"],
        "correct_answer": "3 and -3",
        "difficulty": 0.55,
        "topic": "Algebra",
        "tags": ["quadratic", "factoring"]
    },
    {
        "question_text": "If f(x) = 2x^2 + 3x - 5, what is f(2)?",
        "options": ["7", "9", "11", "13"],
        "correct_answer": "9",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["functions", "evaluation"]
    },
    {
        "question_text": "What is 15% of 200?",
        "options": ["20", "25", "30", "35"],
        "correct_answer": "30",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["percentages", "basic"]
    },
    {
        "question_text": "A shirt costs $80 and is on sale for 25% off. What is the sale price?",
        "options": ["$55", "$60", "$65", "$70"],
        "correct_answer": "$60",
        "difficulty": 0.35,
        "topic": "Arithmetic",
        "tags": ["percentages", "word-problem"]
    },
    {
        "question_text": "What is the ratio of 45 to 60 in simplest form?",
        "options": ["3:4", "4:5", "2:3", "9:12"],
        "correct_answer": "3:4",
        "difficulty": 0.4,
        "topic": "Arithmetic",
        "tags": ["ratios"]
    },
    {
        "question_text": "If a car travels 150 miles in 2.5 hours, what is its average speed?",
        "options": ["50 mph", "55 mph", "60 mph", "65 mph"],
        "correct_answer": "60 mph",
        "difficulty": 0.45,
        "topic": "Arithmetic",
        "tags": ["rate", "word-problem"]
    },
    {
        "question_text": "A number increased by 20% gives 96. What is the original number?",
        "options": ["72", "76", "80", "84"],
        "correct_answer": "80",
        "difficulty": 0.6,
        "topic": "Arithmetic",
        "tags": ["percentages", "reverse"]
    },
    {
        "question_text": "What is the area of a rectangle with length 8 and width 5?",
        "options": ["30", "35", "40", "45"],
        "correct_answer": "40",
        "difficulty": 0.15,
        "topic": "Geometry",
        "tags": ["area", "rectangle"]
    },
    {
        "question_text": "What is the perimeter of a square with side length 12?",
        "options": ["36", "44", "48", "52"],
        "correct_answer": "48",
        "difficulty": 0.2,
        "topic": "Geometry",
        "tags": ["perimeter", "square"]
    },
    {
        "question_text": "A triangle has angles of 50 and 60 degrees. What is the third angle?",
        "options": ["60", "65", "70", "80"],
        "correct_answer": "70",
        "difficulty": 0.3,
        "topic": "Geometry",
        "tags": ["angles", "triangle"]
    },
    {
        "question_text": "What is the area of a circle with radius 7? (Use pi = 22/7)",
        "options": ["144", "150", "154", "160"],
        "correct_answer": "154",
        "difficulty": 0.5,
        "topic": "Geometry",
        "tags": ["area", "circle"]
    },
    {
        "question_text": "In a right triangle, if one leg is 6 and the hypotenuse is 10, what is the other leg?",
        "options": ["6", "7", "8", "9"],
        "correct_answer": "8",
        "difficulty": 0.65,
        "topic": "Geometry",
        "tags": ["pythagorean", "right-triangle"]
    },
    {
        "question_text": "Choose the synonym of 'happy':",
        "options": ["Sad", "Joyful", "Angry", "Tired"],
        "correct_answer": "Joyful",
        "difficulty": 0.1,
        "topic": "Vocabulary",
        "tags": ["synonyms", "basic"]
    },
    {
        "question_text": "What is the antonym of 'abundant'?",
        "options": ["Plentiful", "Scarce", "Excess", "Generous"],
        "correct_answer": "Scarce",
        "difficulty": 0.3,
        "topic": "Vocabulary",
        "tags": ["antonyms"]
    },
    {
        "question_text": "Choose the word that best completes: 'The professor's lecture was so ___ that several students fell asleep.'",
        "options": ["Riveting", "Tedious", "Animated", "Concise"],
        "correct_answer": "Tedious",
        "difficulty": 0.45,
        "topic": "Vocabulary",
        "tags": ["context-clues", "sentence-completion"]
    },
    {
        "question_text": "The word 'ubiquitous' most nearly means:",
        "options": ["Rare", "Unique", "Everywhere", "Invisible"],
        "correct_answer": "Everywhere",
        "difficulty": 0.65,
        "topic": "Vocabulary",
        "tags": ["definitions", "advanced"]
    },
    {
        "question_text": "Choose the word most opposite in meaning to 'ephemeral':",
        "options": ["Fleeting", "Permanent", "Brief", "Momentary"],
        "correct_answer": "Permanent",
        "difficulty": 0.8,
        "topic": "Vocabulary",
        "tags": ["antonyms", "gre-level"]
    },
    {
        "question_text": "A passage states: 'The industrial revolution transformed society from agrarian to urban.' What does 'agrarian' refer to?",
        "options": ["City-based", "Farm-based", "Trade-based", "Technology-based"],
        "correct_answer": "Farm-based",
        "difficulty": 0.35,
        "topic": "Reading Comprehension",
        "tags": ["vocabulary-in-context"]
    },
    {
        "question_text": "If an author writes 'The evidence is merely circumstantial,' what is the author implying?",
        "options": [
            "The evidence is very strong",
            "The evidence is indirect and not conclusive",
            "The evidence has been fabricated",
            "The evidence supports the conclusion perfectly"
        ],
        "correct_answer": "The evidence is indirect and not conclusive",
        "difficulty": 0.55,
        "topic": "Reading Comprehension",
        "tags": ["inference", "critical-reading"]
    },
    {
        "question_text": "An argument states: 'All mammals are warm-blooded. Whales are mammals. Therefore, whales are warm-blooded.' This is an example of:",
        "options": ["Inductive reasoning", "Deductive reasoning", "Analogy", "Fallacy"],
        "correct_answer": "Deductive reasoning",
        "difficulty": 0.7,
        "topic": "Reading Comprehension",
        "tags": ["logic", "reasoning"]
    },
    {
        "question_text": "Which rhetorical device uses deliberate exaggeration for emphasis?",
        "options": ["Metaphor", "Hyperbole", "Irony", "Alliteration"],
        "correct_answer": "Hyperbole",
        "difficulty": 0.75,
        "topic": "Reading Comprehension",
        "tags": ["rhetoric", "literary-devices"]
    },
    {
        "question_text": "In the phrase 'the author's tone is sardonic,' what does sardonic mean?",
        "options": ["Cheerful", "Mocking and cynical", "Neutral", "Sympathetic"],
        "correct_answer": "Mocking and cynical",
        "difficulty": 0.85,
        "topic": "Reading Comprehension",
        "tags": ["tone", "vocabulary", "gre-level"]
    },
]


def seed_database():
    deleted = questions_collection.delete_many({})
    print(f"Cleared {deleted.deleted_count} old questions.")

    result = questions_collection.insert_many(questions)
    print(f"Inserted {len(result.inserted_ids)} new questions.")
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
