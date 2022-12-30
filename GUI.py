import PySimpleGUI as sg

layout1 = [
    [sg.Text('This is the first layout')],
    [sg.Button('Change to layout 2')]
]

layout2 = [
    [sg.Text('This is the second layout')],
    [sg.Button('Change to layout 1')]
]

window = sg.Window('Changeable layout', layout1)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Change to layout 2':
        window.Layout(layout2)
    elif event == 'Change to layout 1':
        window.Layout(layout1)

window.close()