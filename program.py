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

        

    

def zadanie1(freq,filename, hasFirstTime):
    if freq>=0 :
        if not readFile(freq, filename, hasFirstTime):
             messagebox.showinfo(message="Wybrany plik jest niepoprawny") 
        else:
             return plotEKG()
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
    plt.xlim(left=bottomLimmit/fs, right=upperLimit/fs)
    plt.show()
    return True


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()




