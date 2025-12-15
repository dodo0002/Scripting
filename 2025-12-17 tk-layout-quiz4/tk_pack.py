import tkinter as tk

# 視窗設定
form = tk.Tk()
form.title("Tkinter Pack")
form.geometry("400x300")
form.resizable(False, False)


# 區塊結構
Left_Sidebar = tk.Frame(form, bg="lightgreen", width=40)
right_Sidebar = tk.Frame(form, bg="lightblue", width=40)
top = tk.Frame(form, bg="red", height=60)
bottom = tk.Frame(form, bg="blue", height=30)
middle = tk.Frame(form, bg="yellow")

# 關閉 pack_propagate，不隨內部 Label 縮小
top.pack_propagate(False)

# 區塊pack布局設定
Left_Sidebar.pack(side="left", fill="y")
right_Sidebar.pack(side="right", fill="y")
top.pack(side="top", fill="x")
bottom.pack(side="bottom", fill="x")
middle.pack(side="top", fill="both", expand=True)


# 標籤設定
label_left = tk.Label(top, text="left", bg='white', fg='black')
label_center = tk.Label(top, text="center", bg='white', fg='black' )
label_right = tk.Label(top, text="Right", bg='white', fg='black')

# 標籤pack布局設定
label_left.pack(side="left" , fill="x", expand=True,   anchor="nw", padx=40, pady=5) 
label_center.pack(side="left", fill="x", expand=True,  anchor="n", padx=40 , pady=5) 
label_right.pack(side="left", fill="x", expand=True,  anchor="ne", padx=30, pady=5)


form.mainloop()