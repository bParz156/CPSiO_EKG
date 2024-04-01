import matplotlib.pyplot as plt
import numpy as np
import os
from os import listdir
from os.path import isfile, join


time=[]
values=[]
def readFile(samplingFrequency, filename):
    timePeriod = 1 / samplingFrequency
    global time, values
    try:
        with open(filename, 'r') as file:
            numberLine=0
            for line in file:
                columns = line.split()
                time.append(timePeriod*numberLine)
                values.append(float(value))
                numberLine+=1
        return True
    except Exception as e:
        print("Błąd odczytu pliku", str(e))
        return False

def plot():
    plt.figure()  # Ustawienie większego rozmiaru figury
    plt.plot(time, values, label='Sygnał oryginalny')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda [mV]')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()  # Automatyczna regulacja odstępów
    plt.show()


if readFile(samplingFrequency=360,filename='C:\\Users\\Dell\\Documents\\GitHub\\CPSiO_EKG\\ekg100.txt'):
    print('here')
    plot()
else:
    print('AGHGH')


cwd = os.getcwd()
onlyfiles = [os.path.join(cwd, f) for f in os.listdir(cwd) if 
os.path.isfile(os.path.join(cwd, f))]
print(onlyfiles) 