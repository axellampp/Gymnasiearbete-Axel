import random

### Points system instead of years in prison as it is most logical to want as many points as possible than prison years. Thus the table is reversed.
payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

# Function for simulating one round.
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]
    
### Strategies

# Always Cooperate
def strat_cooperator(lastOwnMove=None, lastOutcome=None):
    return "Cooperate"

# Always Defect
def strat_defector(lastOwnMove=None, lastOutcome=None):
    return "Defect"

# Randomize the outcome
def strat_random(lastOwnMove=None, lastOutcome=None):
    return random.choice(["Cooperate", "Defect"])

# Start with cooperating, then copy the opponents last choice.
def strat_titfortat(lastOpponentMove=None, lastOutcome=None):
    if lastOpponentMove is None:
        return "Cooperate"

    return lastOpponentMove

def strat_titfortwotats(lastOpponentMove=None, lastOutcome=None):
    if lastOpponentMove is None or len(lastOpponentMove) < 2:
        return "Cooperate"
    print(lastOpponentMove[-2])
    if lastOpponentMove[-2] == "Defect":
        return "Defect"

    return "Cooperate"

# Cooperate until the opponent has defected, then defect forever.
def strat_grudger(lastOpponentMove=None, lastOutcome=None):
    if strat_grudger.hasDefected:
        return "Defect"

    if lastOpponentMove == "Defect":
        strat_grudger.hasDefected = True
        return "Defect"
    
    return "Cooperate"    

strat_grudger.hasDefected = False

# Cooperate if the last round was mutually beneficial. Otherwise, switch strategy.
def strat_WinStayLoseShift(lastOwnMove=None, lastOutcome=None):
    
    if lastOwnMove is None: # First round
        return "Cooperate"

    if lastOutcome in [(3, 3), (1, 1)]: # Mutual outcome
        return lastOwnMove # Stick with the previous move

    if lastOutcome in [(0, 5), (5, 0)]:
        print("asdasd")
        return "Defect" if lastOwnMove == "Defect" else "Cooperate"

# Let the user be a player and choose to defect or cooperate.       
def strat_human(lastOwnMove=None, lastOutcome=None):
    choice = input("Defect or Cooperate: ")

    if choice.lower() == "defect":
        return "Defect"

    if choice.lower() == "cooperate":
        return "Cooperate"
    
    else:
        print(f"'{choice}' is invalid, try again:")

def simulate_tournament(num_rounds, A_strategy, B_strategy):
    A_score = 0
    B_score = 0

    A_last_move = None
    B_last_move = None
    A_last_outcome = None
    B_last_outcome = None

    for _ in range(num_rounds):
        A_choice = A_strategy(B_last_move, B_last_outcome)
        B_choice = B_strategy(A_last_move, A_last_outcome)

        print(f"A choice: {A_choice}")
        print(f"B choice: {B_choice}")

        outcome = simulate_round(A_choice, B_choice)

        A_score += outcome[0]
        B_score += outcome[1]

        # Update
        A_last_move = A_choice
        B_last_move = B_choice
        A_last_outcome = outcome
        B_last_outcome = (outcome[1], outcome[0])
        #print(f" A outcome: {outcome}")
        #print(f"B outcome: {(outcome[1], outcome[0])}")

        # Debug för att see val
        #print(f"Player A chose to {A_choice}")
        #print(f"Player B chose to {B_choice}")

    print(f"Player A\'s score: {A_score}")
    print(f"Player B\'s score: {B_score}")

# Funktion för simulationen. Kräver antal rundor, As strategi och Bs strategi
simulate_tournament(5, strat_human, strat_defector)