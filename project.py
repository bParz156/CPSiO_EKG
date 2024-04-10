import matplotlib.pyplot as plt
import numpy as np
import time


xarray=[]
yarray=[]
samplingFrequency=10
timePeriod=1/samplingFrequency


def main():
    while True:
        menu()


def menu():
    print("MENU")
    option=input("1. Ćwiczenie 1: Napisz skrypt w Pythonie/Matlabie umożliwiający wczytywanie i wizualizację badanych sygnałów. "
          +"Program powinien umożliwiać obserwowanie wycinka sygnału dla zadanego przedziału czasowego, "
          +"skalowanie osi wykresów i ich opis oraz zapis dowolnego wycinka sygnału do pliku o podanej nazwie."
          +"\n2. Ćwiczenie 2: ..."
          +"\n3. Ćwiczenie 3: ..."
          +"\n4. Ćwiczenie 4: ..."
          +"\n4. Ćwiczenie 5: ..."
          +"\nq . Wyjdź z programu \n")
    print(option, type(option))
    if option=="1":
        zadanie1()
    elif option=="2":
        zadanie2()
    elif option=="3":
        zadanie3
    elif option=="4":
        zadanie4
    elif option=="5":
        zadanie5
    elif option=="q":
        print("Koniec programu. Do widzenia")
        time.sleep(1)
        exit()
    else:
        print("Wybranej opcji nie ma wśród dostępnych")
        
    
    
def zadanie1():
    print("Zadanie 1 ")
    while True:
        samplingFrequency=int(input("Podaj częstotliwość próbkowanie sygnału EKG \n"))
        if samplingFrequency>=0:
            break
        else: 
            print("Częstotliwość musi być dodatnią liczbą całkowitą!")
            continue
    timePeriod=1/samplingFrequency
    filename=input("Podaj nazwę pliku (Z ROZSZERZENIEM), z którego mają zostać wczytane dane \n")
    hasFirstTime=False
    while True:
        option=int(input("Wybierz: \n 1. Jeśli dane w wybranym pliku mają w pierwszej kolumnie czas"
                   +"\n 2. Jeśli pierwsza kolumna zawiera dane \n"))
        if option==1:
            hasFirstTime=True
            break
        elif option==2:
            break
        else: 
            print("Wybierz opcję z listy!")
            continue
    
    while (not readFile(filename, hasFirstTime)):
        print("Podany plik stwarza problemu, podaj inny plik")
        filename=input("Podaj nazwę pliku (Z ROZSZERZENIEM), z którego mają zostać wczytane dane \n")
        while True:
            samplingFrequency=int(input("Podaj częstotliwość próbkowanie sygnału EKG \n"))
            if samplingFrequency>=0:
                break
            else: 
                print("Częstotliwość musi być dodatnią liczbą całkowitą!")
                continue
        timePeriod=1/samplingFrequency
        hasFirstTime=False
        while True:
            option=int(input("Wybierz: \n 1. Jeśli dane w wybranym pliku mają w pierwszej kolumnie czas"
                        +"\n 2. Jeśli pierwsza kolumna zawiera dane \n"))
            if option==1:
                hasFirstTime=True
                break
            elif option==2:
                break
            else: 
                print("Wybierz opcję z listy!")
                continue
    
    plotEKG()

def zadanie2():
    print("Zadanie 2")

def zadanie3():
    print("Zadanie 3")

def zadanie4():
    print("Zadanie 4")
def zadanie5():
    print("Zadanie 5")

"""filename - name of the file from which the EKG signals is read
isFirstValid - the information whatever th first column is valid as x-array or if that's time
"""
def readFile(filename, hasFirstTime):
    try:
        file = open(filename, 'r')
        allcount=0
        for line in file:
            columns=line.split()
            count=0

            if hasFirstTime:
                for pom in columns:
                    if (count==0):
                        xarray.append(pom)
                    else:
                        yarray.append(pom)
                    count+=1
            else:
                for pom in columns:
                    yarray.append(pom)
                    xarray.append(allcount*timePeriod)
                    allcount+=1
            count=0

        file.close()
        return True
    except:
        return False

def plotEKG():
    default_size=100
    plt.plot(xarray[0:default_size],yarray[0:default_size])
    plt.show()

main()