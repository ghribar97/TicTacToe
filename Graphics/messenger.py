import tkinter.messagebox as mb
import Common.functions as functions


class SendToUser:
    @staticmethod
    def ask_for_new_game(text):
        if functions.is_string(text):
            return mb.askyesno("Game is over!", text + "\nDo you want to play another game?")
        raise ValueError(str(text) + " is not a string!")

    @staticmethod
    def error(text):
        if functions.is_string(text):
            mb.showerror("Error!", text)
            return True
        raise ValueError(str(text) + " is not a string!")

    @staticmethod
    def go_back(title, text):
        if functions.is_string(title) and functions.is_string(text):
            mb.showinfo(title, text)
            return True
        raise ValueError(str(text) + " or " + str(title) + " is not a string!")

    @staticmethod
    def ask_for_field_change(text):
        if functions.is_string(text):
            return mb.askyesno("Request from opponent", text)
        raise ValueError(str(text) + " is not a string!")

    @staticmethod
    def show_info(title, text):
        if functions.is_string(title) and functions.is_string(text):
            mb.showinfo(title, text)
            return True
        raise ValueError(str(text) + " is not a string!")
