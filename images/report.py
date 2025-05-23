from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.config(bg="white")
        self.root.geometry("1200x500+0+0")
        self.root.focus_force()

        # ==============================Title===========================================
        title = Label(self.root, text="View Student Results Details", font=("goudy old style", 20, "bold"), bg="Orange", fg="#262626").place(x=10, y=15, relwidth=1, height=40)
        
        # ===========================Search==================
        self.var_search = StringVar()
        lbl_search = Label(self.root, text="Search By Roll No", font=("goudy old style", 20, 'bold'), bg='white').place(x=280, y=100)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg='lightyellow').place(x=500, y=100, width=150)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=670, y=100, width=120, height=35)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2", command=self.clear).place(x=800, y=100, width=120, height=35)
        
        # ===========================Result Labels==================
        lbl_roll = Label(self.root, text="Roll No", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=150, y=230, width=150, height=50)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=300, y=230, width=150, height=50)
        lbl_courses = Label(self.root, text="Course", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=450, y=230, width=150, height=50)
        lbl_marks = Label(self.root, text="Marks Obtained", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=600, y=230, width=150, height=50)
        lbl_full_marks = Label(self.root, text="Total Marks", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=750, y=230, width=150, height=50)
        lbl_per = Label(self.root, text="Percentage", font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE).place(x=900, y=230, width=150, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)
        self.name = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)
        self.course = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)
        self.marks_ob = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.marks_ob.place(x=600, y=280, width=150, height=50)
        self.full_marks = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.full_marks.place(x=750, y=280, width=150, height=50)
        self.per = Label(self.root, font=("goudy old style", 15, 'bold'), bg='white', bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)
        
        # ===========================Button Delete==================
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=500, y=350, width=150, height=35)
        
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll, name, course, marks_ob, full_marks FROM result WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.roll.config(text=row[0])
                self.name.config(text=row[1])
                self.course.config(text=row[2])
                self.marks_ob.config(text=row[3])
                self.full_marks.config(text=row[4])
                self.per.config(text=f"{(row[3] / row[4]) * 100:.2f}%")
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.roll.cget("text") == "":
                messagebox.showerror("Error", "Please search for a student result to delete", parent=self.root)
            else:
                cur.execute("DELETE FROM result WHERE roll=?", (self.roll.cget("text"),))
                con.commit()
                messagebox.showinfo("Success", "Result deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_search.set("")
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks_ob.config(text="")
        self.full_marks.config(text="")
        self.per.config(text="")

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()