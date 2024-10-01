import random

### Poängsystem istället för belöning i fängelsetid då det är mest logiskt att vilja ha så mycket poäng som möjligt än fängelseår. Därmed är tabellen omvänd så logiken är lika.

payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

# Funktion för en runda
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]
    
### Strategier

# alltid Cooperate
def strat_cooperator(_):
    return "Cooperate"

# alltid Defect
def strat_defector(_):
    return "Defect"

# Slumpa
def strat_random(_):
    return random.choice(["Cooperate", "Defect"])

# Börja med Cooperate, sedan kopiera motståndarens val.
def strat_titfortat(lastOpponentMove=None):

    if lastOpponentMove is None:
        return "Cooperate"

    return lastOpponentMove

# Cooperate tills motståndaren har valt defekt, sen defekta alltid
def strat_grudger(lastOpponentMove=None):
    if strat_grudger.hasDefected:
        return "Defect"

    if lastOpponentMove == "Defect":
        strat_grudger.hasDefected = True
        return "Defect"
    
    return "Cooperate"    

strat_grudger.hasDefected = False

def WinStayLoseShift():



    pass


def simulate_tournament(num_rounds, A_strategy, B_strategy):
    A_score = 0
    B_score = 0

    last_move_A = None
    last_move_B = None

    for _ in range(num_rounds):
        A_choice = A_strategy(last_move_B)
        B_choice = B_strategy(last_move_A)

        outcome = simulate_round(A_choice, B_choice)

        A_score += outcome[0]
        B_score += outcome[1]

        last_move_A = A_choice
        last_move_B = B_choice
        
        # Debug för att see val
        # print(f"Player A chose to {A_choice}")
        # print(f"Player B chose to {B_choice}")

    
    print(f"Player A\'s score: {A_score}")
    print(f"Player B\'s score: {B_score}")

# Funktion för simulationen. Kräver antal rundor, As strategi och Bs strategi
simulate_tournament(300, strat_grudger, strat_random)