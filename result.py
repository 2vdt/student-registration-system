from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.config(bg="white")
        self.root.geometry("1200x500+0+0")
        self.root.focus_force()

        # ==============================Title===========================================
        title = Label(self.root, text="Add Student Results Details", font=("goudy old style", 20, "bold"), bg="Orange", fg="#262626").place(x=10, y=15, relwidth=1, height=40)
        
        # ===========================Widgets==================
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()

        lbl_select = Label(self.root, text="Select", font=("goudy old style", 15, 'bold'), bg='white').place(x=50, y=100)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=50, y=160)
        lbl_courses = Label(self.root, text="Courses", font=("goudy old style", 15, 'bold'), bg='white').place(x=50, y=220)
        lbl_marks_obt = Label(self.root, text="Marks Obtained", font=("goudy old style", 15, 'bold'), bg='white').place(x=50, y=280)
        lbl_full_marks = Label(self.root, text="Full Marks", font=("goudy old style", 15, 'bold'), bg='white').place(x=50, y=340)
        
        # =====================Entry fields================
        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.set("Select")
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=500, y=100, width=120, height=28)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW', state='readonly').place(x=280, y=160, width=300)
        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW', state='readonly').place(x=280, y=220, width=300)
        txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW').place(x=280, y=280, width=300)
        txt_full_marks = Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 15, 'bold'), bg='LIGHT YELLOW').place(x=280, y=340, width=300)
        
        # =================Button==========================
        btn_add = Button(self.root, text="Submit", font=("times new roman", 15), bg="lightgreen", activebackground="lightgreen", cursor="hand2", command=self.add).place(x=300, y=420, width=120, height=35)
        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15), bg="lightgreen", cursor="hand2", command=self.clear).place(x=450, y=420, width=120, height=35)

        # Load and display image
        self.bg_img = Image.open("images/result.png")
        self.bg_img = self.bg_img.resize((500, 300))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(self.root, image=self.bg_img).place(x=630, y=100)

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def fetch_roll(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select roll from student")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()


    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select a student", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=? AND course=?", (self.var_roll.get(), self.var_course.get()))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Result already present", parent=self.root)
                elif self.var_roll.get() == "" or self.var_marks.get() == "" or self.var_full_marks.get() == "":
                    messagebox.showerror("Error", "All fields are required", parent=self.root)
                else:
                    per = (int(self.var_marks.get()) / int(self.var_full_marks.get())) * 100
                    cur.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks) VALUES (?, ?, ?, ?, ?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Result added successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.txt_student.set("Select")

if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()