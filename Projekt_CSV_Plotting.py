import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd

"""
Diese Datei beinhaltet Klassen zur Auswahl einer Datei auf der lokalen Maschine (via Text und GUI-Input),
sowie eine Klasse zum plotten sämtlicher Spalten eines Pandas-Dataframes über die typischen Plot-Typen:
    * XY-Plot
    * Scatterplot
    * Histogram
    * Boxplot
    * Step-plot

Zusätzlich ein kleines Programm in der <main>-Funktion, welches die GUI-Inputklasse, 
sowie die GUI-Plotklasse miteinander Verknüpft und so ein komplettes Bild abgibt.

Was dieses Programm leisten Soll:
    * Die Möglichkeit bieten schnell die Daten einer CSV in einem Standard-Plot grafisch darzustellen
    * Mithilfe der Plots einen Groben Überblick über die Daten zu erhalten.
    * Eine Möglichkeit zur Kontrolle der Plausibilität präziserer Plots bieten

Was dieses Programm nicht leisten Soll:
    * Präsentierbereite Plots liefern, die genau so abgespeichert und in eine Veröffentlichung fließen sollen.
    * Immer logische und nachvollziehbare Plots liefern
        ** dies hängt vor allem an der Kompetenz des Benutzers
        ** Sowie an den Daten der CSV

Der Code an welchem sich für dieses Programm orientiert wurde ist im Ordner <Quellen> abgelegt.
Die Zugehörige Quelle steht dabei immer im Markdown-Feld über dem jeweiligen Code-Snippet.
"""

class InputClass:
    """
    Parent-Class
    """
    def __init__(self):
        # Ruft <input_filename()> - Funktion auf bei Klasserstellung
        self.input_filename()


    def input_filename(self):
        """Dummy-Funktion der Parent-Class"""
        return "DIES IST DIE PARENT-KLASSE"


    def set_filename(self, filename):
        """Setter-Funktion für den Dateinamen"""
        self.__filename = filename


    def get_filename(self):
        """Getter-Funktion für den Dateinamen"""
        return self.__filename


    def check_file(self, filename):
        """Check-Funktion zur Überprüfung, ob der Dateiname im System gefunden werden kann"""
        # Erzeugt Fehlermeldungen, falls Datei nicht gefunden werden konnte,
        if not os.path.isfile(filename):
            raise Exception("Datei konnte nicht gefunden werden")

        # oder falls es sich bei der gewählten Datei nicht um eine CSV-Datei handelt.
        if filename[-3:].lower() != "csv":
            raise Exception("Es handelt sich bei der Datei um keine CSV")

        print("Dateieingabe korrekt!")


    def get_input_file(self):
        """Funktion zur Überprüfung und Rückgabe der Datei"""
        try:
            self.check_file(self.__filename)
            return self.__filename
        except Exception as e:
            print(f"{e}")


class TextInput(InputClass):
    """Textinput-Klasse auf Basis der Input-Klasse"""

    # input_filename() loopt so lange keine korrekte Datei im Input angegeben wird.
    def input_filename(self):
        loop = True
        while loop:
            try:
                filename = input("Bitte geben Sie hier den genauen Dateistring an: ")
                self.check_file(filename)
                self.set_filename(filename)
            except Exception as e:
                print(e)

                if input("Falsche Eingabe. Wiederholen? (j/n)").lower() != "j":
                    loop = False


class GUI_Input(InputClass):
    """GUI-Dateiinput-Klasse basierend auf InputClass"""

    # Fenster Initialisieren
    root = tk.Tk()
    root.title("File Input")
    root.resizable(False, False)
    root.geometry("300x150")

    # Funktion für den Button-Press
    def select_file(self):
        """Dateiauswahl über auswahlfenster"""

        filetypes = (
            ("csv files", "*.csv"),
            ("All files", "*.*")
            )

        # erlaubt auswahl zwischen entweder csv-Dateien 
        # oder Dateien aller Dateitypen über die Variable <filetypes>
        filename = fd.askopenfilename(
            title="Open file",
            filetypes=filetypes)

        # Anzeigefenster für die Ausgewählte Datei
        showinfo(
            title="Ausgewählte Datei",
            message=f'Ausgewählte Datei:\n{filename}'
        )

        # Filename der Klasse anpassen
        self.set_filename(filename)

        # Fenster schließen
        self.root.destroy()


    def input_filename(self):

        try:
            # Button im Hauptfenster, der die <select_file>-Funktion auslöst
            open_button = ttk.Button(
                self.root,
                text="Datei auswählen",
                command=self.select_file,
            )
            open_button.pack(expand=True)

            self.root.mainloop()
            print(self.get_filename())

        except Exception as e:
            showinfo(title="Fehler", message=e)


