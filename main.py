
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="ReevaMehta"
    )


# Main window
root = tk.Tk()
root.title("Job Recommendation System")
root.geometry("750x550")


tk.Label(
    root,
    text="Job Recommendation System",
    font=("Arial", 20, "bold")
).pack(pady=15)


# Input fields
form = tk.Frame(root)
form.pack(pady=10)

fields = ["R_regno", "Rcontactno", "R_name", "R_design"]
entries = {}

for i, field in enumerate(fields):
    tk.Label(
        form, text=field, font=("Arial", 11), width=15
    ).grid(row=i, column=0, padx=10, pady=6)

    entry = tk.Entry(form, width=30, font=("Arial", 11))
    entry.grid(row=i, column=1, padx=10, pady=6)

    entries[field] = entry


# Clear input fields
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)


# INSERT recruiter
def insert_recruiter():
    values = tuple(entries[f].get().strip() for f in fields)

    if any(v == "" for v in values):
        messagebox.showwarning("Warning", "Fill in all fields.")
        return

    con = None
    cur = None

    try:
        con = connect_db()
        cur = con.cursor()

        query = """
            INSERT INTO Recruiter
            (R_regno, Rcontactno, R_name, R_design)
            VALUES (%s, %s, %s, %s)
        """

        cur.execute(query, values)
        con.commit()

        messagebox.showinfo(
            "Success", "Recruiter inserted successfully!"
        )
        view_recruiters()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()


# UPDATE recruiter
def update_recruiter():
    values = tuple(entries[f].get().strip() for f in fields)

    if any(v == "" for v in values):
        messagebox.showwarning(
            "Warning", "Fill in all fields to update."
        )
        return

    con = None
    cur = None

    try:
        con = connect_db()
        cur = con.cursor()

        query = """
            UPDATE Recruiter
            SET Rcontactno = %s,
                R_name = %s,
                R_design = %s
            WHERE R_regno = %s
        """

        params = (
            values[1], values[2], values[3], values[0]
        )

        cur.execute(query, params)
        con.commit()

        if cur.rowcount > 0:
            messagebox.showinfo(
                "Success", "Recruiter updated successfully!"
            )
        else:
            messagebox.showinfo(
                "Result", "Recruiter registration number not found."
            )

        view_recruiters()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()


# DELETE recruiter using registration number
def delete_recruiter():
    regno = entries["R_regno"].get().strip()

    if not regno:
        messagebox.showwarning(
            "Warning", "Enter R_regno to delete."
        )
        return

    if not messagebox.askyesno(
        "Confirm Delete",
        f"Delete recruiter with registration number {regno}?"
    ):
        return

    con = None
    cur = None

    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM Recruiter WHERE R_regno = %s",
            (regno,)
        )
        con.commit()

        if cur.rowcount > 0:
            messagebox.showinfo(
                "Success", "Recruiter deleted successfully!"
            )
        else:
            messagebox.showinfo(
                "Result", "Recruiter not found."
            )

        view_recruiters()

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e) + "\nCheck whether another table references this recruiter."
        )

    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()


# VIEW all recruiters
def view_recruiters():
    con = None
    cur = None

    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "SELECT R_regno, Rcontactno, R_name, R_design "
            "FROM Recruiter"
        )

        rows = cur.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", tk.END, values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()


# Buttons
buttons = tk.Frame(root)
buttons.pack(pady=12)

tk.Button(
    buttons, text="INSERT", width=12,
    command=insert_recruiter
).grid(row=0, column=0, padx=5)

tk.Button(
    buttons, text="UPDATE", width=12,
    command=update_recruiter
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons, text="DELETE", width=12,
    command=delete_recruiter
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons, text="VIEW", width=12,
    command=view_recruiters
).grid(row=0, column=3, padx=5)

tk.Button(
    buttons, text="CLEAR", width=12,
    command=clear_fields
).grid(row=0, column=4, padx=5)


# Display recruiter records
columns = ("R_regno", "Rcontactno", "R_name", "R_design")

tree = ttk.Treeview(
    root, columns=columns, show="headings", height=8
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=160)

tree.pack(fill="both", expand=True, padx=10, pady=10)


# Load existing records
view_recruiters()

root.mainloop()
