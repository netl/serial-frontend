from Tkinter import *
import tkFont
import serial

#events
def cmd_start(event):
	canv.itemconfig(buttonStart, image=image_start_pressed)
	print("starting scan")
	#ser.write("scan")
	graph_results()

def cmd_tray(event):
	global loadstatus
	canv.itemconfig(buttonTray, image=image_tray_pressed)
	print("toggle tray")
	if loadstatus:
		loadstatus=0
		ser.write("unload\r\n")
	else:
		loadstatus=1
		ser.write("load\r\n")

def clear_buttons(event):
	canv.itemconfig(buttonStart, image=image_start)
	canv.itemconfig(buttonTray, image=image_tray)

def graph_results():
	for x in xrange(0,40):
		canv.coords(canv.graph[x],x*12,200-x,(x+1)*12,200-(x+1))

def read_serial():
	while ser.inWaiting():
		print ser.read(ser.inWaiting())
	root.after(1000,read_serial)

#setup
ser = serial.Serial('/dev/ttyAMA0', 115200)
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

loadstatus = 1 #guessing the tray is in

#images
tausta = PhotoImage(file="~/serial-frontend/labrox/tausta.gif")
image_start = PhotoImage(file="~/serial-frontend/labrox/start.gif")
image_tray = PhotoImage(file="~/serial-frontend/labrox/tray.gif")
image_start_pressed = PhotoImage(file="~/serial-frontend/labrox/start_pressed.gif")
image_tray_pressed = PhotoImage(file="~/serial-frontend/labrox/tray_pressed.gif")

#create canvas and objects
canv = Canvas(root, width=w, height=h)
canv.create_image(0,0, image=tausta, anchor='nw')
buttonStart = canv.create_image(45, 549, image=image_start, anchor='nw')
buttonTray = canv.create_image(45, 670, image=image_tray, anchor='nw')

#draw graphs
canv.graph = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1]
for x in xrange(0,40):
	canv.graph[x] = canv.create_line(x*12,200,(x+1)*12,200,fill="green",width=3)

#bind events
canv.end = Button(root, text="quit", command=quit)
canv.end.place(x=15, y=15, width=30, height=30)
canv.tag_bind(buttonStart, '<ButtonPress-1>', cmd_start)
canv.tag_bind(buttonTray, '<ButtonPress-1>', cmd_tray)
canv.tag_bind(buttonStart, '<ButtonRelease-1>', clear_buttons)
canv.tag_bind(buttonTray, '<ButtonRelease-1>', clear_buttons)

#loop, and cleanup
canv.pack()
root.after(2000,read_serial)
root.mainloop()
root.destroy()
ser.close()
