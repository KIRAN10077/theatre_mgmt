from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

def mov_details_page():
    home.destroy()
    import movie_details
    movie_details.main()

def cus_details_page():
    home.destroy()
    import customer_details
    customer_details.main()

def staffs_details_page():
    home.destroy()
    import staff_details
    staff_details.main()

def logout():
    messagebox.showwarning("WARNING","are you sure you want to logout?")
    home.destroy()
    import Login_page

def menu_page():
    home.destroy()
    import menu_manager
    menu_manager.main()
    

home = Tk()
home.geometry('1200x700')
home.resizable(0, 0)

# Load image for the background 
image = Image.open('gg.png')
photo_image = ImageTk.PhotoImage(image)

# Create canvas for the background image
canvas = Canvas(home, width=1000, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=photo_image, anchor='nw')

# Heading label with styled text
Heading = Label(home, text="FUSION CINEMAS", font=("Arial", 40, "bold"), fg="#FF6347", bg="Black")
Heading.place(x=400, y=20)


# Button to navigate to movie details page
movie_icon = PhotoImage(file="movielogo.png")
movie_details_btn = Button(home, text=("MANAGE \n MOVIES"), fg="Black", font=("Arial", 20, "bold italic"),cursor="hand2",compound="bottom",image=movie_icon, command=mov_details_page)
movie_details_btn.place(x=270, y=160, height=290, width=170)

# Button to navigate to customer details page
customer_icon = PhotoImage(file="customerlogo.png")
customer_details_btn = Button(home, text=("BOOKED \n DETAILS"), fg="Black", font=("Arial", 20, "bold italic"),cursor="hand2",compound="bottom",image=customer_icon,command=cus_details_page)
customer_details_btn.place(x=450, y=160, height=290, width=170)

# Button to navigate to staff details page
staff_icon = PhotoImage(file="stafflogo.png")
manage_staffs = Button(home, text=("MANAGE \n STAFFS"), fg="Black", font=("Arial", 20, "bold italic"),compound="bottom",image=staff_icon,cursor="hand2",command=staffs_details_page)  
manage_staffs.place(x=630, y=160, height=290, width=170)

# Button to navigate to menu manager page
menu_icon = PhotoImage(file="menulogo.png")
menu = Button(home, text=("MENU\nEDITOR"), fg="Black", font=("Arial", 20, "bold italic"),compound="bottom",image=menu_icon,cursor="hand2",command=menu_page)
menu.place(x=810, y=160, height=290, width=140)

# Logout button
logout_icon = PhotoImage(file= "logoutlogo.png")
logout_btn = Button(home, fg="Black", font=("Arial", 14, "bold"), compound="bottom",image=logout_icon, cursor="hand2", command=logout)
logout_btn.place(x=1070, y=20, height=70, width=100)

home.mainloop()
