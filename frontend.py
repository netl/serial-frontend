print("setting up...")

from Tkinter import *
import serial

print("opening serial")
ser = serial.Serial('/dev/ttyAMA0',9600)

print("setting up display")
display = Tk()

def callback():
	print("pressed!")
	ser.write("pressed/n")

b = Button(display, text="hello", command=callback, height=5, width=10)
b.pack()

print("ready")

display.mainloop()

ser.close()
