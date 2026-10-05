import random
import time

SCORE_FILE = "maze_scores.txt"


MAZES = {
    "easy": [
        list("##########"),
        list("#P     #E#"),
        list("#####  # #"),
        list("#   #    #"),
        list("# # ######"),
        list("# #      #"),
        list("# ###### #"),
        list("#        #"),
        list("##########"),
        list("##########")
    ],

    "medium": [
        list("##########"),
        list("#P     #E#"),
        list("# ### ## #"),
        list("#   #    #"),
        list("### ### ##"),
        list("#     #  #"),
        list("# ### ## #"),
        list("#        #"),
        list("##########"),
        list("##########")
    ],

    "hard": [
        list("############"),
        list("#P   #     #"),
        list("### ### ###"),
        list("#     #   E#"),
        list("# ### ### ##"),
        list("# #       ##"),
        list("# # ####   #"),
        list("#   #      #"),
        list("############"),
        list("############"),
        list("############"),
        list("############")
    ]
}


def display_maze(maze):
    print("\n" + "=" * 40)
    print("             MAZE")
    print("=" * 40)

    for row in maze:
        print(" ".join(row))

    print("=" * 40)


def find_player(maze):
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "P":
                return r, c


def place_coins(maze, number):
    empty = []

    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == " ":
                empty.append((r, c))

    for r, c in random.sample(empty, min(number, len(empty))):
        maze[r][c] = "*"


def save_score(score, moves, difficulty):
    with open(SCORE_FILE, "a") as file:
        file.write(
            f"{difficulty.upper()} | "
            f"Score: {score} | Moves: {moves}\n"
        )


def show_scores():
    print("\n" + "=" * 40)
    print("             SCORE HISTORY")
    print("=" * 40)

    try:
        with open(SCORE_FILE, "r") as file:
            data = file.read()

            if data:
                print(data)
            else:
                print("No scores yet.")

    except FileNotFoundError:
        print("No scores yet.")


def play_game(difficulty):
    maze = [row[:] for row in MAZES[difficulty]]

    place_coins(maze, 3)

    # Restore player and exit because coins are random
    player_r, player_c = find_player(maze)

    moves = 0
    coins = 0

    start_time = time.time()

    while True:

        display_maze(maze)

        print("Moves:", moves)
        print("Coins:", coins)
        print("Controls: W = Up | S = Down | A = Left | D = Right")
        print("Q = Quit")

        move = input("Your move: ").lower()

        if move == "q":
            print("You left the maze.")
            return

        if move not in ["w", "a", "s", "d"]:
            print("Invalid move!")
            continue

        new_r = player_r
        new_c = player_c

        if move == "w":
            new_r -= 1
        elif move == "s":
            new_r += 1
        elif move == "a":
            new_c -= 1
        elif move == "d":
            new_c += 1

        # Check boundaries
        if (new_r < 0 or new_r >= len(maze) or
                new_c < 0 or new_c >= len(maze[0])):

            print("You cannot go there!")
            continue

        target = maze[new_r][new_c]

        # Wall
        if target == "#":
            print("You hit a wall!")
            continue

        moves += 1

        # Coin
        if target == "*":
            coins += 1
            print("⭐ You collected a coin!")

        # Exit
        if target == "E":
            elapsed = round(time.time() - start_time, 2)

            score = max(
                1000 - moves * 10 - int(elapsed) + coins * 100,
                0
            )

            maze[player_r][player_c] = " "
            maze[new_r][new_c] = "P"

            display_maze(maze)

            print("\n🎉 YOU ESCAPED!")
            print("Moves :", moves)
            print("Time  :", elapsed, "seconds")
            print("Coins :", coins)
            print("Score :", score)

            save_score(score, moves, difficulty)
            return

        # Move player
        maze[player_r][player_c] = " "
        maze[new_r][new_c] = "P"

        player_r = new_r
        player_c = new_c


def instructions():
    print("\n" + "=" * 40)
    print("          HOW TO PLAY")
    print("=" * 40)

    print("""
P = Player
# = Wall
E = Exit
* = Coin

Reach E to escape the maze.

W -> Up
S -> Down
A -> Left
D -> Right

Collect coins for bonus points.
Fewer moves and less time = higher score.
""")


def main():
    while True:

        print("\n" + "=" * 40)
        print("          🧩 MAZE ESCAPE GAME")
        print("=" * 40)

        print("1. Play Game")
        print("2. Instructions")
        print("3. Score History")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":

            print("\nChoose difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")

            level = input("Enter choice: ")

            if level == "1":
                play_game("easy")
            elif level == "2":
                play_game("medium")
            elif level == "3":
                play_game("hard")
            else:
                print("Invalid difficulty.")

        elif choice == "2":
            instructions()

        elif choice == "3":
            show_scores()

        elif choice == "4":
            print("\nThanks for playing!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
