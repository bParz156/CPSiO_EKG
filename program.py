import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import time

xarray=[]
yarray=[]
fs=None

class SampleApp(tk.Tk):
   
    def __init__(self): 
        width=800
        height=600
        tk.Tk.__init__(self)
        self.title("Cyfrowe Przetwarzanie Sygnałów i Obrazów")
        self.geometry(str(width)+"x"+str(height))

        self.pages = {}

        main_page = MainPage(self)
        self.add_page("main_page", main_page)

        for i in range(1, 6):
            page = Page(self, f"Page {i}")
            self.add_page(f"page_{i}", page)

        self.show_page("main_page")

    def add_page(self, name, page):
        self.pages[name] = page

    def show_page(self, name):
        for page_name, page in self.pages.items():
            if page_name == name:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text="Przetwarzanie i analiza sygnału EKG", font=("Helvetica", 18))
        self.label.pack(pady=10)
        label = tk.Label(self, text="Barbara Parzonka i Joanna Zoglowek", font=("Helvetica", 12))
        label.pack(pady=10)

        for i in range(1, 5):
            button = tk.Button(self, text=f"Zadanie {i}", command=lambda i=i: master.show_page(f"page_{i}"))
            button.pack(pady=5, padx=10, fill='x')

class Page(tk.Frame):
    def __init__(self, master, name):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text=name, font=("Helvetica", 18))
        self.label.pack(pady=10)
        
        button = tk.Button(self, text="Wróć", command=lambda: master.show_page("main_page"))
        button.pack(pady=10)

        if name == "Page 1":
            container = tk.Frame(self)
            container.pack(pady=10)

            # Set the weight of the first column to 15% of the total width
            container.grid_columnconfigure(0, weight=1, minsize=int(master.winfo_width() * 0.15), )

            label1 = tk.Label(container, text="Podaj czestotliwosc probkowania sygnalu (Hz)", font=("Helvetica", 18))
            label1.grid(row=0, column=0, sticky='w', padx=10, pady=5)
            self.entry1 = tk.Entry(container)
            self.entry1.grid(row=0, column=1, columnspan=1, padx=10, pady=5)

            label2 = tk.Label(container, text="Podaj nazwe pliku z danymi (z roszerzeniem)", font=("Helvetica", 18))
            label2.grid(row=1, column=0, sticky='w', padx=10, pady=5)
            self.entry2 = tk.Entry(container)
            self.entry2.grid(row=1, column=1, columnspan=1, padx=10, pady=5)

            self.checkbox_var = tk.BooleanVar()
            self.checkbox = tk.Checkbutton(container, text="Zaznacz jesli pierwsza kolumna zawiera czas", variable=self.checkbox_var)
            self.checkbox.grid(row=2, column=0, columnspan=1, sticky='w', padx=10, pady=5)

            self.button = tk.Button(container, text="Wyświetl wykres", command=lambda: self.plotChartButtonCLicked(master=master))
            self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

        elif name == "Page 5":
            container = tk.Frame(self)
            container.pack(pady=10)

            # Set the weight of the first column to 15% of the total width
            container.grid_columnconfigure(0, weight=1, minsize=int(master.winfo_width() * 0.15), )

            label1 = tk.Label(container, text="Podaj dolny ogranicznik czasu", font=("Helvetica", 18))
            label1.grid(row=0, column=0, sticky='w', padx=10, pady=5)
            self.entryBottomLimit = tk.Entry(container)
            self.entryBottomLimit.grid(row=0, column=1, columnspan=1, padx=10, pady=5)

            label2 = tk.Label(container, text="Podaj górny ogranicznik czasu", font=("Helvetica", 18))
            label2.grid(row=1, column=0, sticky='w', padx=10, pady=5)
            self.entryUpperLimit = tk.Entry(container)
            self.entryUpperLimit.grid(row=1, column=1, columnspan=1, padx=10, pady=5)
            
            self.button = tk.Button(container, text="Aktualizuj wykres", command=self.updatePlot)
            self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
            
    def plotChartButtonCLicked(self, master):
        global fs
        ok=True
        try:
            fs=int(self.entry1.get())
        except:
            answer=messagebox.askquestion(title= "Brak podanej częstotliwośći",message= "Nie podano częstotliwości. Czy chcesz przyjąć, że częstotliwość to 100 Hz?")
            ok=answer==messagebox.YES

        if ok:
            if zadanie1(fs,self.entry2.get(),self.checkbox_var.get()):
                master.show_page("page_5")

    def updatePlot(self):
        upperLimit=float(self.entryUpperLimit.get())
        bottomLimmit=float(self.entryBottomLimit.get())
        if upperLimit<= bottomLimmit:
            messagebox.showwarning(message="Górna granica nie może być mniejsza niż dolna")
        elif (bottomLimmit<0 or upperLimit<0 ):
            messagebox.showwarning(message="Granice muszą być dodatnie")
        else:
            bottomLimmit=int(bottomLimmit*fs)
            upperLimit=int(upperLimit*fs)
            plotEKG(bottomLimmit, upperLimit)

