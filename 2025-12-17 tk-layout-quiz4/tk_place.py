import tkinter as tk

# 視窗設定
form = tk.Tk()
form.title("Tkinter Place")
form.geometry("400x300")
form.resizable(False, False)

# 區塊結構
Left_Sidebar = tk.Frame(form, bg="lightgreen", width=40)
right_Sidebar = tk.Frame(form, bg="lightblue", width=40)
top = tk.Frame(form, bg="red", height=60)
bottom = tk.Frame(form, bg="blue", height=30)
middle = tk.Frame(form, bg="yellow")

# 關閉 propagate，不隨內部 Label 縮小
top.propagate(False)

# 區塊place布局設定
Left_Sidebar.place(x=0, y=0, relwidth=0.1, relheight=1.0)
right_Sidebar.place(x=360, y=0, relwidth=0.1, relheight=1.0)
top.place(x=40, y=0, relwidth=0.8, relheight=0.2)
bottom.place(x=40, y=270, relwidth=0.8, relheight=0.1)
middle.place(x=40, y=60, relwidth=0.8, relheight=0.7)


# 標籤設定
label_left = tk.Label(top, text="left", bg='white', fg='black')
label_center = tk.Label(top, text="center", bg='white', fg='black' )
label_right = tk.Label(top, text="Right", bg='white', fg='black')  

# 標籤place布局設定
label_left.place(relx=0.05, rely=0.3, anchor='w', x=20)
label_center.place(relx=0.5, rely=0.3, anchor='center')
label_right.place(relx=0.95, rely=0.3, anchor='e', x=-20)


form.mainloop()
