import face_recognition
import cv2
import numpy as np
import os
import glob


lista_obecnych_uczniow = []
lista_wszystkich_uczniow = []

zakodowane_twarze = []

#wprowadzamy podstawowe dane
FOLDER_Z_UCZNIAMI = input("Podaj ścieżkę do folderu z zdjęciami uczniow: ")
PLIK_Z_LISTA_OBECNOSCI = input("Podaj ścieżkę gdzie chcesz stworzyć listę obecności: ")

#pobieramy listę uczniów z wybranego przez nas folderu
sciezka = os.getcwd() + "\\" + FOLDER_Z_UCZNIAMI + "\\"
lista_z_zdjeciami = [f for f in glob.glob(sciezka+'*.jpg')]

#sprawdzamy czy wskazany folder zawiera zdjęcia z zdjęciami uczniów
if not len(lista_z_zdjeciami):
    print("Nie znaleziono żadnego ucznia w folderze: {}".format(sciezka))
    exit(0)

for i in range(len(lista_z_zdjeciami)):
    #tworzymy liste z imionami i nazwiskami uczniów
    imie = lista_z_zdjeciami[i].replace(sciezka, "").replace("_", " ").replace(".jpg", "")
    lista_wszystkich_uczniow.append(imie)

    # tworzymy liste z zakodowanymi przez program twarzami
    globals()['zdj{}'.format(i)] = face_recognition.load_image_file(lista_z_zdjeciami[i])
    globals()['zdj_kod{}'.format(i)] = face_recognition.face_encodings(globals()['zdj{}'.format(i)])[0]
    zakodowane_twarze.append(globals()['zdj_kod{}'.format(i)])

#odpalamy kamerke
kamerka = cv2.VideoCapture(0)

#główna pętla programu
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

    #dodajemy do listy obecnosci znalezionych przez program uczniów
    for imie in imiona_znalezionych:
        if imie != "Osoba nieznana":
            if not imie in lista_obecnych_uczniow:
                lista_obecnych_uczniow.append(imie)

    # oczekiwanie na klikniecie przycisku `
    if cv2.waitKey(1) & 0xFF == ord('`'):
        # tworzymy liste obecnych i nieobecnych uczniow
        with open(PLIK_Z_LISTA_OBECNOSCI, "w") as plik:
            plik.write("Lista obecnych uczniów: ")

            for imie in lista_obecnych_uczniow:
                plik.write("\n\t- {}".format(imie))

            plik.write("\n\n Lista nieobecnych uczniów: ")
            for imie in lista_wszystkich_uczniow:
                if not imie in lista_obecnych_uczniow:
                    plik.write("\n\t- {}".format(imie))

        #wychodzimy z programu
        exit()

