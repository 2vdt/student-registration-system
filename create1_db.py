import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()
    
    # Create course table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS course (
        CID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Duration TEXT,
        Charges TEXT,
        Description TEXT
    )
    """)
    con.commit()

    # Create student table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student (
        roll INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        gender TEXT,
        dob TEXT,
        contact TEXT,
        addmision TEXT,
        course TEXT,
        state TEXT,
        city TEXT,
        pin TEXT,
        address TEXT
    )
    """)
    con.commit()

    # Create result table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS result (
        rid INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT,
        name TEXT,
        course TEXT,
        marks_ob INTEGER,
        full_marks INTEGER,
        FOREIGN KEY (roll) REFERENCES student (roll)
    )
    """)
    con.commit()
    con.close()

if __name__ == "__main__":
    create_db()
    print("Tables created successfully.")