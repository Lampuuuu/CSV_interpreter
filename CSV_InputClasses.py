import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import numpy as np

# Basisklasse für den Dateiinput
class InputClass:
    def __init__(self):
        # Ruft <input_filename()> - Funktion auf bei Klasserstellung
        self.input_filename()

    # Dummy-Funktion der Parent-Class 
    def input_filename(self):
        return "THIS IS THE PARENT CLASS"
        
    # Setter-Funktion für den Dateinamen
    def set_filename(self, filename):
        self.__filename = filename

    # Getter-Funktion für den Dateinamen
    def get_filename(self):
        return self.__filename  

    # Check-Funktion zur Überprüfung, ob der Dateiname im System gefunden werden kann
    def check_file(self, filename):
        # Erzeugt Fehlermeldungen, falls Datei nicht gefunden werden konnte,
        # oder falls es sich bei der gewählten Datei nicht um eine CSV-Datei handelt.
        if not os.path.isfile(filename):
            raise Exception("Datei konnte nicht gefunden werden")
        elif filename[-3:].lower() != "csv":
            raise Exception("Es handelt sich bei der Datei um keine CSV")
        else:
            print("Dateieingabe korrekt!")

    def get_input_file(self):
        print("\nGET INPUT FILE\n")
        try: 
            self.check_file(self.__filename)
            return self.__filename
        except Exception as e:
            print(f"{e}")
    


    
class TextInput(InputClass):

    def input_filename(self):
        loop = True
        while loop:
            try:
                filename = input("Bitte geben Sie hier den genauen Dateistring an: ")
                self.check_file(filename)
                self.set_filename(filename)
            except Exception as e:
                print(e)

                if input("\nFalsche Eingabe. Wiederholen? (j/n)").lower() != "j":
                    loop = False

    

class GUI_Input(InputClass):
    
    # Fenster initialisieren
    root = tk.Tk()
    root.title("File Input")
    root.resizable(False, False)
    root.geometry("300x150")

    # Funktion für den Button-Press
    def select_file(self):
        print("\nSELECT FILE\n")
        filetypes = (
        ("csv files", "*.csv"),
        ("All files", "*.*")
        )

        filename = fd.askopenfilename(
            title="Open file",
            #initialdir="/",
            filetypes=filetypes)

        showinfo(
            title="Selected File",
            message=filename
        )
        self.set_filename(filename)
        self.root.destroy()
    
    
    def input_filename(self):
        print("\n INPUT FILENAME \n")
        try:
            open_button = ttk.Button(
                self.root,
                text="Open a File",
                command=self.select_file
            )
            open_button.pack(expand=True)

            self.root.mainloop()
            print(self.get_filename())


        except Exception as e:
            print(e)
            



