import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time

xarray=[]
valuesArray=[]
fs=None
numberOfCases=1

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
        elif name == "Page 2":
            # Etykieta strony
            self.label = tk.Label(self, text="Analiza FFT", font=("Helvetica", 18))
            self.label.pack(pady=10)
            
            # Kontener na elementy
            container = tk.Frame(self)
            container.pack(pady=10)

            # Etykieta i pole wejściowe dla częstotliwości 1
            tk.Label(container, text="Częstotliwość 1 (Hz):", font=("Helvetica", 12)).grid(row=0, column=0, sticky='w', padx=10, pady=5)
            self.freq1_entry = tk.Entry(container, font=("Helvetica", 12))
            self.freq1_entry.grid(row=0, column=1, padx=10, pady=5)

            # Etykieta i pole wejściowe dla częstotliwości 2
            tk.Label(container, text="Częstotliwość 2 (Hz):", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w', padx=10, pady=5)
            self.freq2_entry = tk.Entry(container, font=("Helvetica", 12))
            self.freq2_entry.grid(row=1, column=1, padx=10, pady=5)

            # Etykieta i pole wejściowe dla czasu trwania sygnału
            tk.Label(container, text="Czas trwania sygnału (s):", font=("Helvetica", 12)).grid(row=2, column=0, sticky='w', padx=10, pady=5)
            self.duration_entry = tk.Entry(container, font=("Helvetica", 12))
            self.duration_entry.grid(row=2, column=1, padx=10, pady=5)

            # Etykieta i pole wejściowe dla częstotliwości próbkowania
            tk.Label(container, text="Częstotliwość próbkowania (Hz):", font=("Helvetica", 12)).grid(row=3, column=0, sticky='w', padx=10, pady=5)
            self.sampling_rate_entry = tk.Entry(container, font=("Helvetica", 12))
            self.sampling_rate_entry.grid(row=3, column=1, padx=10, pady=5)

            self.run_task_button = tk.Button(container, text="Uruchom zadanie 2", command=self.run_task_2)
            self.run_task_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def run_task_2(self):
        try:
            f1 = float(self.freq1_entry.get())
            f2 = float(self.freq2_entry.get())
            fs = int(self.sampling_rate_entry.get())
            zadanie2(f1, f2, fs)  
        except ValueError as e:
            messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

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
        messagebox.showinfo(message="Czestotliwość musi być liczbą dodatnią")
    return False
           


    """filename - name of the file from which the EKG signals is read
    isFirstValid - the information whatever th first column is valid as x-array or if that's time """

def readFile(samplingFrequency,filename, hasFirstTime):
    timePeriod=1/samplingFrequency
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
                        yarray.append(float(pom))

                    count+=1

            else:
                 for pom in columns:
                    yarray.append(float(pom))
                    xarray.append(allcount*timePeriod)
                    allcount+=1
            count=0
        file.close()
        return True
    except: 
        return False


def plotEKG(bottomLimmit=0, upperLimit=100):
    plt.figure()
    plt.plot(xarray[bottomLimmit:upperLimit], yarray[bottomLimmit:upperLimit])
    plt.xlabel('time [s]')
    plt.ylabel('amplituda sygnalu [mV]')
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

class MultiChartApp:
    def __init__(self, master, num_charts):
        self.master = master
        self.num_charts = num_charts
        self.figures = []

        # Create and pack a notebook widget to hold the charts
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create and add each chart to the notebook
        for i in range(num_charts):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f"Chart {i+1}")

            # Create a figure and axes for the chart
            fig, ax = plt.subplots()
            self.figures.append(fig)

            # Plot some data on the axes
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            ax.plot(x, y)
            
            # Embed the figure in the tkinter frame
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def zadanie2(f1, f2, fs):

    # Parametry sygnału
    f1 = 50  # częstotliwość fali sinusoidalnej 50Hz
    f2 = 60  # częstotliwość fali sinusoidalnej 60Hz
    signal_length = 65536  # długość sygnału
    fs = 1000  # częstotliwość próbkowania (fs > 2*fmax zgodnie z twierdzeniem Nyquista)

    # Czas trwania sygnału
    t = np.arange(signal_length) / fs

    # 1. Generowanie ciągu próbek dla fali sinusoidalnej 50 Hz
    signal_50Hz = np.sin(2 * np.pi * f1 * t)

    # 2. Dyskretna transformata Fouriera (DFT) sygnału 50 Hz
    fft_50Hz = np.fft.fft(signal_50Hz)
    freqs = np.fft.fftfreq(signal_length, 1/fs)
    half_freqs = freqs[:signal_length//2]
    half_fft_50Hz = np.abs(fft_50Hz[:signal_length//2])  # Widmo amplitudowe

    # Wykres widma amplitudowego dla sygnału 50 Hz
    plt.figure(figsize=(12, 6))
    plt.plot(half_freqs, half_fft_50Hz)
    plt.title('Widmo amplitudowe sygnału 50 Hz')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda')
    plt.xlim(0, fs/2)
    plt.grid()
    plt.show()

    # 3. Generowanie ciągu próbek dla mieszaniny dwóch fal sinusoidalnych (50Hz i 60Hz)
    mixed_signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

    # DFT mieszaniny sygnałów
    fft_mixed = np.fft.fft(mixed_signal)
    half_fft_mixed = np.abs(fft_mixed[:signal_length//2])  # Widmo amplitudowe

    # Wykres widma amplitudowego dla mieszaniny sygnałów
    plt.figure(figsize=(12, 6))
    plt.plot(half_freqs, half_fft_mixed)
    plt.title('Widmo amplitudowe mieszaniny sygnałów 50 Hz i 60 Hz')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda')
    plt.xlim(0, fs/2)
    plt.grid()
    plt.show()

    # 4. Powtarzamy eksperymenty dla innej częstotliwości próbkowania
    # Tutaj można ustawić inne wartości `fs` i wygenerować nowe sygnały, 
    # jednak dla uproszczenia tego przykładu pominę ten krok.

    # 5. Odwrotna transformata Fouriera dla sygnału 50 Hz
    ifft_50Hz = np.fft.ifft(fft_50Hz)
    ifft_mixed = np.fft.ifft(fft_mixed)

    # Porównanie sygnałów oryginalnych i otrzymanych przez IFFT
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, signal_50Hz, label='Oryginalny sygnał 50 Hz')
    plt.plot(t, ifft_50Hz.real, label='Sygnał po IFFT', linestyle='--')
    plt.title('Porównanie sygnałów 50 Hz')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t, mixed_signal, label='Oryginalna mieszanina sygnałów')
    plt.plot(t, ifft_mixed.real, label='Mieszanina sygnałów po IFFT', linestyle='--')
    plt.title('Porównanie mieszaniny sygnałów')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()




