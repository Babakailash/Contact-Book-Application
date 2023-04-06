from tkinter import*
from tkinter.ttk import*
from sqlite3 import*
from tkinter import messagebox

class ManageContactsFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        
        s = Style()
        s.configure('TFrame', background = 'white')
        s.configure('TLabel', background = 'white', font = ('Arial',15))
        s.configure('TButton', font = ('Arial',15))
        s.configure('Treeview.Heading', font = ('Arial',15))
        s.configure('Treeview', font = ('Arial',14), rowheight = 25)

        self.pack(fill = BOTH, expand= TRUE)
        
        self.con = connect("D:\Coding_Practice\contact_book_project\contact_db\contact_db")
        self.cur = self.con.cursor()
        
        self.create_view_all_contact_frame()
    
    def fill_contacts_treeview(self):
        for contact in self.contacts_treeview.get_children():
            self.contacts_treeview.delete(contact)
        
        contacts = self.cur.fetchall()
        for contact in contacts:
            self.contacts_treeview.insert("",END,values = contact)
            
        
    def create_view_all_contact_frame(self):
        self.view_all_contacts_frame = Frame(self)
        self.view_all_contacts_frame.place(relx=.5, rely=.5, anchor= CENTER)
        
        add_new_contact_button = Button(self.view_all_contacts_frame, text = "Add New Contact", command=self.add_new_contact_button_click)
        add_new_contact_button.grid(row=0, column=1, sticky=E, pady=25)
        
        name_label = Label(self.view_all_contacts_frame, text = "Name:")
        name_label.grid(row=1, column=0)
        
        self.name_entry = Entry(self.view_all_contacts_frame, font = ('Arial', 15), width=66)
        self.name_entry.grid(row=1, column=1, pady=10)
        
        self.name_entry.bind('<KeyRelease>',self.name_entry_key_release)
        
        self.contacts_treeview = Treeview(self.view_all_contacts_frame, columns=('name','phone_no', 'email_id','city'), show='headings')
        self.contacts_treeview.heading('name', text= 'Name', anchor=W)
        self.contacts_treeview.heading('phone_no', text = 'Phone Number', anchor=W)
        self.contacts_treeview.heading('email_id', text = 'Email Id', anchor=W)
        self.contacts_treeview.heading('city', text = 'City', anchor=W)
        self.contacts_treeview.column('name',width = 250)
        self.contacts_treeview.column('phone_no',width = 200)
        self.contacts_treeview.column('email_id',width = 250)
        self.contacts_treeview.column('city',width = 100)
        self.contacts_treeview.grid(row=2,column=0, columnspan=2, pady=10)
        
        self.contacts_treeview.bind('<<TreeviewSelect>>',self.contact_treeview_row_selection)

        
        self.cur.execute("SELECT * FROM Contact")
        self.fill_contacts_treeview()
        # contacts =self.cur.fetchall()
    
        # for contact in contacts:
        #     self.contacts_treeview.insert("",END,values = contact)
        
        ## contacts_treeview.insert("",0,values = ('Nand Kishor','+911234567890','nand_kishor@gmail.com','Patna'))
        ## contacts_treeview.insert("",1,values = ('Ravi Ranajan','+910987654321','ravi_ranjan@gmail.com','Noida'))
        ## contacts_treeview.insert("",2,values = ('satyam','+9112344321','satyam_s@gmail.com','Greater Noida'))
        
        
    def add_new_contact_button_click(self):
        self.view_all_contacts_frame.destroy()
        
        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx=.5,rely=.5, anchor=CENTER)
        
        name_label = Label(self.add_new_contact_frame, text = "Name:")
        name_label.grid(row=0, column=0, sticky=E)
        
        self.name_entry = Entry(self.add_new_contact_frame, width = 30, font = ('Arial',15))
        self.name_entry.grid(row = 0, column=1, pady=10)
        
        phone_number_label = Label(self.add_new_contact_frame, text = "Phone Number:")
        phone_number_label.grid(row=1, column=0, sticky=E)
        
        self.phone_number_entry = Entry(self.add_new_contact_frame,width = 30, font = ('Arial',15))
        self.phone_number_entry.grid(row=1, column=1, pady=10)
        
        email_id_label = Label(self.add_new_contact_frame, text = "Email Id:")
        email_id_label.grid(row=2, column=0, sticky=E)
        
        self.email_id_entry = Entry(self.add_new_contact_frame, width = 30, font = ('Arial',15))
        self.email_id_entry.grid(row=2, column=1, pady=10)     
        
        city_label = Label(self.add_new_contact_frame, text = "City:")
        city_label.grid(row=3, column=0, sticky=E)
        
        self.city_combobox = Combobox(self.add_new_contact_frame, width = 28, font = ('Arial',15),values=("Noida",'Greater Noida','Delhi','Ayodhya','Mumbai','Lucknow','Pune'))
        self.city_combobox.grid(row=3, column=1, pady=5)
        self.city_combobox.set("Select your city")    
        
        add_button = Button(self.add_new_contact_frame, text = 'Add', width = 30, command=self.add_button_click)
        add_button.grid(row=4,column=1, pady=5)   
     
    def add_button_click(self):
        self.cur.execute("SELECT * FROM Contact WHERE Email_Id = ?",(self.email_id_entry.get(),))
        contact = self.cur.fetchone()
        if contact is None:
            self.cur.execute("INSERT INTO Contact (Name, Phone_Number, Email_Id, City) VALUES(?,?,?,?)",(self.name_entry.get(),self.phone_number_entry.get(),self.email_id_entry.get(),self.city_combobox.get()))
            self.con.commit()
            messagebox.showinfo("Success Message","Contact details are added successfully")
            self.add_new_contact_frame.destroy()  
            self.create_view_all_contact_frame() 
        else:
            messagebox.showerror("Error Message", "Contact details are already added")
        
    def name_entry_key_release(self,event):
        # messagebox.showinfo("Message", "Hello")   
        self.cur.execute("SELECT * FROM Contact WHERE Name LIKE ?",('%'+self.name_entry.get()+'%',))
        self.fill_contacts_treeview()
        
    def contact_treeview_row_selection(self,event):
        contact = self.contacts_treeview.item(self.contacts_treeview.selection())['values'] 
        self.view_all_contacts_frame.destroy()
        
        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx=.5,rely=.5, anchor=CENTER)
        
        name_label = Label(self.update_delete_contact_frame, text = "Name:")
        name_label.grid(row=0, column=0, sticky=E)
        
        self.name_entry = Entry(self.update_delete_contact_frame, width = 30, font = ('Arial',15))
        self.name_entry.grid(row = 0, column=1, pady=10)
        self.name_entry.insert(END,contact[0])
        
        phone_number_label = Label(self.update_delete_contact_frame, text = "Phone Number:")
        phone_number_label.grid(row=1, column=0, sticky=E)
        
        self.phone_number_entry = Entry(self.update_delete_contact_frame,width = 30, font = ('Arial',15))
        self.phone_number_entry.grid(row=1, column=1, pady=10)
        self.phone_number_entry.insert(END,contact[1])
        
        email_id_label = Label(self.update_delete_contact_frame, text = "Email Id:")
        email_id_label.grid(row=2, column=0, sticky=E)
        
        self.email_id_entry = Entry(self.update_delete_contact_frame, width = 30, font = ('Arial',15))
        self.email_id_entry.grid(row=2, column=1, pady=10)     
        self.old_email_id = contact[2]
        self.email_id_entry.insert(END,contact[2])
        
        city_label = Label(self.update_delete_contact_frame, text = "City:")
        city_label.grid(row=3, column=0, sticky=E)
        
        self.city_combobox = Combobox(self.update_delete_contact_frame, width = 28, font = ('Arial',15),values=("Noida",'Greater Noida','Delhi','Ayodhya','Mumbai','Lucknow','Pune'))
        self.city_combobox.grid(row=3, column=1, pady=5)
        self.city_combobox.set(contact[3])    
        
        update_button = Button(self.update_delete_contact_frame, text = 'Update', width = 30, command=self.update_button_click)
        update_button.grid(row=4,column=1, pady=5)    
        
        delete_button = Button(self.update_delete_contact_frame, text = 'Delete', width = 30, command=self.delete_button_click)
        delete_button.grid(row=5,column=1, pady=5) 
        
    def update_button_click(self):
        self.cur.execute("UPDATE Contact SET Name = ?, Phone_Number = ?, Email_Id = ?, City = ? WHERE Email_Id = ?",(self.name_entry.get(),self.phone_number_entry.get(),self.email_id_entry.get(),self.city_combobox.get(),self.old_email_id_entry))
        self.con.commit()
        messagebox.showinfo("Success Message", "Contact details are updated successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contact_frame()
        
    def delete_button_click(self):
        if messagebox.askquestion("Confirmation Message","Are you sure to delete?") == 'yes':   
            self.cur.execute("DELETE FROM Contact WHERE Email_Id = ?",(self.old_email_id,))
            self.con.commit()
            messagebox.showinfo("Success Message", "Contact details are deleted successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contact_frame()             







        