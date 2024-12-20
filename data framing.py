import tkinter as tk
from tkinter import ttk
file = open(r"\maindata.txt","r")
data = eval(file.read())
file.close()
def populate_tree(tree, parent, data):
    for db_name, tables in data.items():
        db_id = tree.insert(parent, "end", text=f"+ {db_name}", open=False)
        for table_name, columns in tables.items():
            table_id = tree.insert(db_id, "end", text=f"{table_name}", open=False)
            for column_name in columns:
                tree.insert(table_id, "end", text=f" {column_name}", open=False)
root = tk.Tk()
root.title("Database Viewer")
tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True)
populate_tree(tree, "", data)
tree.bind("<<TreeviewOpen>>", lambda event: tree.item(tree.focus(), text=f"{tree.item(tree.focus())['text']}"))
tree.bind("<<TreeviewClose>>", lambda event: tree.item(tree.focus(), text=f"{tree.item(tree.focus())['text']}"))
root.mainloop()
