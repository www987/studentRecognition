import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

# Generate some data to plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create the layout for the window
layout = [
    [sg.Text('Graph Example')],
    [
        sg.Column(
            layout=[
                [sg.Text()]
            ],
            justification='left'
        )
    ]
]

# Create the window
window = sg.Window('Graph Example').Layout(layout)

# Plot the data on the graph

# Run the event loop to process user input
while True:
    event, values = window.Read()
    if event is None:
        break

# Close the window
window.Close()