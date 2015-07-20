from Tkinter import *
import serial

variable = 100

class App:
	def __init__(self,master):

		frame = Frame(master, height=100, width=400)
		frame.pack_propagate(0)
		frame.pack()

		self.e = Entry(master)
		self.e.pack(side=TOP)

		self.v = StringVar()
		Label(master, textvariable=self.v).pack(side=TOP)
		self.v.set(variable)

		self.button = Button(frame, text="quit", command=frame.quit)
		self.button.pack(side=LEFT, fill=BOTH, expand =1)

		self.send = Button(frame, text="send", command=self.send_cmd)
		self.send.pack(side=LEFT, fill=BOTH, expand =1)
		
		self.increment = Button(frame, text="+100", command=self.inc_variable)
		self.increment.pack(side=LEFT, fill=BOTH, expand =1)
		
		self.decrement = Button(frame, text="-100", command=self.dec_variable)
		self.decrement.pack(side=LEFT, fill=BOTH, expand =1)
		
	def inc_variable(self):
		global variable
		variable += 100
		self.v.set(variable)
	
	def dec_variable(self):
		global variable
		variable -= 100
		self.v.set(variable)
	
	def send_cmd(self):
		print(self.e.get())
		ser.write(self.e.get())
		ser.write("\n")

ser = serial.Serial('/dev/ttyAMA0', 9600)

root = Tk()

app = App(root)

root.mainloop()
root.destroy()
ser.close()
