import os
import tkinter as tk


class InputClass:
    
    def __init__(self):
        self.input_filename()

    def get_filestring(self):
        return self.__filename  

    def set_filestring(self, filename):
        self.__filename = filename

    def check_file(self, filename):
        if not os.path.isfile(filename):
            raise Exception("Datei konnte nicht gefunden werden")
        elif filename[-3:].lower() != "csv":
            raise Exception("Es handelt sich bei der Datei um keine CSV")
        else:
            print("Dateieingabe korrekt!")

    def get_input_file(self):
        try: 
            self.check_file()
            return self.__filename
        except Exception as e:
            print(f"{e}")
    
    def input_filename(self):
        self.set_filestring("THIS IS THE WRONG CLASS")
    
class TextInput(InputClass):

    def __init__(self):
        self.__filename = input("Bitte geben Sie den genauen Dateistring der CSV-Datei an:\n")


class GUI_Input(InputClass):
    InputWindow = tk.TK()
    InputWindow.title("Dateieingabe")
    InputWindow.resizable(False, False)
    InputWindow.geometry("300x150")



def main():
    csv_input = TextInput()
    csv_string = csv_input.get_input_file()
    print(csv_string)

if __name__ == "__main__":
    main()