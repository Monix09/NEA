# import modules
import tkinter
from tkinter import *
import mysql.connector
import time

# connecting to the database
db = mysql.connector.connect(host="localhost", port='3306', user="root", passwd="Bella72006!",
                             database="maze_of_madness_data_base", charset='utf8mb4')
mycur = db.cursor()

BLACK = "#000000"
WHITE = "#FFFFFF"
GREEN = "#55FF55"
FONT_NAME = "Courier"
INSTRUCTIONS = "•Use the ⬆,⬇,⬅,➡ buttons to move through the maze" \
               "\n•reach the exit as quick as possible to gain points" \
               "\n•retracing your steps will result in a deduction of points" \
               "\n•falling into a trap the game will send you back to the starting position " \
               "\n•game is over when you reach the exit or if the timer runs out"


class GameStart(Tk):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        if self.logged_in is True:
            self.destroy()
        self.title('Start Menu')
        self.config(padx=300, pady=300, bg=BLACK)
        Label(self, text='Maze Of Madness', bg=BLACK, fg=GREEN, font=(FONT_NAME, 50, 'bold')).grid(row=0, column=0,
                                                                                                   pady=(0, 20))

        # Exit Game Button
        button3 = Button(self, text='Exit Game', highlightthickness=0, command=self.destroy)
        button3.config(width=6, height=2)
        button3.config(width=10)
        button3.place(x=-200, y=21)

        # Sign Up Button
        button1 = Button(self, text='Sign Up', highlightthickness=0, width=70, command=self.Sign_Up)
        button1.grid(row=2, column=0, pady=10)

        # Log In Button
        button2 = Button(self, text='Log In', highlightthickness=0, width=70, command=self.Log_In)
        button2.grid(row=3, column=0, pady=10)

        Label(self, text="sign up/ log in to play!", font=(FONT_NAME, 20, "bold"), bg=BLACK, fg=GREEN).grid(row=5,
                                                                                                            column=0,
                                                                                                            pady=10)

    class Log_In(tkinter.Toplevel):
        def __init__(self):
            super().__init__()
            self.title("Log In")
            self.config(bg=BLACK)
            self.geometry("300x300")

            Label(self, text="Log-In Portal", fg=GREEN, bg=BLACK, font="bold", width=10).grid(row=0, column=2, padx=50)

            self.__username_varify = StringVar()
            self.__password_varify = StringVar()

            Label(self, text="", bg=BLACK).grid(row=1, column=2)

            Label(self, text="Username :", font="bold", fg=WHITE, bg=BLACK).grid(row=3, column=2)

            self.username_entry = Entry(self, textvariable=self.__username_varify)
            self.username_entry.grid(row=4, column=2)

            Label(self, text="", bg=BLACK).grid(row=5, column=2)

            Label(self, text="Password :", fg=WHITE, bg=BLACK).grid(row=6, column=2)

            self.password_entry = Entry(self, textvariable=self.__password_varify, show="*")
            self.password_entry.grid(row=7, column=2)

            Label(self, text="", bg=BLACK).grid(row=8, column=2)

            Button(self, text="Log-In", bg="red", command=self.login_varify).grid(row=9, column=2)

            Label(self, text="", bg=BLACK)
            button3 = Button(self, text='Back', highlightthickness=0, command=self.destroy)
            button3.config(width=6, height=2)
            button3.grid(row=1, column=0)

        def login_varify(self):
            user_varify = self.__username_varify.get()
            pas_varify = self.__password_varify.get()
            if user_varify == "" or pas_varify == "":
                self.failed()
                return

            sql = "select * from users where username = %s and password = %s"
            user_id_sql = "select user_id from users where username = %s and password = %s"
            mycur.execute(sql, [user_varify, pas_varify])
            results = mycur.fetchall()

            mycur.execute(user_id_sql, [user_varify, pas_varify])
            user_id = mycur.fetchall()
            user_id = user_id

            if results:
                for i in results:
                    self.logged(user_id[0])
                    break
            else:
                self.failed()

        def logged(self, id):
            self.destroy()
            self.log_in_complete(id)

        def failed(self):
            self.title("Invalid")
            Label(self, text="Invalid credentials...", bg=BLACK, fg="red", font="bold").grid(row=10, column=2)
            self.username_entry.config(bg="red")
            self.password_entry.config(bg="red")

        def log_in_complete(self, user_id):
            global game_play
            global log_in_ui
            log_in_ui.destroy()
            from ui_setup import start_game_play
            start_game_play(user_id)

    class Sign_Up(tkinter.Toplevel):
        def __init__(self):
            super().__init__()
            self.error_label = None
            self.__password_info = None
            self.__username_info = None
            self.title("Sign Up Portal")
            self.config(bg=BLACK)
            self.geometry("300x300")

            Label(self, text="SignUp Portal", fg=GREEN, bg=BLACK, font="bold", width=10).grid(row=0, column=2, padx=50)

            self.__username = StringVar()
            self.__password = StringVar()

            Label(self, text="", bg=BLACK).grid(row=1, column=2)

            Label(self, text="", bg=BLACK).grid(row=4, column=2)
            Label(self, text="Username :", font="bold", fg=WHITE, bg=BLACK).grid(row=5, column=2)

            self.username_entry = Entry(self, textvariable=self.__username)
            self.username_entry.grid(row=6, column=2)

            Label(self, text="", bg=BLACK).grid(row=7, column=2)

            Label(self, text="Password :", fg=WHITE, bg=BLACK).grid(row=8, column=2)

            self.password_entry = Entry(self, textvariable=self.__password, show="*")
            self.password_entry.grid(row=9, column=2)

            Label(self, text="", bg=BLACK).grid(row=10, column=2)

            Label(self, text="", bg=BLACK).grid(row=11, column=2)

            Button(self, text="Register", bg="red", command=self.register_user).grid(row=11, column=2)

            Label(self, text="", bg=BLACK)
            button3 = Button(self, text='Back', highlightthickness=0, command=self.destroy)
            button3.config(width=6, height=2)
            button3.grid(row=1, column=0)

        def register_user(self):

            self.__username_info = self.__username.get()
            self.__password_info = self.__password.get()
            error = False

            if self.__username_info == "":
                self.error(1)
                error = True
            if self.__password_info == "":
                self.error(2)
                error = True
            username_verification_ = username_verification(self.__username_info)
            password_verification_ = password_verification(self.__password_info)
            if username_verification_ is not None:
                self.error(username_verification_)
                error = True

            elif password_verification_ is not None:
                self.error(password_verification_)
                error = True

            if error is False:
                mycur.execute("SELECT COUNT(*) FROM users")
                result = mycur.fetchone()
                num = int(result[0])
                num += 1
                sql = "insert into users values(%s,%s,%s,%s,%s,%s,%s,%s)"
                t = (num, self.__username_info, self.__password_info, True, False, False, False, 0)
                mycur.execute(sql, t)
                db.commit()
                # Label(self, text="").pack()
                time.sleep(0.50)
                self.success(num)

        def error(self, type):
            if self.error_label is not None:
                self.error_label.destroy()

            if type == 1 or type == 2:
                self.error_label = Label(self, text="All fields are required..", fg="red", bg=BLACK, font="bold")
                self.error_label.grid(row=12, column=2)
                if type == 1:
                    self.error_label = self.username_entry.config(bg="red")

                elif type == 2:
                    self.error_label = self.password_entry.config(bg="red")
            else:
                self.username_entry.config(bg="red")
                self.password_entry.config(bg="red")
                self.error_label = Label(self, text=type, fg="red", bg=BLACK, font="bold", width=20)
                self.error_label.grid(row=12, column=2)

        def success(self, num):
            Label(self, text="Registration successful, log in to play!", bg="black", fg="green", font="bold").place(x=0,
                                                                                                                    y=0)
            global game_play
            global log_in_ui
            log_in_ui.destroy()
            from ui_setup import start_game_play
            start_game_play((num,))


