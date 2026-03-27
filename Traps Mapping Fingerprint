import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111, projection='3d')

# Generate energy landscape
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

# Multiple traps (Gaussian wells)
Z = (
    -1.5*np.exp(-(X+1.5)**2 - (Y+1)**2)
    -2.5*np.exp(-(X-1)**2 - (Y-1.5)**2)
    -3.5*np.exp(-(X)**2 - (Y+2)**2)
)

ax.plot_surface(X, Y, Z)

# Electrons (points)
ax.scatter([1,-1,0], [1,-1,2], [-2,-1,-3], s=50)

ax.set_title("Defect Energy Landscape (Conceptual)")
ax.set_zlabel("Energy")

plt.show()
