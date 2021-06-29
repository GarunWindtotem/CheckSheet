from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from PIL import ImageTk, Image

root = tk.Tk()
root.geometry("800x500")
root.pack_propagate(False)
root.resizable(0, 0)

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=500)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=300, rely=0.65, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse a file", command=lambda: file_dialog())
button1.place(rely=0.65, relx=0.5)

button2 = tk.Button(file_frame, text="Load File", command=lambda: load_excel_data())
button2.place(rely=0.65, relx=0.3)

label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

# Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

# open image
my_pic = Image.open('D:\\Github\\CheckSheet\\Output\\diagram dynamic mean.png')
# Resize image
resized = my_pic.resize((300, 225), Image.ANTIALIAS)
new_pic = ImageTk.PhotoImage(resized)

my_label = Label(root, image=new_pic)
my_label.place(x=800-300-20, y=500-225-20)

# path = 'D:\\Github\\CheckSheet\\Output\\diagram dynamic mean.png'
# img = ImageTk.PhotoImage(Image.open(path))
# panel = tk.Label(root, image=img)
# panel.pack(side="bottom", fill="both", expand="no")


def file_dialog():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetype=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    label_file["text"] = filename
    return None


def load_excel_data():
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        df = pd.read_excel(excel_filename)
    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()

    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    return None


def clear_data():
    tv1.delete(*tv1.get_children())


root.mainloop()
