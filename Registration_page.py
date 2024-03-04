from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3


a = Tk()
a.config(bg = "white")
a.geometry("1000x600")
a.title("REGISTRATION FORM")
a.iconbitmap("logg.ico")



Label(a, text = "REGISTER",bg = "white", font=("Times New Roman",40, "bold")).place(x = 600, y = 0)

#background work------------
image1 = ImageTk.PhotoImage(file="ticket.png")
image1Label=Label(a,image=image1)
image1Label.place(x=-137, y=50)


#connection to database-----------
conn=sqlite3.connect('regd_user_database.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS regd_users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                username           TEXT,
                email             TEXT,
                password              TEXT,
                mobile             INT        
)""")
conn.commit()

 
#FUNTIONS--------------

def hide1():
    openeye1.config(file="closeye.png")
    password_entry.config(show="●")
    eye_button1.config(command=show1)
def show1():
    openeye1.config(file="eyeopen.png")
    password_entry.config(show="")
    eye_button1.config(command=hide1)

def hide2():
    openeye2.config(file="closeye.png")
    confirm_password_entry.config(show="●")
    eye_button2.config(command=show2)
def show2():
    openeye2.config(file="eyeopen.png")
    confirm_password_entry.config(show="")
    eye_button2.config(command=hide2)



def register():
    # Get user input from entry fields
    username = username_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    agree_terms = terms_conditions_var.get()
    

     # Check if username, email, or mobile already exists in the database
    c.execute("SELECT * FROM regd_users WHERE username=? OR email=?", (username, email))
    existing_user = c.fetchone()
    if existing_user:
        messagebox.showerror("Error", "Username or email already exists")
        return
    
    #Check if email has @gmail.com---
    if not email.endswith("@gmail.com"):
        messagebox.showerror("Error", "Please enter a Gmail address")
        return
    
    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return
    
     # Check if terms and conditions checkbox is ticked
    if not agree_terms:
        messagebox.showerror("Error", "Please agree to the Terms and Conditions")
        return
    
    if len(mobile)!=10:
        messagebox.showerror("Error","Please enter a valid phone number.")
        return
    

    # Insert user details into the database
    c.execute("INSERT INTO regd_users (username, email, mobile, password) VALUES (?, ?, ?, ?)", (username, email, mobile, password))
    conn.commit()
    messagebox.showinfo("Success", "Registration successful")
    a.destroy()
    import Login_page

 #import the login page when log in here is clicked--
def login_here():
    a.destroy()
    import Login_page



#LABEL FIELDS------
username_label = Label(a, text ="Username ",bg = "white", font = ("Arial",15,"bold"))
username_label.place(x=465, y=100)

email_label = Label(a, text = "Email ",  bg = 'white', font = ("Arial",15,"bold") )
email_label.place(x=465,y=150)

mobile_label = Label(a, text = "Mobile ", bg = 'white', font = ("Arial",15,"bold"))
mobile_label.place(x=465,y=200)

password_label = Label(a, text = "Set a password ",  bg = 'white', font = ("Arial",15,"bold"))
password_label.place(x=465,y=250)

confirm_password_label = Label(a, text = "Confirm Password", bg = 'white', font = ("Arial",15,"bold"))
confirm_password_label.place(x=465,y=300)


#ENTRY FIELDS-----
username_entry = Entry(a, font=("Arial",15))
username_entry.place(x=650,y=100, height=30, width=250)

email_entry = Entry(a, font=("Arial",15))
email_entry.place(x=650,y=150, height=30, width=250)

mobile_entry = Entry(a, font=("Arial",15))
mobile_entry.place(x=650,y=200, height=30, width=250)

password_entry = Entry(a,font=("Arial",15))
password_entry.place(x=650,y=250, height=30, width=250)

openeye1 = PhotoImage(file="eyeopen.png")
openeye2 = PhotoImage(file="eyeopen.png")

eye_button1 = Button(a, image=openeye1,bd=0,bg="white",activebackground="white",command=hide1)
eye_button1.place(x =874, y =253)

confirm_password_entry = Entry(a, font=("Arial",15))
confirm_password_entry.place(x=650,y=300, height=30, width=250)

eye_button2 = Button(a, image=openeye2,bd=0,bg="white",activebackground="white",command=hide2)
eye_button2.place(x=874,y=303)

alreadyaccount=Label(a, text = "Already have an account?",bg = "white", font=("Arial",13))
alreadyaccount.place(x=650,y=470)

login_btn = Button(a, text = "Log In Here", fg = "blue", bg = 'white', 
                   font=("Arial",13, 'bold underline'),cursor='hand2',bd=0,activebackground="white",command=login_here)
login_btn.place(x=850,y=467)


terms_conditions_var = BooleanVar()
terms_conditions = Checkbutton(a, text='I agree to the Terms and Conditions', font=("Arial",11,"bold"),
                    bg = "white",activebackground="white",variable=terms_conditions_var)
terms_conditions.place(x=650,y=350)

register_btn = Button(a,text= "SIGN UP",font=("Times New Roman",20,"bold"),bd=0,
                    bg = "gray50", cursor = "hand2",activebackground="white",command=register)
register_btn.place(x=650, y=400,width=250)






a.mainloop()