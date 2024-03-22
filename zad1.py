"""
Ponizszy program jest wynikiem pracy zespolu: Barbara Parzonka i Joanna Zoglowek 
w ramach zajec laboratoryjnych z przedmiotu Cyfrowe Przetwarzanie Sygnalow i Obrazow pod opieka doktora Jerzego Cichosza
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk,Image
from tkinter import Scrollbar
"""
Kolejne zmienne globalne to:
xarray - wektor argumentow, czas pomiaru
yarray -  wektor/tablica wartosci (w zaleznosci od liczby elektrod dostarczajacych informacji o pacjencie) 
fs- czestotliwosc probkowania
numberofCases - liczba elektrod (wektorow wartosci odpowiadajacych podanemu wektowi argumentow)
"""
xarray = []
valuesArray = []
fs = None
numberOfCases = 1
"""
Klasa SampleApp jest odpowiedzialna za podstawowe GUI, wyswietlenie okna aplikacji, ktore nastepnie jest obudowywane przez pozostale klasy
"""
class SampleApp(tk.Tk):
    def __init__(self):
        width = 800
        height = 600
        tk.Tk.__init__(self)
        self.title("Cyfrowe Przetwarzanie Sygnałów i Obrazów")
        self.geometry(str(width) + "x" + str(height))
        self.pages = {}

        main_page = MainPage(self)
        self.add_page("main_page", main_page)

        for i in range(1, 5):
            page = Page(self, f"Page {i}")
            self.add_page(f"page_{i}", page)

        self.show_page("main_page")

    def add_page(self, name, page):
        self.pages[name] = page

    def show_page(self, name):
        for page_name, page in self.pages.items():
            if page_name == name:
                page.pack(fill="both", expand=True)
                if name=="page_1":
                    Page.reset_options(page)
            else:
                page.pack_forget()
"""
Podstawowa strona aplikacji pozwala na poruszanie sie w aplikacji - wlaczanie programow odpowiedzialnych za poszczegolne zadania
"""
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
            #Pierwsza kolumna powinna stanowic min 15% calkowitej szerokosci
            container.grid_columnconfigure(0, weight=1, minsize=int(master.winfo_width() * 0.15), )

            label1 = tk.Label(container, text="Podaj czestotliwosc probkowania sygnalu (Hz)", font=("Helvetica", 18))
            label1.grid(row=0, column=0, sticky='w', padx=10, pady=5)
            self.entry1 = tk.Entry(container)
            self.entry1.grid(row=0, column=1, columnspan=1, padx=10, pady=5)

            label2 = tk.Label(container, text="Podaj nazwe pliku z danymi (z roszerzeniem)", font=("Helvetica", 18))
            label2.grid(row=1, column=0, sticky='w', padx=10, pady=5)
            self.entryFileName = tk.Entry(container)
            self.entryFileName.grid(row=1, column=1, columnspan=1, padx=10, pady=5)

            self.buttonChoseFile=tk.Button(container,text="Wybierz plik", command=self.chooseFile)
            self.buttonChoseFile.grid(row=1, column=3)


            self.checkbox_var = tk.BooleanVar()
            self.checkbox = tk.Checkbutton(container, text="Zaznacz jesli pierwsza kolumna zawiera czas",
                                           variable=self.checkbox_var)
            self.checkbox.grid(row=2, column=0, columnspan=1, sticky='w', padx=10, pady=5)

            self.button = tk.Button(container, text="Wyświetl wykres",
                                    command=lambda: self.plotChartButtonCLicked())
            self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

            self.labelBottom = tk.Label(container, text="Podaj dolny ogranicznik czasu", font=("Helvetica", 18))
            self.labelBottom.grid_forget()
            self.entryBottomLimit = tk.Entry(container)
            self.entryBottomLimit.grid_forget()

            self.labelUpper = tk.Label(container, text="Podaj górny ogranicznik czasu", font=("Helvetica", 18))
            self.labelUpper.grid_forget()
            self.entryUpperLimit = tk.Entry(container)
            self.entryUpperLimit.grid_forget()

            self.buttonUp = tk.Button(container, text="Aktualizuj wykres", command=self.updatePlot)
            self.buttonUp.grid_forget()
            large_image = tk.PhotoImage(file="test.png")
            self.canvas=tk.Canvas(self)
            self.canvas.pack(side="left", fill="both", expand=True)
            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0,0), window=self.frame, anchor="nw")
            self.image_label = tk.Label(self.frame, image=large_image)
            self.image_label.image = large_image  
            self.image_label.pack()

            self.buttonSave=tk.Button(container,text="Zapisz dane do pliku tekstowego", command=self.save_file_dialog)
            self.buttonSave.grid_forget()
        

    """
    Czyszczenie opcji zaznaczonych/wpisanych w zadaniu 1
    """
    def reset_options(self):
        self.entry1.delete(0, tk.END)  
        self.entryFileName.delete(0, tk.END)  
        self.checkbox_var.set(False)  
        self.labelBottom.grid_forget()
        self.entryBottomLimit.grid_forget()
        self.labelUpper.grid_forget()
        self.entryUpperLimit.grid_forget()
        self.buttonUp.grid_forget()
        self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)  
        large_image = tk.PhotoImage(file="test.png")
        self.image_label.configure(image=large_image)
        self.image_label.image = large_image 
        self.entryBottomLimit.delete(0, tk.END)
        self.entryUpperLimit.delete(0, tk.END)
        self.buttonSave.grid_forget()
            
        """
        Pokazanie dodatkowych opcji jakie mozna wykonac na wyswietlanym wykresie
        """
    def show_option(self):
        self.labelBottom.grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.labelUpper.grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entryBottomLimit.grid(row=6, column=1, columnspan=1, padx=10, pady=5)
        self.entryUpperLimit.grid(row=7, column=1, columnspan=1, padx=10, pady=5)
        self.buttonUp.grid(row=8, column=0, columnspan=1, padx=10, pady=10)
        self.button.grid_forget()
        self.buttonSave.grid(row=9, column=3, columnspan=1, padx=10, pady=10)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        large_image = tk.PhotoImage(file="chart.png")
        self.image_label.configure(image=large_image)
        self.image_label.image = large_image 
        self.image_label.pack()
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
        
    def plotChartButtonCLicked(self):
        global fs
        ok=True
        try:
            fs=int(self.entry1.get())
        except:
            answer=messagebox.askquestion(title= "Brak podanej częstotliwośći",message= "Nie podano częstotliwości. Czy chcesz przyjąć, że częstotliwość to 100 Hz?")
            ok=answer==messagebox.YES

        if ok:
            if zadanie1(fs,self.entryFileName.get(),self.checkbox_var.get()):
                self.show_option()

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
            img = ImageTk.PhotoImage(Image.open("chart.png"))
            self.image_label.configure(image=img)
            self.image_label.image=img

    def save_file_dialog(self):
        global fs
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            upperLimit=len(xarray)
            bottomLimmit=0
            if self.entryUpperLimit.get()!="":
                upperLimit=int(float(self.entryUpperLimit.get())*fs)
            if self.entryBottomLimit.get()!="":
                bottomLimmit=int(float(self.entryBottomLimit.get())*fs)
            with open(file_path, "w") as file:
                for i in range (bottomLimmit,upperLimit):
                    pom=''
                    for j in range(numberOfCases):
                        pom+=str(int(valuesArray[j][i]))+" "
                    file.write(pom+"\n")

            messagebox.showinfo("Zapisano plik!", f"Sciezka to: {file_path}")

    def chooseFile(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        self.entryFileName.insert(index=0,string=file_path)
            

def zadanie1(freq,filename, hasFirstTime):
    if freq>=0 :
        if not readFile(freq, filename, hasFirstTime):
             messagebox.showinfo(message="Wybrany plik jest niepoprawny") 
        else:
             return plotEKG()
    else:
        messagebox.showinfo(message="Czestotliwość musi być liczbą dodatnią")
    return False

def readFile(samplingFrequency, filename, hasFirstTime):
    timePeriod = 1 / samplingFrequency
    global xarray, valuesArray, numberOfCases
    xarray.clear()
    valuesArray.clear()

    try:
        with open(filename, 'r') as file:
            for line in file:
                columns = line.split()
                if hasFirstTime and len(columns) > 1:
                    xarray.append(float(columns[0]))
                    columns = columns[1:]  # Usun istniejaca kolumne
                else:
                    xarray.append(len(xarray) * timePeriod)
                
                for i, value in enumerate(columns):
                    if len(valuesArray) <= i:
                        valuesArray.append([])  #Stworz nowa liste
                    valuesArray[i].append(float(value))
                    
        numberOfCases = len(valuesArray)
        return True
    except Exception as e:
        messagebox.showerror("Błąd odczytu pliku", str(e))
        return False

def plotEKG(bottomLimmit=0, upperLimit=None):
    if upperLimit is None:
        upperLimit = len(xarray)
    
    plt.figure(figsize=(15, 2 * numberOfCases))  # Ustawienie większego rozmiaru figury
    plt.subplots_adjust(hspace=1.0)  # Większe odstępy między wykresami
    
    for i in range(numberOfCases):
        plt.subplot(numberOfCases, 1, i+1)
        plt.plot(xarray[bottomLimmit:upperLimit], valuesArray[i][bottomLimmit:upperLimit], label=f'Sygnał {i+1}')
        plt.xlabel('Czas [s]')
        if i== int(numberOfCases/2):
            plt.ylabel('Amplituda [mV]')
        plt.legend(loc='upper right')
        plt.grid(True)
    
    plt.tight_layout()  # Automatyczna regulacja odstępów
    plt.savefig(fname="chart.png")
    return True


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()