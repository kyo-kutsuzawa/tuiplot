# Import tuiplot.py
import tuiplot

# Create data
import numpy as np
x = np.linspace(0, 5, 100, endpoint=True)
y1 = np.sin(x * 0.2 * 2*np.pi)
y2 = np.cos(x * 0.2 * 2*np.pi)
y3 = x * 0.1

# Initialize a figure
fig = tuiplot.Figure()

# Add data to the figure
fig.plot(x, y1, label='sin(2pi * 0.2 x)')
fig.plot(x, y2, label='cos(2pi * 0.2 x)')
fig.plot(x, y3, label='0.1 x')

# Show the figure
fig.show()
