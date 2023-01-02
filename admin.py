# do not forget to change position of commit cur and to restart primary key
from mysqlConnect import cur
from faceRecognition import studentRecognition
import datetime
import mariadb
import PySimpleGUI as sg
sg.theme("reddit")

graph2= sg.Graph((50, 120), (0, 0), (100, 100), key='-GRAPH2-', enable_events=True)
graph3= sg.Graph((50, 120), (0, 0), (100, 100), key='-GRAPH3-', enable_events=True)
graph4= sg.Graph((50, 120), (0, 0), (100, 100), key='-GRAPH4-', enable_events=True)
graph5 = sg.Graph((50, 120), (0, 0), (80, 100), key='-GRAPH5-', enable_events=True)
graph6 = sg.Graph((50, 120), (0, 0), (80, 100), key='-GRAPH6-', enable_events=True)
layout_1 = [
        [sg.VPush()],
        [sg.Push(), sg.Text("MENU", font=('',20), pad=(10,10)), sg.Push()],
        [sg.Button("Sprawdz obecnosc", font=('',13), k="-l1_checkPresence-", pad=(10,10), size=(20,1))],
        [sg.Button("Dodaj ucznia", k="-l1_addStudent-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.Button("Dodaj admina", k="-l1_addAdmin-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.Button("Pokaż obecności", k="-l1_showPresence-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.Button("Pokaż uczniów", k="-l1_showStudents-", font=('',13), pad=(10,10), size=(20,1))],
        [sg.VPush()],
]
# Next time I should assign ID to every layout
#Ok I will do this here maybe just l2 - layout 2
layout_2 = [
    [graph2, sg.Push()],
    [sg.Text("Sprawdzanie obecności", font=('',20),  k="-l2_mainText-")],
    [sg.Text("Dla jakiego przedmiotu ma być sprawdzana obecność?", key="l2_textSubject")],
    [sg.InputText(key="-l2_inputSubject-")],
    [sg.Button("Sprawdź obecność", key="-l2_buttonCheckAll-")],
    [sg.Text("Błędnie podane dane", key="-l2_errorMessage-", visible=False, text_color="red")],
]
layout_3 = [
    [graph3, sg.Push()],
    [sg.Text("Dodaj ucznia", font=('',20), pad=(10))],
    [sg.Text('Imie ucznia', font=('',11))],
    [sg.InputText(k="-addStudentName-", pad=(10))],
    [sg.Text('Nazwisko ucznia', font=('',11))],
    [sg.InputText(k="-addStudentSurname-", pad=(10))],
    [sg.Text('Hasło ucznia', font=('',11))],
    [sg.InputText(k="-addStudentPassword-", pad=(10))],
    [sg.Button('Potwierdź', pad=(10), font=('',12), tooltip="Kliknij, aby się zalogować", k="-confirmAddStudent-")],
    [sg.Text("Błędnie podane dane", key="studentStatusMessage", visible=False, text_color="red")],
]
layout_4 = [
    [graph4, sg.Push()],
    [sg.Text("Dodaj nauczyciela", font=('',20), pad=(10))],
    [sg.Text('Imie nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminName-", pad=(10))],
    [sg.Text('Nazwisko nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminSurname-", pad=(10))],
    [sg.Text('Hasło nauczyciela', font=('',11))],
    [sg.InputText(k="-addAdminPassword-", pad=(10))],
    [sg.Button('Potwierdź', pad=(10), font=('',12), tooltip="Kliknij, aby się zalogować", k="-confirmAddAdmin-")],
    [sg.Text("Błędny podane dane", key="-adminStatusMessage-", visible=False, text_color="red")],
]
layout_5 = [
    [graph5, sg.Push()],
    [sg.Text("Obecności w danym dniu", font=('',20), pad=(10), key="l5_mainText")],
    [sg.Text("Dla jakiej daty mają być pokazane obecności? RRRR-MM-DD", font=('',13), pad=(10))],
    [sg.InputText(k="-l5_inputDateR-", pad=(10), size=(4,4)), sg.InputText(k="-l5_inputDateM-", pad=(10), size=(2,4)), sg.InputText(k="-l5_inputDateD-", pad=(10), size=(2,4))],
    [sg.Button("Pokaż obecności", k="-l5_showPresence-")],
    [sg.Text("Błędnie podane dane", key="-l5_errorMessage-", visible=False)], 
    [sg.Table(values=[[]], headings = ["L.P.", "Zajęcia", "Godzina sprawdzania", "uczeń"], visible = False, key="-l5_tableData-", justification = "c", col_widths=(1,10,20,20), size=(900,500), expand_x=True, auto_size_columns=False)],
]
layout_6 = [
    [graph6, sg.Push()],
    [sg.Text("Uczniowie", font=('',20), pad=(10), key="l6_mainText")],
    [sg.Table(values=[[]], headings = ["L.P.", "Imię", "nazwisko", "nickname"], visible = False, key="-l6_tableData-", justification = "c", col_widths=(1,10,20,20), size=(900,500), expand_x=True, auto_size_columns=False)],
]
layout = [
    [sg.Column(layout_1, key="-COL1-", visible=True, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True),
    sg.Column(layout_2, key="-COL2-", visible=False, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True),
    sg.Column(layout_3, key="-COL3-", visible=False, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True),
    sg.Column(layout_4, key="-COL4-", visible=False, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True),
    sg.Column(layout_5, key="-COL5-", visible=False, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True),
    sg.Column(layout_6, key="-COL6-", visible=False, element_justification="c", justification="center", vertical_alignment="center",expand_y=True, expand_x=True)
    ]
]

def admin(adminID):
    window = sg.Window("Tryb admina", layout, finalize=True, resizable = False, size=(800,600))
    image_id = graph2.draw_image("images/left-arrow.png", location=(15, 90))
    image_id = graph3.draw_image("images/left-arrow.png", location=(15, 90))
    image_id = graph4.draw_image("images/left-arrow.png", location=(15, 90))
    image_id = graph5.draw_image("images/left-arrow.png", location=(15, 90))
    image_id = graph6.draw_image("images/left-arrow.png", location=(15, 90))
    '''  
    window["-checkPresence-"].set_cursor("hand2")
    window["-addStudent-"].set_cursor("hand2")
    window["-addAdmin-"].set_cursor("hand2") 
    '''
    # I know it should be in function but did not have time
    while True:
        event,values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
                break
        print(event)
        if event == "-l1_checkPresence-":
            window["-COL2-"].update(visible=True)
            
            window["-COL3-"].update(visible=False)
            window["-COL4-"].update(visible=False)
            window["-COL5-"].update(visible=False)
            window["-COL6-"].update(visible=False)
            window["-COL1-"].update(visible=False)
            
        if event == "-l1_addStudent-":
            window["-COL2-"].update(visible=False)
            window["-COL5-"].update(visible=False)
            window["-COL4-"].update(visible=False)
            window["-COL1-"].update(visible=False)
            window["-COL6-"].update(visible=False)

            window["-COL3-"].update(visible=True)
        if event == "-l1_addAdmin-":
            window["-COL5-"].update(visible=False)
            window["-COL3-"].update(visible=False)
            window["-COL2-"].update(visible=False)
            window["-COL1-"].update(visible=False)
            window["-COL6-"].update(visible=False)

            window["-COL4-"].update(visible=True)
        if event == "-l1_showPresence-":
            window["-COL4-"].update(visible=False)
            window["-COL3-"].update(visible=False)
            window["-COL2-"].update(visible=False)
            window["-COL1-"].update(visible=False)
            window["-COL6-"].update(visible=False)

            window["-COL5-"].update(visible=True)
        if event == "-GRAPH2-" or event == "-GRAPH3-" or event == "-GRAPH4-" or event == "-GRAPH5-" or event == "-GRAPH6-":
            window["-COL6-"].update(visible=False)
            window["-COL5-"].update(visible=False)
            window["-COL4-"].update(visible=False)
            window["-COL3-"].update(visible=False)
            window["-COL2-"].update(visible=False)
            window["-COL6-"].update(visible=False)

            window["-COL1-"].update(visible=True)
        if event == "-l1_showStudents-":
            window["-COL6-"].update(visible=True)
            
            window["-COL3-"].update(visible=False)
            window["-COL4-"].update(visible=False)
            window["-COL5-"].update(visible=False)
            window["-COL2-"].update(visible=False)
            window["-COL1-"].update(visible=False)

        
        if event =="-confirmAddStudent-":
            name = window["-addStudentName-"].get()
            surname = window["-addStudentSurname-"].get()
            password = window["-addStudentPassword-"].get()
            if(len(name) == 0 or len(surname) == 0 or len(password) == 0):
                window["studentStatusMessage"].update(visible=True)
            else:
                window["studentStatusMessage"].update("Poprawnie dodano ucznia",visible=True)
                nickname = name + '_' + surname[0]
            try:
                cur.execute("INSERT INTO student VALUES('',?,?,?,?)",(name,surname, password, nickname,))
            except mariadb.Error as e:
                print("error", e)
        if event =="-confirmAddAdmin-":
            name = window["-addAdminName-"].get()
            surname = window["-addAdminSurname-"].get()
            password = window["-addAdminPassword-"].get()
            if(len(name) == 0 or len(surname) == 0 or len(password) == 0):
                window["adminStatusMessage"].update(visible=True)
            else:
                window["studentStatusMessage"].update("Poprawnie dodano nauczyciela",visible=True)
                nickname = name + '_' + surname[0]
            try:
                cur.execute("INSERT INTO teacher VALUES('',?,?,?,?)",(name,surname, password, nickname))
            except mariadb.Error as e:
                print("error", e)
        if event == "-l5_showPresence-":
            inputDateR = window["-l5_inputDateR-"].get()
            inputDateM = window["-l5_inputDateM-"].get()
            inputDateD = window["-l5_inputDateD-"].get()
            inputDateRMD = inputDateR + '-'+ inputDateM + "-" + inputDateD
            if(inputDateR.isnumeric() and inputDateM.isnumeric() and inputDateD.isnumeric()):
                window["-l5_errorMessage-"].update(visible = True)
                cur.execute("SET @row_number = 0;")
                cur.execute("SELECT (@row_number:=@row_number+1) AS num, subject.name, presence.checkingTime, CONCAT(student.name,' ', student.surname) AS studentData  FROM presence INNER JOIN SUBJECT ON presence.subjectID = SUBJECT.ID INNER JOIN student ON presence.studentID = student.ID WHERE DATE(presence.checkingTime) = ?;", (inputDateRMD,))
                presenceData = cur.fetchall()
                print(presenceData)
                presenceDataList = [[0 for x in range(len(presenceData[y]))] for y in range(len(presenceData))]
                for i in range(len(presenceData)):
                    for j in range(len(presenceData[i])):
                        if j == 2:
                            presenceDataList[i][j] = presenceData[i][2].strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            presenceDataList[i][j] = presenceData[i][j]
                window['-l5_tableData-'].update(visible = True)
                print(presenceDataList)
                window['-l5_tableData-'].update(values=presenceDataList)
            else:
                window["-l5_errorMessage-"].update(visible = True)
        if event == "-l1_showStudents-":
            cur.execute("SET @row_number = 0;")
            cur.execute("SELECT (@row_number:=@row_number+1) AS num, name, surname, nickname FROM student;")
            presenceData = cur.fetchall()
            print(presenceData)
            presenceDataList = [[0 for x in range(len(presenceData[y]))] for y in range(len(presenceData))]
            for i in range(len(presenceData)):
                for j in range(len(presenceData[i])):
                    presenceDataList[i][j] = presenceData[i][j]
            window['-l6_tableData-'].update(visible = True)
            print(presenceDataList)
            window['-l6_tableData-'].update(values=presenceDataList)
        if event == "-l2_buttonCheckAll-":
            subject = window["-l2_inputSubject-"].get()
            if subject:
                subjectID = ""
                window["-l2_errorMessage-"].update(visible = False)
                listOfStudents = studentRecognition()
                cur.execute("SELECT ID FROM subject WHERE name =? LIMIT 1",(subject,))
                currentDatetime = datetime.datetime.now()
                currentDatetimeFormat = currentDatetime.strftime('%Y-%m-%d %H:%M:%S')
                if cur.rowcount == 0:
                    cur.execute("Insert into subject VALUES('',?)", (subject,))
                    cur.execute("SELECT ID FROM subject WHERE name =? LIMIT 1",(subject,))
                    dataTemp = cur.fetchall()
                    subjectID = "".join(map(str,dataTemp[0]))
                else:
                    cur.execute("SELECT ID FROM subject WHERE name =? LIMIT 1",(subject,))
                    dataTemp = cur.fetchall()
                    subjectID = "".join(map(str,dataTemp[0]))
                for x in listOfStudents:
                    cur.execute("SELECT ID FROM student WHERE nickname =? LIMIT 1",(x,))
                    dataTemp = cur.fetchall()
                    studentID= "".join(map(str,dataTemp[0]))
                    try:
                        cur.execute("INSERT INTO presence VALUES('',?,?,?,?)",(int(studentID),int(adminID),int(subjectID),currentDatetimeFormat,))
                    except mariadb.Error as e:
                        print("error")

                window["-l2_errorMessage-"].update("Sprawdzono obecność dla przedmiotu {}. Sprawdz szczegóły w menu".format(subject,), visible = True, text_color="green")
            else:
                window["-l2_errorMessage-"].update(visible = True, text_color="red")
        #text.metadata = (text.metadata + 1) % 51
        #text.update(text.metadata)