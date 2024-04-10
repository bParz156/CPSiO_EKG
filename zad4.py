import numpy as np
import matplotlib.pyplot as plt

# Zmienne globalne
xarray = []
valuesArray = []
datapath = 'data/'  # Upewnij się, że ta ścieżka jest poprawna
filepath = datapath + 'ekg_noise.txt'
frequency = 360

def readFile(filename=filepath, frequency=frequency, hasFirstTime=True):
    timePeriod = 1 / frequency
    global xarray, valuesArray, numberOfCases
    
    xarray.clear()
    valuesArray.clear()
    try:
        with open(filename, 'r') as file:
            for line in file:
                columns = line.split()
                if hasFirstTime and len(columns) > 1:
                    xarray.append(float(columns[0]))
                    columns = columns[1:]  # Usunięcie istniejącej kolumny
                else:
                    xarray.append(len(xarray) * timePeriod)
                
                for i, value in enumerate(columns):
                    if len(valuesArray) <= i:
                        valuesArray.append([])  # Stworzenie nowej listy
                    valuesArray[i].append(float(value))
                    
        numberOfCases = len(valuesArray)
        return True
    except FileNotFoundError as e:
        print("Błąd odczytu pliku:", e)
        return False
    except Exception as e:
        print("Nieoczekiwany błąd:", e)
        return False

def fourierIOdwrotny(x, fs, nazwa):
    # Sygnał
    plt.figure(figsize=(5,3))
    plt.plot(xarray, x)
    plt.title(nazwa)
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.tight_layout()
    plt.grid(True)
    plt.show()
    
    # Fourier
    n = len(x)
    fourier = np.fft.fft(x)
    freq_axis = np.fft.fftfreq(n, d=1/fs)
    modul = abs(fourier)
    plt.figure(figsize=(5,3))
    plt.plot(freq_axis, modul)
    plt.title('Widmo amplitudowe sygnału - ' + nazwa)
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda')
    plt.tight_layout()
    plt.grid(True)
    plt.xlim(0, fs/2)
    plt.show()
    
    # Transformata odwrotna
    odwrotna = np.fft.ifft(fourier)
    modulOdwrotna = abs(odwrotna)
    modulFunkcji = [abs(ele) for ele in x]
    roznica = modulOdwrotna - modulFunkcji
    plt.figure(figsize=(5,3))
    plt.plot(xarray, roznica)
    plt.title('Różnica między oryginałem a transformata odwrotna - ' +  nazwa)
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.grid(True)
    plt.show()

# Wywołanie funkcji
if readFile():
    fourierIOdwrotny(valuesArray[0], frequency, 'Sygnał EKG z szumem')
