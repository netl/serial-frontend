from Tkinter import *
import tkFont
import serial

#events
def cmd_start(event):
	if loadstatus and (meas.count==100 or meas.count==0):
		canv.itemconfig(buttonStart, image=image_start_pressed)
		clear_results()
		ser.write(str(meas.points))
		ser.write(". ")
		ser.write(str(meas.delay))
		ser.write(". ")
		ser.write(str(meas.dist))
		ser.write(". meas\r\n")

def cmd_tray(event):
	if meas.count==100 or meas.count==0:
		global loadstatus
		canv.itemconfig(buttonTray, image=image_tray_pressed)
		if loadstatus:
			loadstatus=0
			ser.write("unload\r\n")
		else:
			loadstatus=1
			ser.write("load homemv\r\n")
			clear_results()

def clear_buttons(event):
	canv.itemconfig(buttonStart, image=image_start)
	canv.itemconfig(buttonTray, image=image_tray)

def graph_results():
   global w
   wScale = w/meas.points #density of result points
   hScale = 1/7000 #scale for results
   hOffset = 333 #offset from top of the screen
   #draw the graph
   for x in xrange(0,meas.count-1):
      canv.coords(canv.graph[x],x*wScale,hOffset-meas.values[x]*hScale,(x+1)*wScale,hOffset-meas.values[x+1]*hScale)
   #draw information measurement completed
   if meas.count == meas.points or meas.count == 0:
      canv.itemconfig(textResult, text=meas.result)
      canv.itemconfig(textControl, text=meas.controlResult)
      if meas.controlResult:
         canv.itemconfig(textRatio, text=float("{0:.2f}".format(float(meas.result)/float(meas.controlResult))))
      else:
         canv.itemconfig(textRatio, text="-.--")
      canv.coords(boxControl, meas.controlArea[0]*wScale,348,meas.controlArea[1]*wScale,144)
      canv.coords(boxResult, meas.resultArea[0]*wScale,348,meas.resultArea[1]*wScale,144)
      canv.coords(textControlText,(meas.controlArea[0]+meas.controlArea[1])/2*wScale,182)
      canv.coords(textResultText,(meas.resultArea[0]+meas.resultArea[1])/2*wScale,182)

def clear_results(): 
   global w
	#hide the graph by moving it above the screen
	for x in xrange(0,meas.points):
		meas.values[x] = 7000000 #massive value due to the scaling
	for x in xrange(0,2):
		meas.controlArea[x]=w/meas.points
		meas.resultArea[x]=w/meas.points
	#clear results
	meas.result = 0
	meas.controlResult = 0
	graph_results()
	#clear measurement settings
	meas.count = 0
	meas.control = 0

def read_serial():
	while ser.inWaiting():
		data = ser.readline()
		info = data.split()
      if info[-1]=='result': #are we yielding results?
         meas.values[meas.count] = int(info[-2])
         #search for the control and measurement
         if meas.values[meas.count] > meas.threshold: #are we detecting something?
            if meas.control==0 or meas.control==2: #found the start of a signal
               if meas.control == 0:
                  meas.controlArea[0] = meas.count-2
               else:
                  meas.resultArea[0] = meas.count-2
               meas.control +=1
            #update counts
            if meas.control == 1: #at the control signal
                  meas.controlResult += meas.values[meas.count]
            if meas.control == 3: #at the test signal
                  meas.result += meas.values[meas.count]
         else:
            #check if we found the edge of a signal
            if meas.control == 1: #control
               meas.controlArea[1] = meas.count
            elif meas.control == 3: #measurement
               meas.resultArea[1] = meas.count
            meas.control +=1
         meas.count += 1

      if info[-1]=='donemeas': #measurement complete
         meas.values[meas.count] = 0
         graph_results()
	root.after(10,read_serial) #keep checking

#setup
ser = serial.Serial('/dev/ttyAMA0', 115200)
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.config(cursor="none") 

