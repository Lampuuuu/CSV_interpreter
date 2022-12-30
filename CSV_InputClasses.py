import os
import tkinter

class InputClass:
    __filestring = ""

    def get_filestring(self):
        return self.__filestring  

    def check_file(self):
        if not os.path.isfile(self.__filestring):
            raise Exception("Datei konnte nicht gefunden werden")

    def get_input_file(self):
        try: 
            self.check_file()
            return self.__filestring
        except Exception as e:
            print(f"{e}")

    
class TextInput(InputClass):

    def __init__(self):
        self.__filestring = input("Bitte geben Sie den genauen Dateistring der CSV-Datei an:\n")


class GUI_Input(InputClass):
    def __init__(self):
        pass

def main():
    csv_input = TextInput()
    csv_string = csv_input.get_input_file()
    print(csv_string)

if __name__ == "__main__":
    main()