from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3

win = Tk()
win.config(bg = "white")
win.geometry("1000x600")
win.title("LOGIN FORM")
win.iconbitmap("logg.ico")
win.resizable(0,0)


#FUNTIONS--------------

def hide():
    openeye.config(file="closeye.png")
    login_password_entry.config(show="●")
    eye_button.config(command=show)
def show():
    openeye.config(file="eyeopen.png")
    login_password_entry.config(show="")
    eye_button.config(command=hide)

def signup_here():
    win.destroy()
    import Registration_page

def signin():
    conn = sqlite3.connect('regd_user_database.db')
    c = conn.cursor()

    email = login_email_entry.get()
    password = login_password_entry.get()

    


    # Query the database to check if a user with the entered username and password exists
    c.execute("SELECT * FROM regd_users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful")
        win.destroy()
        import Home_page
    else:
        messagebox.showerror("Error", "Invalid username or password")

    





Label(win, text = "LOGIN",bg = "white", font=("Times New Roman",40, "bold")).place(x = 600, y = 0)

#background work------------
image1 = ImageTk.PhotoImage(file="ticket.png")
image1Label=Label(win,image=image1)
image1Label.place(x=-137, y=50)

#LABELS------------------
login_email = Label(win, text = "Email ",  bg = 'white', font = ("Arial",15,"bold") )
login_email.place(x=465,y=100)

login_password = Label(win, text = "Password ",  bg = 'white', font = ("Arial",15,"bold"))
login_password.place(x=465,y=150)

#ENTRIES------------------
login_email_entry = Entry(win, font=("Arial",15))
login_email_entry.place(x=650,y=100, height=30, width=250)

login_password_entry = Entry(win, font=("Arial",15))
login_password_entry.place(x=650,y=150, height=30, width=250)

openeye = PhotoImage(file="eyeopen.png")
eye_button = Button(win, image=openeye,bd=0,bg="white",activebackground="white",command=hide)
eye_button.place(x =874, y =153)

dont_have_account=Label(win, text = "Don't have an account?",bg = "white", font=("Arial",13))
dont_have_account.place(x=640,y=350)

Signup_btn = Button(win, text = "Sign Up Here", fg = "blue", bg = 'white', 
                   font=("Arial",13, 'bold underline'),cursor='hand2',bd=0,activebackground="white",command=signup_here)
Signup_btn.place(x=820,y=347)

Signin_btn = Button(win,text= "SIGN IN",font=("Times New Roman",20,"bold"),bd=0,
                    bg = "gray50", cursor = "hand2",activebackground="white",command=signin)
Signin_btn.place(x=650, y=240, width=250)



def forget_pass():
    def change_pass():
        if _email_entry.get() == '' or new_password_entry.get() == '' or confirm_new_password_entry.get() == '':
            messagebox.showerror("ERROR", "All Fields Are Required", parent=window)
        elif new_password_entry.get() != confirm_new_password_entry.get():
            messagebox.showerror("ERROR", "Password and Confirm Password are not Matching", parent=window)
        else:
            conn = sqlite3.connect('regd_user_database.db')
            c = conn.cursor()

            email = _email_entry.get()
            new_password = new_password_entry.get()

            query = "SELECT * FROM regd_users WHERE email=?"
            c.execute(query, (email,))
            row = c.fetchone()

            if row is None:
                messagebox.showerror("ERROR", "Incorrect Email", parent=window)
            else:
                query = "UPDATE regd_users SET password=? WHERE email=?"
                c.execute(query, (new_password, email))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password Changed Successfully", parent=window)
                window.destroy()

    window = Toplevel()
    window.config(bg="white")
    window.geometry("1000x600")
    window.iconbitmap("logg.ico")
    window.resizable(0, 0)
    window.title("RESET PASSWORD")

    heading_lvl = Label(window, text="CHANGE PASSWORD", bg='white', font=("Arial", 30, "bold"))
    heading_lvl.place(x=465, y=10)

    _email = Label(window, text="Email", bg='white', font=("Arial", 15, "bold"))
    _email.place(x=465, y=100)

    _email_entry = Entry(window, font=("Arial", 15))
    _email_entry.place(x=650, y=100, height=30, width=250)

    new_password = Label(window, text="Enter New Password", bg='white', font=("Arial", 15, "bold"))
    new_password.place(x=465, y=150)

    new_password_entry = Entry(window, font=("Arial", 15))
    new_password_entry.place(x=680, y=150, height=30, width=250)

    confirm_password = Label(window, text="Confirm Password", bg='white', font=("Arial", 15, "bold"))
    confirm_password.place(x=465, y=200)

    confirm_new_password_entry = Entry(window, font=("Arial", 15))
    confirm_new_password_entry.place(x=680, y=200, height=30, width=250)

    Submit_btn = Button(window, text="SUBMIT", font=("Times New Roman", 20, "bold"), bd=0,
                        bg="gray50", cursor="hand2", activebackground="white", command=change_pass)
    Submit_btn.place(x=650, y=290, width=250)






forgot_button = Button(win, text="Forgot Password?",font=("Arial",10,"bold"),
                    bd=0,bg="white",activebackground="white",fg="blue",cursor="hand2",command=forget_pass)
forgot_button.place(x =790, y =183)



win.mainloop()