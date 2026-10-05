import json
import random
from datetime import datetime

QUESTION_FILE = "questions.json"
RESULT_FILE = "results.txt"


def load_questions():
    try:
        with open(QUESTION_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        questions = [
            {
                "question": "What is the capital of India?",
                "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
                "answer": 2,
                "difficulty": "easy"
            },
            {
                "question": "Which data structure follows FIFO?",
                "options": ["Stack", "Queue", "Tree", "Graph"],
                "answer": 2,
                "difficulty": "medium"
            },
            {
                "question": "What is the time complexity of binary search?",
                "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                "answer": 2,
                "difficulty": "hard"
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["func", "define", "def", "function"],
                "answer": 3,
                "difficulty": "easy"
            },
            {
                "question": "Which file format is commonly used for structured data?",
                "options": ["JSON", "MP3", "PNG", "EXE"],
                "answer": 1,
                "difficulty": "easy"
            }
        ]

        save_questions(questions)
        return questions


def save_questions(questions):
    with open(QUESTION_FILE, "w") as file:
        json.dump(questions, file, indent=4)


def start_quiz(questions):
    print("\n" + "=" * 45)
    print("             START QUIZ")
    print("=" * 45)

    difficulty = input(
        "Choose difficulty (easy/medium/hard): "
    ).lower()

    selected = [
        q for q in questions
        if q["difficulty"] == difficulty
    ]

    if not selected:
        print("No questions available for this difficulty.")
        return

    random.shuffle(selected)

    try:
        number = int(input("Number of questions: "))
    except ValueError:
        print("Invalid number.")
        return

    selected = selected[:min(number, len(selected))]

    score = 0

    for i, q in enumerate(selected, 1):
        print("\nQuestion", i)
        print(q["question"])

        for j, option in enumerate(q["options"], 1):
            print(f"{j}. {option}")

        try:
            answer = int(input("Your answer: "))
        except ValueError:
            print("Invalid answer. Moving on.")
            continue

        if answer == q["answer"]:
            print("✓ Correct!")
            score += 1
        else:
            print("✗ Wrong!")
            print("Correct answer:", q["options"][q["answer"] - 1])

    percentage = (score / len(selected)) * 100

    print("\n" + "=" * 45)
    print("                 RESULT")
    print("=" * 45)
    print("Score      :", score, "/", len(selected))
    print("Percentage :", round(percentage, 2), "%")

    if percentage >= 80:
        print("Excellent performance!")
    elif percentage >= 50:
        print("Good job! Keep improving.")
    else:
        print("Keep practising!")

    save_result(score, len(selected), percentage)


def save_result(score, total, percentage):
    with open(RESULT_FILE, "a") as file:
        time = datetime.now().strftime("%d-%m-%Y %H:%M")
        file.write(
            f"{time} | Score: {score}/{total} | "
            f"Percentage: {percentage:.2f}%\n"
        )


def add_question(questions):
    print("\n" + "=" * 45)
    print("              ADD QUESTION")
    print("=" * 45)

    question = input("Question: ")

    options = []
    for i in range(4):
        options.append(input(f"Option {i + 1}: "))

    try:
        answer = int(input("Correct option (1-4): "))
        if answer not in range(1, 5):
            raise ValueError
    except ValueError:
        print("Invalid answer.")
        return

    difficulty = input(
        "Difficulty (easy/medium/hard): "
    ).lower()

    if difficulty not in ["easy", "medium", "hard"]:
        print("Invalid difficulty.")
        return

    questions.append({
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": difficulty
    })

    save_questions(questions)
    print("Question saved successfully!")


def view_history():
    print("\n" + "=" * 45)
    print("              SCORE HISTORY")
    print("=" * 45)

    try:
        with open(RESULT_FILE, "r") as file:
            data = file.read()

            if data:
                print(data)
            else:
                print("No results yet.")

    except FileNotFoundError:
        print("No results yet.")


def main():
    questions = load_questions()

    while True:
        print("\n" + "=" * 45)
        print("          SMART QUIZ GENERATOR")
        print("=" * 45)
        print("1. Start Quiz")
        print("2. Add Question")
        print("3. View Score History")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            start_quiz(questions)

        elif choice == "2":
            add_question(questions)

        elif choice == "3":
            view_history()

        elif choice == "4":
            print("\nThank you for using Smart Quiz Generator!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
