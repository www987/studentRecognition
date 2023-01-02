import face_recognition
import cv2
import numpy as np
import os
import glob
import time
# Aby kod działał plik wykonywalny musi być w tej samej scieżce co folder uczniowie

def studentRecognition():
    lista_obecnych_uczniow = []
    lista_wszystkich_uczniow = []

    zakodowane_twarze = []

    #pobieramy listę uczniów z wybranego przez nas folderu
    sciezka = os.getcwd() + "\\" + "uczniowie" + "\\"
    lista_z_zdjeciami = [f for f in glob.glob(sciezka+'*.jpg')]

    listWithFace = []
    listWithFaceEncoded = []
    for i in range(len(lista_z_zdjeciami)):
        #tworzymy liste z imionami i nazwiskami uczniów
        nickname = lista_z_zdjeciami[i].replace(sciezka, "").replace(".jpg", "")
        lista_wszystkich_uczniow.append(nickname)

        # tworzymy liste z zakodowanymi przez program twarzami
        listWithFace.append(face_recognition.load_image_file(lista_z_zdjeciami[i]))
        if(cv2.haveImageReader(lista_z_zdjeciami[i])):
            print("tak")
        listWithFaceEncoded.append(face_recognition.face_encodings(listWithFace[i])[0])
        zakodowane_twarze.append(listWithFaceEncoded[i])
        print("test")

    #odpalamy kamerke
    kamerka = cv2.VideoCapture(0)
    start_time = time.time()
    while True:
        #odczytujemy klatke i skalujemy ją
        _, klatka = kamerka.read()
        zeskalowana_klatka = cv2.resize(klatka, (0, 0), fx=0.25, fy=0.25)

        #skanujemy daną klatke w poszukiwaniu twarzy
        znalezione_twarze = face_recognition.face_locations(zeskalowana_klatka)
        zakodowana_twarz = face_recognition.face_encodings(zeskalowana_klatka, znalezione_twarze)
        imiona_znalezionych = []
        for twarz in zakodowana_twarz:
            wyniki = face_recognition.compare_faces(zakodowane_twarze, twarz)
            imie = "Osoba nieznana"
            dystans = face_recognition.face_distance(zakodowane_twarze, twarz)
            try:
                najlepszy_wynik = np.argmin(dystans)
                if wyniki[najlepszy_wynik]:
                    imie = lista_wszystkich_uczniow[najlepszy_wynik]
                imiona_znalezionych.append(imie)
            except:
                pass

        # jeżeli na klatce znaleziono twarze wyświetlamy wokół nich ramki w raz z imieniem
        for (gora, prawo, dol, lewo), imie in zip(znalezione_twarze, imiona_znalezionych):
            gora *= 4
            prawo *= 4
            dol *= 4
            lewo *= 4

            cv2.rectangle(klatka, (lewo, gora), (prawo, dol), (255, 0, 0), 2)
            cv2.rectangle(klatka, (lewo, gora), (prawo, gora + 20), (255, 0, 0), cv2.FILLED)
            cv2.putText(klatka, imie, (lewo + 3, gora + 13), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), 1)

        #wyświetlamy klatke w raz z ramkami
        cv2.imshow('Video', klatka)
        for imie in imiona_znalezionych:
            if imie != "Osoba nieznana":
                if not imie in lista_obecnych_uczniow:
                    lista_obecnych_uczniow.append(imie)
        print(lista_obecnych_uczniow)
        elapsed_time = time.time() - start_time
        key = cv2.waitKey(1)
        if key == 27:  # 27 is the ASCII code for the Esc key
            return lista_obecnych_uczniow