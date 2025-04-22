import sqlite3
def create_db():
    con=sqlite3.connect(database="rms.db")

    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS course(CID INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Duration text,Charges text,Description text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY AUTOINCREMENT, name text ,email text,gender text ,dob text,contact text,addmision text,course text,state text,city text,pin text,address text)")
    con.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS result (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT,
        name TEXT,
        course TEXT,
        marks_obt INTEGER,
        full_marks INTEGER,
        FOREIGN KEY (roll) REFERENCES student (roll)
    )
    """)
    
    con.commit()
    con.close()

if __name__ == "__main__":
 create_db()
 print("Tables created successfully.")
