#import libraries
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
# Define variable
x0=sp.symbols("x0")
y0=sp.symbols("y0")
t=sp.symbols("t")
phi=sp.symbols("varphi")
x=sp.symbols("x")
y=sp.symbols("y")
t5 =sp.symbols("5t") 
x_t=x0*sp.cos(t5)
y_t=y0*sp.cos(t5+phi)
#dummy variable meant to equal to 0
o=sp.symbols("o")
#expand y_t
y_t = sp.expand_trig(y_t)
#find sin(5t) in terms of y and others
sin = sp.solve(y_t-y,sp.sin(t5))[0]
#find cos(5t) in terms of x and x0
cos = sp.solve(x_t-x, sp.cos(t5))[0]
#square x_t
x2=x_t**2
#substitute cos(5t)^2 for 1-sin(5t)^2
x2 = x2.subs(sp.cos(t5)**2,1-sp.sin(t5)**2)
#substitute sin(5t) for the previously found expression
x2 = x2.subs(sp.sin(t5),sin)
x2 = sp.expand(x2)
#substitute cos(5t) for the found expression.
x2 = x2.subs(sp.cos(t5), cos) - o
#move all expression to one side, aka let the equation be 0
sol2 = sp.solve(x2-x**2,o)[0]
#simplify the equation
e = sp.simplify(sol2/x0**2*sp.sin(phi)**2)
#add the input
a = input("Value of phi: ")
b = input("Value of x0: ")
c = input("Value of y0: ")

#substitute the input
o = e.subs([(phi, a), (x0, b), (y0, c)])

# Define the function f(x, y) from 0
f = sp.lambdify((x, y), o, 'numpy')
# Generate grid for x and y
x = np.linspace(-3, 3, 400)  # x range
y = np.linspace(-3, 3, 400)  # y range
X, Y = np.meshgrid(x, y)

# Evaluate f(x, y) on the grid
Z = f(X, Y)

# Plot the contour for f(x, y) = 0
plt.figure(figsize=(6, 6))
plt.contour(X, Y, Z, levels=[0], colors='blue')  # Plot only the 0 contour
#plt.title(r'Plot of $f(x, y) = 0$')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # x-axis
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')  # y-axis
plt.grid(True, linestyle='--', alpha=0.5)
plt.gca().set_aspect('equal')  # Equal aspect ratio for x and y
plt.show()

