import math


def calculate_probability(ability, difficulty):
    exponent = -1.7 * (ability - difficulty)
    probability = 1.0 / (1.0 + math.exp(exponent))
    return probability


def update_ability(current_ability, difficulty, is_correct, question_number):
    step_size = 0.4 / (1 + 0.1 * question_number)

    probability = calculate_probability(current_ability, difficulty)

    if is_correct:
        new_ability = current_ability + step_size * (1 - probability)
    else:
        new_ability = current_ability - step_size * probability

    if new_ability > 1.0:
        new_ability = 1.0
    if new_ability < 0.0:
        new_ability = 0.0

    new_ability = round(new_ability, 4)

    return new_ability


def pick_next_question(available_questions, current_ability):
    if len(available_questions) == 0:
        return None

    best_question = None
    smallest_gap = 999

    for question in available_questions:
        gap = abs(question["difficulty"] - current_ability)

        if gap < smallest_gap:
            smallest_gap = gap
            best_question = question

    return best_question
