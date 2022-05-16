from wordle import *
import sys


# <string> doesn't have to be capital.
# TODO: Correct this. Test all appropriate languages, not only English.
def is_valid_language(string: str):
    return string.upper() == "ENGLISH"


def validate_arguments():
    set_parameters_message = "To set the script arguments in PyCharm, press the wrench button below the play button," \
                             "in the Run window.\n" \
                             "There, edit the parameters text field.\n" \
                             "To set the script arguments in the CMD (Command Line)," \
                             "simply enter a line that matches the correct usage."
    invalid_script_run_exception = Exception("Invalid run of the script.\n"
                                             "Correct usage: \"CLI.py <wordsize> (integer) <language> (string)\"\n"
                                             "Example usage: \"CLI.py 5 EnglISH\"" + "\n\n" +
                                             set_parameters_message)
    invalid_language_exception = Exception("Invalid language parameter.\n"
                                           "Valid languages: English" + "\n\n" +  # TODO: Correct this. It's not just English.
                                           set_parameters_message)

    if len(sys.argv[1:]) != 2:
        raise invalid_script_run_exception
    param1 = sys.argv[1]
    param2 = sys.argv[2]
    if not param1.isnumeric():
        raise invalid_script_run_exception
    if not param2.isalpha():
        raise invalid_script_run_exception
    elif not is_valid_language(param2):
        raise invalid_language_exception


def start_cli_loop():
    quitInputs = ["quit", "q", "exit", "finish", "done"]
    while input().lower() not in quitInputs:
        print("Cool")  # TODO


def main():
    validate_arguments()

    solver = Keyboard()  # TODO: Change this to WordleSolver, when merging. Keyboard is no longer the correct class.
    solver.guess_word("hello", "bbbbb")
    print(solver.possible_words())
    print(solver.completely_new_words())
    start_cli_loop()

main()