def zadanie1(freq, filename, hasFirstTime):
    global xarray, yarray
    if freq <= 0:
        messagebox.showinfo(message="Częstotliwość musi być liczbą dodatnią")
        return False

    # Sprawdzenie, czy wybrany plik to 'ekg100.txt' i czy ma być obsłużony specjalnie
    if filename.endswith('ekg100.txt'):
        time, data = readSingleColumnFile(filename, freq)
        if time is None or data is None:
            messagebox.showinfo(message="Wybrany plik jest niepoprawny")
            return False
        # Rysowanie wykresu dla 'ekg100.txt'
        plotEKG(time, data, 1)  # Dla uproszczenia przyjmujemy, że rysujemy tylko jeden wykres
    else:
        # Obsługa plików z wieloma kolumnami
        columns = readMultipleColumns(filename)
        if not columns:
            messagebox.showinfo(message="Wybrany plik jest niepoprawny")
            return False

        # Decyzja na podstawie hasFirstTime
        if hasFirstTime and len(columns) > 1:
            xarray, yarrays = columns[0], columns[1:]
            for i, yarray in enumerate(yarrays, start=1):
                plotEKG(xarray, yarray, i)
        else:
            # Jeśli pierwsza kolumna nie zawiera czasu, użyj indeksu jako osi X
            for i, column in enumerate(columns, start=1):
                xarray = list(range(len(column)))
                plotEKG(xarray, column, i)
    return True

def readMultipleColumns(filename):
    columns = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                values = line.split()  # Dzielenie linii na wartości
                for i, value in enumerate(values):
                    if len(columns) <= i:  # Jeśli to nowa kolumna, dodaj nową listę
                        columns.append([])
                    columns[i].append(float(value))
        return columns
    except Exception as e:
        print(f"Nie udało się odczytać pliku: {e}")
        return []

def plotEKG(xarray, yarray, figure_number):
    plt.figure(figure_number)
    plt.plot(xarray, yarray)
    plt.title(f'Wykres kolumny {figure_number}')
    plt.xlabel('Czas [s]' if figure_number == 1 else 'Indeks próbki')
    plt.ylabel('Wartość [mV]')
    # Ustawienie limitów dla osi X
    #plt.xlim(left=bottomLimmit/fs, right=upperLimit/fs)
    plt.show()
    
def readSingleColumnFile(filename, frequency):
    try:
        with open(filename, 'r') as file:
            data = []
            for line in file:
                try:
                    # Usuwamy białe znaki i konwertujemy linie na float
                    data.append(float(line.strip()))
                except ValueError as e:
                    print(f"Problem z linijką '{line.strip()}': {e}")
        # Zakładamy, że czas jest równomiernie rozmieszczony i obliczamy go
        time = [i / frequency for i in range(len(data))]
        return time, data
    except Exception as e:
        print(f"Nie udało się otworzyć pliku: {e}")
        return None, None


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()




