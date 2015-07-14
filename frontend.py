print("setting up...")

from Tkinter import *
import serial

print("opening serial")
ser = serial.Serial('/dev/ttyAMA0',9600)

print("setting up display")
display = Tk()

def callback():
	print("pressed!")
	ser.write("LEL")

b = Button(display, text="hello", command=callback())
b.pack()

print("ready")

mainloop()

ser.close()
