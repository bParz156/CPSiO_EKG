import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import time

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
            else:
                page.pack_forget()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text="Przetwarzanie i analiza sygnału EKG", font=("Helvetica", 18))
        self.label.pack(pady=10)
        label = tk.Label(self, text="Barbara Parzonka i Joanna Zaglowek", font=("Helvetica", 12))
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

            label1 = tk.Label(container, text="Podaj czestotliwosc probkowania sygnalu", font=("Helvetica", 18))
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

            self.button = tk.Button(container, text="Update Label", command=self.update_label)
            self.button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)


    def updateLabelText(self,pagename, newtex):
            self.master.pages[pagename].label.config(text=newtex)

    def update_label(self):
        new_text = self.entry1.get()+" "+self.entry2.get()+" "+str(self.checkbox_var.get())
        self.master.pages["page_1"].label.config(text=new_text)
        zadanie1(int(self.entry1.get()),self.entry2.get(),self.checkbox_var.get())

    


def zadanie1(freq,filename, hasFirstTime):
        if freq>=0 :
            while (not readFile(freq,filename, hasFirstTime)):
                Page.updateLabelText(pagename="page_1",newtex="Zły plik")
                print("Podany plik stwarza problemu, podaj inny plik")
                filename=input("Podaj nazwę pliku (Z ROZSZERZENIEM), z którego mają zostać wczytane dane \n")
                while True:
                    samplingFrequency=int(input("Podaj częstotliwość próbkowanie sygnału EKG \n"))
                    if samplingFrequency>=0:
                        break
                    else: 
                        print("Częstotliwość musi być dodatnią liczbą całkowitą!")
                        continue
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


        """filename - name of the file from which the EKG signals is read
    isFirstValid - the information whatever th first column is valid as x-array or if that's time
    """

xarray=[]
yarray=[]

def readFile(samplingFrequency,filename, hasFirstTime):
    print(str(samplingFrequency))
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
        print('Zly plik')
        return False

def plotEKG(default_size=100):
    plt.plot(xarray[0:default_size],yarray[0:default_size])
    plt.xlabel('time [s]')
    plt.show()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()




