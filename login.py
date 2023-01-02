import PySimpleGUI as sg
import mariadb
from mysqlConnect import cur
sg.theme("reddit")

layout = [
    [sg.VPush()],
    [sg.Text('Zaloguj się', font=('',20), pad=(0, 20))],
    [sg.Text('Nazwa użytkownika ', font=('',11))],
    [sg.InputText(key="-userInput-", pad=(10, 10), size=("30", "10"))],
    [sg.Text('Hasło', font=('',11))],
    [sg.InputText(key="-passwordInput-", pad=(10), size=("30", "10"))],
    [sg.Button('Zaloguj się', pad=(10), font=('',12), tooltip="Kliknij, aby się zalogować", k="-login-")],
    [sg.Text("Błędny login lub hasło", key="statusMessage", visible=False, text_color="red")],
    [sg.VPush()]
]
def login():
    isAdmin = 0
    window = sg.Window('Logowanie do systemu', layout, size = (700,550), resizable = False, element_justification='c', finalize=True)
    window["-login-"].set_cursor('hand2')
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            return None
        # We have to check here if user or teacher is in database
        if event =="-login-":
            name = window["-userInput-"].get()
            surname = window["-passwordInput-"].get()
            cur.execute("SELECT ID FROM student WHERE nickname=? AND password=?LIMIT 1",(name,surname,))
            if cur.rowcount == 0:
                cur.execute("SELECT ID FROM teacher WHERE nickname=? AND password=? LIMIT 1",(name,surname,))
                if cur.rowcount == 0:
                    window["statusMessage"].update(visible=True)
                else:
                    ID = cur.fetchall()
                    ID = "".join(map(str,ID[0]))
                    isAdmin = 1
                    window.close()
                    return ID, isAdmin
            else:
                ID = cur.fetchall()
                ID = "".join(map(str,ID[0]))
                isAdmin = 0
                window.close()
                return ID, isAdmin
           
    window.close()