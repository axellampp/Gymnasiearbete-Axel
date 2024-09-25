import random

### Poängsystem istället för år i fängelse då det är mest logiskt att vilja ha så mycket poäng som möjligt än fängelseår

payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

# Funktion för en runda
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]
    
# Exempel på en så kallad, strategi.
def always_cooperate():
    return "Cooperate"

def always_defect():
    return "Defect"

def random_strategy():
    return random.choice(["Cooperate", "Defect"])

def simulate_tournament(num_rounds):
    A_score = 0
    B_score = 0

    for _ in range(num_rounds):
        A_choice = always_defect()
        B_choice = random_strategy()

        outcome = simulate_round(A_choice, B_choice)

        A_score += outcome[0]
        B_score += outcome[1]
    
    print("Player A\'s score: ", A_score)
    print("Player B\'s score: ", B_score)


simulate_tournament(100)