import tkinter as tk
import pyscreenshot as ImageGrab
from imgPreProcess import readImg
from predict import predict
from tkinter import messagebox

pos = [0, 0]


def move(event):
    global pos
    pos = [event.x, event.y]


def draw(event):
    global pos
    x, y = pos
    canvas.create_line(x,y,event.x,event.y)
    # canvas.create_rectangle(x - 3, y - 3, event.x + 3, event.y + 3, fill="black")
    # canvas.create_rectangle(x + 3, y + 3, event.x - 3, event.y - 3, fill="black")
    # canvas.create_rectangle(x - 3, y + 3, event.x + 3, event.y - 3, fill="black")
    # canvas.create_rectangle(x + 3, y - 3, event.x - 3, event.y + 3, fill="black")
    pos = [event.x, event.y]


def saveImg(event):
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    im = ImageGrab.grab((x, y, x1, y1))
    im.save("number.png")
    img = readImg("number.png")
    pred = predict(img)
    messagebox.showinfo("辨識結果", "你寫的數字是: " + str(pred))

    canvas.delete("all")


root = tk.Tk()
root.geometry("600x600")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = tk.Canvas(root, bg="#FFF")
canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
canvas.bind("<Button-1>", move)
canvas.bind("<B1-Motion>", draw)
root.bind("<ButtonRelease-3>", saveImg)

root.mainloop()
