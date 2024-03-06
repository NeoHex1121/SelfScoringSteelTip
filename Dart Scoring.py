import random

def get_player_input(player_name, dart_number):
    while True:
        dart_input = input(f"{player_name}, enter the score for Dart {dart_number} (or type 'Next' to move on): ")
        if dart_input.lower() == "next":
            return 0
        try:
            dart_score = int(dart_input)
            if 0 <= dart_score <= 60:
                return dart_score
            else:
                print("Invalid input. Please enter a score between 0 and 60 or type 'Next' to move on.")
        except ValueError:
            print("Invalid input. Please enter a valid number or type 'Next' to move on.")

def throw_dart():
    return random.randint(1, 20) * random.choice([1, -1])  # Random score between 1 and 20 with a random sign

def update_score(player, points):
    player["score"] -= points
    if player["score"] < 0:
        player["score"] = 0

def check_winner(player):
    return player["score"] == 0

def print_scores(player1, player2):
    print(f"\nCurrent Scores - Player 1: {player1['score']} | Player 2: {player2['score']}")

def player_turn(player):
    initial_score = player['score']
    total_points = 0

    print(f"\n{player['name']}'s Turn:")
    for dart_number in range(1, 4):
        dart_score = get_player_input(player['name'], dart_number)
        if dart_score == 0:
            print(f"{player['name']}, Dart {dart_number}: Next")
        else:
            print(f"{player['name']}, Dart {dart_number}: {dart_score}")
            total_points += dart_score

        # Check for bust
        if player['score'] - total_points < 0:
            print(f"{player['name']} busts! Resetting score for this turn.")
            player['score'] = initial_score
            return 0

    return total_points

def main():
    players = [{"score": 501, "name": "Player 1"}, {"score": 501, "name": "Player 2"}]

    print("Welcome to the 501 Dart Game!")

    current_player = 0

    while True:
        print_scores(players[0], players[1])

        total_points = player_turn(players[current_player])
        update_score(players[current_player], total_points)

        if check_winner(players[current_player]):
            print(f"\nCongratulations, {players[current_player]['name']} wins!")
            break

        current_player = (current_player + 1) % 2  # Switch players

if __name__ == "__main__":
    main()