class AuswahlFenster():
    """
    Anzeigefenster, dass durch den Input eines Dataframes die graphische Darstellung einer
    oder mehrerer Spalten dieses Dataframes über verschiedene Plots ermöglicht.
    """

    # Liste zur Auswahl der möglichen plots
    #   (könnte durch weitere Implementierung von features erweitert werden)
    __plot_choices = ["plot (x,y)", "boxplot", "step-plot", "histogram", "scatterplot"]

    def __init__(self, df:pd.DataFrame):
        """
        erwartet als input einen Pandas Dataframe, aus welchem Daten entzogen 
        und graphisch in verschiedenen Fromendargestellt werden können
        """

        self.root = tk.Tk()
        self.root.title("Auswahlfenster")

        # sorgt dafür, dass das Fenster immer im Vordergrund auftaucht
        self.root.attributes("-topmost", True)

        self.df = df

        # Frame zur Auswahl des plots
        self.plot_choice_frame = tk.Frame(self.root)
        self.plot_choice_frame.columnconfigure(0, weight=1)

        # Label zur Beschriftung an Position |x|_|_| des Frames
        self.plot_choice_label = tk.Label(
            self.plot_choice_frame,
            text="Art des Diagramms:",
            font=("Arial", 12))
        self.plot_choice_label.grid(row=0, column=0, sticky="W E", padx=5)

        # Auswahlmenü zur Auswahl des Plot-Typs an Position |_|x|_| des Frames
        self.plot_choice_var = tk.StringVar(self.plot_choice_frame, "Auswählen")
        self.plot_choice_menu = tk.OptionMenu(
            self.plot_choice_frame,
            self.plot_choice_var,
            *self.__plot_choices)
        self.plot_choice_menu.grid(row=0, column=1, sticky="W E")

        # Button zur Bestätigung der Auswahl an Position |_|_|x| des Frames 
        # Zeigt nach dem Drücken die zum Plot passenden Auswahlfenster im Hauptfenster an
        self.plot_choice_button = tk.Button(
            self.plot_choice_frame,
            text="OK",
            font=("Arial", 12, "bold"),
            command=self.show_data_choices)
        self.plot_choice_button.grid(row=0, column=2, padx=10, pady=10)

        # packing des Frames in das Auswahlfenster
        self.plot_choice_frame.pack(padx=10, pady=20)

        # Mainloop des Auswahlfensters
        self.root.mainloop()


    def set_data_x(self, text):
        """Funktion zur erstelleung des X-Labels und Dropdown-Menüs der Datensatzauswahl"""

        self.data_label_x = tk.Label(self.data_choice_frame, text=text)
        self.data_label_x.grid(row=0, column=0, sticky="W E")

        self.data_var_x = tk.StringVar(self.data_choice_frame, "Auswählen")
        self.data_menu_x = tk.OptionMenu(self.data_choice_frame, self.data_var_x, *self.df.columns)
        self.data_menu_x.grid(row=0, column=1, sticky="W E")

    def set_data_y(self, text):
        """Funktion zur erstelleung des Y-Labels und Dropdown-Menüs der Datensatzauswahl"""

        self.data_label_y = tk.Label(self.data_choice_frame, text=text)
        self.data_label_y.grid(row=1, column=0, sticky="W E")

        self.data_var_y = tk.StringVar(self.data_choice_frame, "Auswählen")
        self.data_menu_x = tk.OptionMenu(self.data_choice_frame, self.data_var_y, *self.df.columns)
        self.data_menu_x.grid(row=1, column=1, sticky="W E")


    def show_data_choices(self):
        """Zeigt Auswahl für Datensatz basierend auf der getroffenen Wahl des Plots an"""
    
        plot_type = self.plot_choice_var.get()

        # Exception Handler zum Löschen und Erstellen des data_choice_frame
        try:
            self.data_choice_frame.forget()
            self.plot_button.forget()
            self.data_choice_frame = tk.Frame(self.root)
        except:
            self.data_choice_frame = tk.Frame(self.root)

        # Beim Histogramm und beim Boxplot wird lediglich eine Spalte benötigt
        if plot_type in ["histogram", "boxplot"]:
            self.set_data_x(text="Datensatz")

        # Boxplot, Scatterplot und Step-plot sind zweidimensional
        elif plot_type in ["plot (x,y)", "scatterplot", "step-plot"]:
            self.set_data_x(text="Datensatz X:")
            self.set_data_y(text="Datensatz Y:")

        else:
            # Fehlermeldung bei nicht getroffener Auswahl
            tk.messagebox.showinfo(title="Fehler", message="keine Auswahl getroffen")
            return

        self.plot_button = tk.Button(self.root, text="plotten", font=("Arial", 14, "bold"), command=self.plot_data)

        self.data_choice_frame.pack()
        self.plot_button.pack(padx=10, pady=20)

    def plot_data(self):
        """
        Erstellung des Plots in neuem Fenster nach Knopfdruck.
        Geschieht auf basis der in den Dropdownmenüs festgelegten StringVars:
            <data_var_x>; <data_var_y>; <plot_choice_var>
        """

        # Erstellung einer leeren Figure, in die unser plot gelegt wird
        self.fig = Figure(figsize=(5, 4), dpi=150)
        self.ax = self.fig.add_subplot()

        # Überprüfung, ob in den Optionsmenüs etwas ausgewählt wurde mit anschließender Fehlermeldung
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

        # Plotting der jeweiligen plots auf den Subplot <self.ax>
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
                showinfo(title="Fehler", message="Ein unerwarteter Fehler ist aufgetreten")
                return

        # Fehlermeldung
        except Exception as e:
            tk.messagebox.showinfo(
                title="FEHLER",
                message=f'Ein Fehler ist aufgetreten.\nFehlermeldung:\n{e}'
            )
            return

        # Erstellen eines neuen Fensters, in welchem der Plot angezeigt werden soll
        self.plot_window = tk.Tk()

        # Je nach Auswahl des Plots: Anpassung des Titels
        if self.plot_choice_var.get() in ["plot (x,y)", "scatterplot", "step-plot"]:
            self.plot_window.title(f'{self.plot_choice_var.get()}: {self.data_var_x.get()} {self.data_var_y.get()}')
        else:
            self.plot_window.title(f'{self.plot_choice_var.get()}: {self.data_var_x.get()}')

        # Hinzufügen der erstellten Figure auf eine für tkinter angepassten canvas via
        #   <FigureCanvasTkAgg>
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_window)
        self.canvas.draw()

        # Toolbar zur navigation in dem erstellten Graphen
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_window, pack_toolbar=False)
        self.toolbar.update()

        # Packing von toolbar und Canvas ins Fenster
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=20)

        # Fetching von Fehlern
        try:
            self.plot_window.mainloop()
        except Exception as e:
            tk.messagebox.showinfo(
                title="FEHLER",
                message=f'Ein Fehler ist aufgetreten.\n Fehlermeldung:\n {e}')

        





def main():
    """main"""

    # Erstellen des GUI-Inputs <csv_input>
    csv_input = GUI_Input()

    # Abspeichern des Dateinamen in <csv_filestring>
    csv_filestring = csv_input.get_filename()

    # Information des Nutzers
    showinfo(
        title="Import", 
        message=("Das Einlesen der Datei beginnt nun\n"
                 "dieser Prozess kann einige Sekunden in Anspruch nehmen.\n"
                 "Sobald dies vollzogen ist, öffnet sich ein neues Fenster."))

    standard_seps = [",", ";", "-", "\t", "^"]

    # Überprüfung der Standard-Separatoren von csv-files 
    #   (sollte normalerweise auf ";" & "," beschränkt sein)
    # Und einladen in einen Pandas-Dataframe
    for sep in standard_seps:
        try:
            csv_df = pd.read_csv(csv_filestring, sep=sep)
            break
        except:
            continue

    # Aufrufen eines Auswahlfensters mit unserem Dataframe
    AuswahlFenster(csv_df)

if __name__ == "__main__":
    main()