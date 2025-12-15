import tkinter as tk

# 視窗設定
form = tk.Tk()
form.title("Tkinter Grid")
form.geometry("400x300")
form.resizable(False, False)

# 區塊結構
Left_Sidebar = tk.Frame(form, bg="lightgreen", width=40)
right_Sidebar = tk.Frame(form, bg="lightblue", width=40)
top = tk.Frame(form, bg="red", height=60)
bottom = tk.Frame(form, bg="blue", height=30)
middle = tk.Frame(form, bg="yellow")

# 關閉 grid_propagate，不隨內部 Label 縮小
top.grid_propagate(False)

# 區塊grid布局設定
Left_Sidebar.grid(row=0, column=0,  sticky="ns", rowspan=3)
right_Sidebar.grid(row=0, column=4, sticky='ns', rowspan=3)
top.grid(row=0, column=1, sticky="ew", columnspan=3)
bottom.grid(row=2, column=1, sticky="ew", columnspan=3)
middle.grid(row=1, column=1, sticky="nsew", columnspan=3)

# 行配置
form.rowconfigure(1, weight=1)

# 列配置
form.columnconfigure(1, weight=1)


# 標籤設定
label_left = tk.Label(top, text="left", bg='white', fg='black')
label_center = tk.Label(top, text="center", bg='white', fg='black')
label_right = tk.Label(top, text="Right", bg='white', fg='black')

# 標籤grid布局設定
label_left.grid(row=0, column=0, padx=5, pady=5)
label_center.grid(row=0, column=1, padx=5, pady=5)
label_right.grid(row=0, column=2, padx=5, pady=5)

top.columnconfigure(0, weight=1)
top.columnconfigure(1, weight=1)
top.columnconfigure(2, weight=1)


form.mainloop()
