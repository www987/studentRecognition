import mariadb as cur
import PySimpleGUI as sg
sg.theme("reddit")
graph = sg.Graph((50, 50), (0, 0), (80, 100), key='-GRAPH-')
layout_1 = [
        [graph, sg.Push()],
        [sg.VPush()],
        [sg.Text("MENU", font=('',20), pad=(10,10))],
        [sg.Button("Sprawdz obecnosc", font=('',13), k="-l1_checkPresence-", pad=(10,10), size=(20,1))],
        [sg.Button("Dodaj ucznia", k="-l1_addStudent-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.Button("Dodaj admina", k="-l1_addAdmin-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.Button("Pokaż obecności", k="-l1_showPresence-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.VPush()],
]
# Next time I should assign ID to every layout
#Ok I will do this here maybe just l2 - layout 2
layout_2 = [
    [graph, sg.Push()],
    [sg.VPush()],
    [sg.Text("Sprawdzanie obecności", font=('',20),  k="-l2_mainText-")],
    [sg.Text("Dla jakiego przedmiotu ma być sprawdzana obecność?", key="l2_textSubject")],
    [sg.InputText(key="l2_inputSubject")],
    [sg.Button("Sprawdź obecność", key="-l2_buttonCheckAll-")],
    [sg.Text("Rozpoczęto sprawdzanie obecności...", k="-l2_statusText-", font=('',13), pad=(10,10))],
    [sg.Text('', size=(50, 1), relief='sunken',
                   text_color='yellow', background_color='#0079d3',key='-l2_statusBar-', metadata=0, pad=(5,5))], 
    [sg.VPush()]
]
layout_3 = [
    [graph, sg.Push()],
    [sg.VPush()],
    [sg.Text("Dodaj ucznia", font=('',20), pad=(10))],
    [sg.Text('Imie ucznia', font=('',11))],
    [sg.InputText(k="-addStudentName-", pad=(10))],
    [sg.Text('Nazwisko ucznia', font=('',11))],
    [sg.InputText(k="-addStudentSurname-", pad=(10))],
    [sg.Text('Hasło ucznia', font=('',11))],
    [sg.InputText(k="-addStudentPassword-", pad=(10))],
    [sg.Text('Scieżka do zdjęcia ucznia', font=('',11))],
    [sg.InputText(k="-addStudentImage-", pad=(10))],
    [sg.Button('Potwierdź', pad=(10), font=('',12), tooltip="Kliknij, aby się zalogować", k="-confirmAddStudent-")],
    [sg.Text("Błędny login lub hasło", key="studentStatusMessage", visible=False, text_color="red")],
    [sg.VPush()]
]
layout_4 = [
    [graph, sg.Push()],
    [sg.VPush()],
    [sg.Text("Dodaj nauczyciela", font=('',20), pad=(10))],
    [sg.Text('Imie nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminName-", pad=(10))],
    [sg.Text('Nazwisko nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminSurname-", pad=(10))],
    [sg.Text('Hasło nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminPassword-", pad=(10))],
    [sg.Button('Potwierdź', pad=(10), font=('',12), tooltip="Kliknij, aby się zalogować", k="-confirmAddAdmin-")],
    [sg.Text("Błędny login lub hasło", key="-adminStatusMessage-", visible=False, text_color="red")],
    [sg.VPush()]
]
layout_5 = [
    [graph, sg.Push()],
    [sg.VPush()],
    [sg.Text("Dla jakiej daty mają być pokazane obecności?", font=('',20), pad=(10), key="l5_mainText")],
    [sg.InputText(k="-l5_inputDate-", pad=(10))],
    [sg.Table(headings="", values="")]
    [sg.VPush()]
]
layout = [
    [sg.Column(layout_1, key="-COL1-"),
    sg.Column(layout_1, key="-COL2-"),
    sg.Column(layout_1, key="-COL3-"),
    sg.Column(layout_1, key="-COL4-"),
    sg.Column(layout_1, key="-COL5-")]
]

def admin(adminID):
    
    window = sg.Window("Wybór opcji", layout_2, size=(700,550), element_justification='c', finalize=True, resizable = False)
    image_id = graph.draw_image("images/left-arrow.png", location=(15, 90))
    '''  
    window["-checkPresence-"].set_cursor("hand2")
    window["-addStudent-"].set_cursor("hand2")
    window["-addAdmin-"].set_cursor("hand2") 
    '''
    while True:
        event,values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
                return None
                
        #text.metadata = (text.metadata + 1) % 51
        #text.update(text.metadata)
admin(1)