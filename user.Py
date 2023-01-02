import PySimpleGUI as sg
import mariadb
import random
import string
from mysqlConnect import cur
from datetime import datetime
sg.theme("reddit")

def user(userID):
    NAME = ""
    SURNAME = ""
    try: 
        cur.execute("SELECT name, surname from student WHERE ID =?", (userID,))
        NAME,SURNAME = cur.fetchone()
        print(NAME,SURNAME)
        cur.execute("SET @row_number = 0;")
        cur.execute("SELECT (@row_number:=@row_number+1) AS num, subject.name, presence.checkingTime FROM presence INNER JOIN SUBJECT ON presence.subjectID = SUBJECT.ID WHERE presence.studentID = ?;", (1,))
    except mariadb.Error as e:
        print("error")
    data = cur.fetchall()
    dataList = [[0 for x in range(len(data[y]))] for y in range(len(data))]
    #These for transforms tuple to list and datetime to string
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == 2:
                dataList[i][2] = data[i][2].strftime("%Y-%m-%d %H:%M:%S")
            else:
                dataList[i][j] = data[i][j]
    print(dataList)
    headings = ["L.P.", "Zajęcia", "Czas sprawdzania obecnosci"]
    layout = [
        [sg.Text(f"Twoja obecność: {NAME} {SURNAME}", font=('', 20), pad=(0,20))],
        [sg.Table(values=data[:][:], headings = headings, justification='center', expand_x=True, expand_y=True, header_font=("",12), font=("",10), row_height=20,)]
    ]

    window = sg.Window("Obecność użytkownika", layout, size=(800,400))
    window.read()