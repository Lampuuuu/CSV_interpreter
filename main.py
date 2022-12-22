import CSV_InputClasses
import CSV_interpreter
import CSV_OptionsInterface



def main():
    Eingabe = CSV_InputClasses.TextInput()
    dateiname = Eingabe.get_input()

    interpreter = CSV_verarbeiter(dateiname)
    csv_dataframe = CSV_interpreter.get_df()

    # Dict mit Optionen für jeweilige Spalte?!
    # erstmal optional
    display_options = interpreter.get_options() 


    OptionsInterface = CSV_OptionsInterface(csv_dataframe, display_options)
    OptionsInterface.run()