class AnzeigeFenster():
    __plot_choices = ["plot (x,y)", "boxplot", "step-plot", "histogram", "scatterplot"]


    def set_data_x(self, text):
        self.data_label_x = tk.Label(self.data_choice_frame, text=text)
        self.data_label_x.grid(row=0, column=0, sticky="W E")

        self.data_var_x = tk.StringVar(self.data_choice_frame, "Auswählen")
        self.data_menu_x = tk.OptionMenu(self.data_choice_frame, self.data_var_x, *self.df.columns)
        self.data_menu_x.grid(row=0, column=1, sticky="W E")

    def set_data_y(self, text):
        self.data_label_y = tk.Label(self.data_choice_frame, text=text)
        self.data_label_y.grid(row=1, column=0, sticky="W E")

        self.data_var_y = tk.StringVar(self.data_choice_frame, "Auswählen")
        self.data_menu_x = tk.OptionMenu(self.data_choice_frame, self.data_var_y, *self.df.columns)
        self.data_menu_x.grid(row=1, column=1, sticky="W E")

    def plot_data(self):
        print("PLOT DATA!!!")
        print(f'pcv = {self.plot_choice_var.get()}')
        print(f'pdv_x = {self.data_var_x.get()}')
        self.fig = Figure(figsize=(5, 4), dpi=150)
        self.ax = self.fig.add_subplot()

        try:
            series_x = self.df[self.data_var_x.get()]
            series_y = self.df[self.data_var_y.get()]
            self.ax.set_xlabel(self.data_var_x.get())
            self.ax.set_ylabel(self.data_var_y.get())
        except:
            try:
                series_x = self.df[self.data_var_x.get()]
                self.ax.set_title(self.data_var_x.get())
            except:
                tk.messagebox.showinfo(title="FEHLER", message="keine Daten ausgewählt")
                return


        try:
            if self.plot_choice_var.get() == "plot (x,y)":
                self.ax.plot(series_x, series_y)
                

            elif self.plot_choice_var.get() == "boxplot":
                self.ax.boxplot(series_x.dropna())
                

            elif self.plot_choice_var.get() == "histogram":
                self.ax.hist(series_x)
                
            elif self.plot_choice_var.get() == "scatterplot":
                self.ax.scatter(series_x, series_y)


            elif self.plot_choice_var.get() == "step-plot":
                self.ax.step(series_x, series_y) 
            else:
                tk.messagebox.showinfo(title="Fehler", message="Ein unerwarteter Fehler ist aufgetreten")
                return

        except Exception as e:
            tk.messagebox.showinfo(
                title="FEHLER",
                message=f'Ein Fehler ist aufgetreten.\nFehlermeldung:\n{e}'
            )
            return
        
        self.plot_window = tk.Tk()
        
        if self.plot_choice_var.get() in ["plot (x,y)", "scatterplot", "step-plot"]:
            self.plot_window.title(f'{self.plot_choice_var.get()}: {self.data_var_x.get()} {self.data_var_y.get()}')
        else:
            self.plot_window.title(f'{self.plot_choice_var.get()}: {self.data_var_x.get()}')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_window)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_window, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=20)
        try:
            self.plot_window.mainloop()
        except Exception as e:
            tk.messagebox.showinfo(
                title="FEHLER",
                message=f'Ein Fehler ist aufgetreten.\n Fehlermeldung:\n {e}')

        

    def show_data_choices(self):
        plot_type = self.plot_choice_var.get()

        # falls Variable noch nicht existiert
        try:
            self.data_choice_frame.forget()
            self.plot_button.forget()
            self.data_choice_frame = tk.Frame(self.root)
        except:
            self.data_choice_frame = tk.Frame(self.root)


            
        if plot_type in ["histogram", "boxplot"]:
            self.set_data_x(text="Datensatz")


        elif plot_type in ["plot (x,y)", "scatterplot", "step-plot"]:
            self.set_data_x(text="Datensatz X:")
            self.set_data_y(text="Datensatz Y:")

        
        else:
            tk.messagebox.showinfo(title="Fehler", message="keine Auswahl getroffen")
            return

        

        self.plot_button = tk.Button(self.root, text="plotten", font=("Arial", 14, "bold"), command=self.plot_data)

        self.data_choice_frame.pack()
        self.plot_button.pack(padx=10, pady=20)

    def __init__(self, df):
        self.root = tk.Tk()
        self.root.title("Anzeigefenster")
        self.root.attributes("-topmost", True)
        self.df = df

        # Auswahl des Plots treffen
        self.plot_choice_frame = tk.Frame(self.root)
        self.plot_choice_frame.columnconfigure(0, weight=1)

        self.plot_choice_label = tk.Label(
            self.plot_choice_frame, 
            text="Art des Diagramms:",
            font=("Arial", 12))
        self.plot_choice_label.grid(row=0, column=0, sticky="W E", padx=5)

        # Button zum bestätigen
        self.plot_choice_var = tk.StringVar(self.plot_choice_frame, "Auswählen")
        self.plot_choice_menu = tk.OptionMenu(self.plot_choice_frame, self.plot_choice_var, *self.__plot_choices)
        self.plot_choice_menu.grid(row=0, column=1, sticky="W E")

        self.plot_choice_button = tk.Button(
            self.plot_choice_frame, 
            text="OK", 
            font=("Arial", 12, "bold"), 
            command=self.show_data_choices)
        self.plot_choice_button.grid(row=0, column=2, padx=10, pady=10)

        self.plot_choice_frame.pack(padx=10, pady=20)
        

        self.root.mainloop()


def main():
    csv_input = GUI_Input()
    csv_filestring = csv_input.get_filename()
    showinfo(
        title="Import", 
        message=("Das Einlesen der Datei beginnt nun\n"
                 "dieser Prozess kann einige Sekunden in Anspruch nehmen.\n"
                 "Sobald dies vollzogen ist, öffnet sich ein neues Fenster."))
    
    standard_seps = [",", ";", "-", "\t", "^"]
    for sep in standard_seps:
        try:
            csv_df = pd.read_csv(csv_filestring, sep=sep)
            break
        except:
            continue
    plot_window = AnzeigeFenster(csv_df)

if __name__ == "__main__":
    main()