def username_verification(inputted_username):  # also check if another person exists with the same username
    sql = "select username from users"
    mycur.execute(sql)
    result = mycur.fetchall()

    if (inputted_username,) in result:
        return 'this username exists'

    elif len(inputted_username) > 10:
        return 'username needs to be\n shorter than 10 characters'

    return None


def password_verification(inputted_password):
    if len(inputted_password) < 10:
        return 'password needs to be\n longer than 10 characters'

    elif check_if_uppercase_letter_present(inputted_password) is False:
        return 'password should\ninclude at least one\n upper case letter'

    elif check_for_numbers(inputted_password) is False:
        return 'password should\ninclude at least one\n number'

    elif check_special_characters(inputted_password) is False:
        return 'password should\ninclude at least one\n special character'

    return None


def check_if_uppercase_letter_present(password):
    for i in range(len(password)):
        if password[i].isupper() is True:
            return True
    return False


def check_special_characters(password):
    print('yes')
    print(password)
    all_special_characters = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", '-', "_", "+", "=", "{", "}",
                              "[", "]", "|", "/", "\\", ":", ";", "'", "<", ">", ",", ".", "?"]

    for i in all_special_characters:
        if i in password:
            print('no')
            return True
    return False


def check_for_numbers(password):
    all_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for i in all_nums:
        if i in password:
            return True
    return False


global log_in_ui
log_in_ui = GameStart()
log_in_ui.mainloop()