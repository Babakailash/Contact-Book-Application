from sqlite3 import connect
from tkinter import*
from tkinter.ttk import*
from tkinter import messagebox
import home

class LoginWindow(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        
        self.title("Login")
        self.geometry("400x300")
        
        s = Style()
        s.configure('Header.TFrame', background = 'blue')
        
        header_frame = Frame(self, style='Header.TFrame')
        header_frame.pack(fill=X)
        
        s.configure('Header.TLabel', background = 'blue', foreground = 'white', font = ('Arial',15))
        header_lable = Label(header_frame, style='Header.TLabel', text= "My Contact Book")
        header_lable.pack(pady=10)
        
        s.configure('Content.TFrame', background = 'white')
        content_frame = Frame(self, style='Content.TFrame')
        content_frame.pack(fill= BOTH, expand= TRUE)
        
        login_frame = Frame(content_frame, style='Content.TFrame')
        login_frame.place(relx=.5,rely=.5, anchor= CENTER)
        
        s.configure('Login.TLabel', background = 'white', font = ('Arial', 15))
        
        username_label = Label(login_frame, text = 'Username', style='Login.TLabel')
        username_label.grid(row=0,column=0)
        
        self.username_entry = Entry(login_frame, font = ('Arial', 15), width=15)
        self.username_entry.grid(row=0,column=1, pady=5)
        
        password_label = Label(login_frame, text = 'Password', style='Login.TLabel')
        password_label.grid(row=1,column=0)
        
        s.configure('Login.TButton', font = ('Arial', 15))
        
        self.password_entry = Entry(login_frame, font = ('Arial', 15), width=15, show='*')
        self.password_entry.grid(row=1,column=1, pady=5)
        
        login_button = Button(login_frame, text = "Login", style='Login.TButton', command= self.login_button_click)
        login_button.grid(row=2,column=1, pady=5)
        login_button.bind('<Return>',self.login_button_click)
    
    def login_button_click(self,event = None):
        con = connect('D:\Coding_Practice\contact_book_project\contact_db\contact_db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Login where Username = ? and Password =?",(self.username_entry.get(),self.password_entry.get()))
        row = cur.fetchone()
        
        if row is not None:
            # messagebox.showinfo("Success Message", "Logged in successfully")
            self.destroy()
            home.HomeWindow()
        else:
            messagebox.showerror("Error Message", "Incorrect username/password")    
                  
if __name__ == '__main__':
    lw = LoginWindow()
    lw.mainloop()        