import random

payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

# Funktion för en runda
def simulate_round(A_Choice, B_Choice):
    return payoff_matrix[(A_Choice, B_Choice)]