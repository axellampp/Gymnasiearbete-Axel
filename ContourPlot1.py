import numpy as np
import matplotlib.pyplot as plt

# resolution
x = np.linspace(0, 1, 500)  # More points for better detail
y = np.linspace(0, 1, 500)  # More points for better detail

# meshgrid for the plot
X, Y = np.meshgrid(x, y)

def payoff_function(X, Y):
    return -X * Y + 4 * Y + 1 - X


Z = payoff_function(X, Y)

plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 50), cmap='YlOrRd')

# contour lines for equilibrium
contour_lines = plt.contour(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 16), colors='black', linewidths=0.3)

colorbar = plt.colorbar(contour, label='Payoff')
colorbar.set_ticks(np.arange(int(Z.min()), int(Z.max()) + 1))

# Labels and title
plt.title('Payoff Contour Plot for Prisoner A')
plt.xlabel('Probability of Player A Cooperating (x)')
plt.ylabel('Probability of Player B Cooperating (y)')


plt.show()
