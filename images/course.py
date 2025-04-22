from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.config(bg="white")
        self.root.geometry("1350x700+0+0")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Manage Course Detail", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, relwidth=1, height=40)

        # Variables
        self.var_course = StringVar()
        self.var_Duration = StringVar()
        self.var_Charges = StringVar()

        # Widgets
        lbl_courseName = Label(self.root, text="Course Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        lbl_Duration = Label(self.root, text="Duration", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        lbl_Charges = Label(self.root, text="Charges", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        lbl_Description = Label(self.root, text="Description", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)

        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW')
        self.txt_courseName.place(x=150, y=60, width=200)
        self.txt_Duration = Entry(self.root, textvariable=self.var_Duration, font=("goudy old style", 15, 'bold'), bg='light yellow')
        self.txt_Duration.place(x=150, y=100, width=200)
        self.txt_Charges = Entry(self.root, textvariable=self.var_Charges, font=("goudy old style", 15, 'bold'), bg='light yellow')
        self.txt_Charges.place(x=150, y=140, width=200)
        self.txt_Description = Text(self.root, font=("goudy old style", 15, 'bold'), bg='light yellow')
        self.txt_Description.place(x=150, y=180, width=500, height=200)

        # Buttons
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#e43b06", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#0676ad", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#038074", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # Search Panel
        self.var_search = StringVar()
        lbl_search_courseName = Label(self.root, text="Course Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=720, y=60)
        txt_search_courseName = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW').place(x=870, y=60, width=180)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=1070, y=60, width=120, height=28)

        # Content
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("CID", "Name", "Duration", "Charges", "Description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        self.CourseTable.heading("CID", text="Course ID")
        self.CourseTable.heading("Name", text="Name")
        self.CourseTable.heading("Duration", text="Duration")
        self.CourseTable.heading("Charges", text="Charges")
        self.CourseTable.heading("Description", text="Description")
        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("CID", width=50)
        self.CourseTable.column("Name", width=100)
        self.CourseTable.column("Duration", width=100)
        self.CourseTable.column("Charges", width=100)
        self.CourseTable.column("Description", width=100)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course Name already present", parent=self.root)
                else:
                    cur.execute("insert into course (Name, Duration, Charges, Description) VALUES (?, ?, ?, ?)", (
                        self.var_course.get(),
                        self.var_Duration.get(),
                        self.var_Charges.get(),
                        self.txt_Description.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select course from list", parent=self.root)
                else:
                    cur.execute("update course set Duration=?, Charges=?, Description=? where Name=?", (
                        self.var_Duration.get(),
                        self.var_Charges.get(),
                        self.txt_Description.get("1.0", END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name should be required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select course from list", parent=self.root)
                else:
                    cur.execute("delete from course where name=?", (self.var_course.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Course Deleted Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_Duration.set(row[2])
        self.var_Charges.set(row[3])
        self.txt_Description.delete('1.0', END)
        self.txt_Description.insert(END, row[4])

    def clear(self):
        self.var_course.set("")
        self.var_Duration.set("")
        self.var_Charges.set("")
        self.txt_Description.delete('1.0', END)

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()