class meas:
   loadstatus = 1 #the tray is in
   controlResult = 1000000 #sum of counts in control
   controlArea = range(2) #range for control counts
   resultArea = range(2) #range for result counts
   control = 0	#flag for searching for control during measurement
   trheshold = 5000 #minimum amount of counts to be counted as a measurement
   result = 2220000	#sum of counts at measurement area
   points = 100	#how many measurements
   delay = 1	#delay between measurements
   dist = 3	#distance between measurements
   count = 0	#number of counts completed
   values = range(self.points)

#images
tausta = PhotoImage(file="./labrox/taustakuva.gif")
image_quit = PhotoImage(file="./labrox/quit.gif")
image_start = PhotoImage(file="./labrox/start.gif")
image_tray = PhotoImage(file="./labrox/tray.gif")
image_start_pressed = PhotoImage(file="./labrox/start_pressed2.gif")
image_tray_pressed = PhotoImage(file="./labrox/tray_pressed2.gif")
image_start_addon = PhotoImage(file="./labrox/start_addon.gif")
image_start_addon_pressed = PhotoImage(file="./labrox/start_addon_pressed.gif")

#create canvas and objects
canv = Canvas(root, width=w, height=h)
canv.create_image(0,0, image=tausta, anchor='nw')

#buttons
buttonQuit = canv.create_image(0, 0, image=image_quit, anchor='nw')
buttonStart = canv.create_image(45, 634, image=image_start, anchor='sw')
buttonTray = canv.create_image(45, 755, image=image_tray, anchor='sw')
buttonStartAddon = canv.create_image(45+332, 634, image=image_start_addon, anchor='sw')

#areas for control and test
boxControl =  canv.create_rectangle(-1,-1,-1,-1,outline="#5e625c",fill="#5e625c")	#control
boxResult =  canv.create_rectangle(-1,-1,-1,-1,outline="#5e625c",fill="#5e625c")	#result

#text
font = tkFont.Font(family="Roboto", size=24)
fontSmall = tkFont.Font(family="Roboto", size=15)
canv.create_text(93, 425, text="Control:", font=font, fill="white", anchor='sw')
canv.create_text(93, 461, text="Test:", font=font, fill="white", anchor='sw')
canv.create_text(93, 497, text="T/C ratio:", font=font, fill="white", anchor='sw')
textControlText = canv.create_text(500, 0, text="Control", font=fontSmall, fill="white", anchor='s')
textResultText = canv.create_text(500, 0, text="Test", font=fontSmall, fill="white", anchor='s')
textControl = canv.create_text(240, 425, text="1000000", font=font, fill="white", anchor='sw')
textResult = canv.create_text(240, 461, text="2220000", font=font, fill="white", anchor='sw')
textRatio = canv.create_text(240, 497, text="2.22", font=font, fill="white", anchor='sw')

#draw graphs
canv.graph = range(100)
for x in xrange(0,99):
	canv.graph[x] = canv.create_line(x*4.8,333,(x+1)*4.8,333,fill="#bfce00",width=3)

#bind events
canv.tag_bind(buttonQuit, '<ButtonPress-1>', quit)
canv.tag_bind(buttonStart, '<ButtonPress-1>', cmd_start)
canv.tag_bind(buttonTray, '<ButtonPress-1>', cmd_tray)
canv.tag_bind(buttonStart, '<ButtonRelease-1>', clear_buttons)
canv.tag_bind(buttonTray, '<ButtonRelease-1>', clear_buttons)
canv.tag_bind(buttonStartAddon, '<ButtonPress-1>', cmd_start_addon)
canv.tag_bind(buttonStartAddon, '<ButtonRelease-1>', clear_buttons)

#home the tray
ser.write("home\r\n")

#loop, and cleanup
canv.pack()
clear_results()
root.after(10,read_serial)

root.mainloop()
root.destroy()
ser.close()
