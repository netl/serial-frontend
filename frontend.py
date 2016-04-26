from Tkinter import *
import tkFont
import serial

#events
def cmd_start(event):
	if loadstatus and (meas.count==100 or meas.count==0):
		canv.itemconfig(buttonStart, image=image_start_pressed)
		canv.itemconfig(buttonStartAddon, image=image_start_addon_pressed)
		clear_results()
		ser.write(str(meas.points))
		ser.write(". ")
		ser.write(str(meas.delay))
		ser.write(". ")
		ser.write(str(meas.dist))
		ser.write(". meas\r\n")

def cmd_start_addon(event):
	if loadstatus and (meas.count==100 or meas.count==0):
		global resCount
		resCount = -1	#we want to spoof a blank result
		cmd_start(1)

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
	canv.itemconfig(buttonStartAddon, image=image_start_addon)
	canv.itemconfig(buttonTray, image=image_tray)

def graph_results():
   #draw the graph
   for x in xrange(0,meas.count-1):
      canv.coords(canv.graph[x],x*4.8,333-meas.values[x]/7000,(x+1)*4.8,333-meas.values[x+1]/7000)

   #draw information measurement completed
   if meas.count == meas.points or meas.count == 0 and  resCount >= 0:
      canv.itemconfig(textResult, text=meas.result)
      canv.itemconfig(textControl, text=meas.controlResult)
      if meas.controlResult:
         canv.itemconfig(textRatio, text=float("{0:.2f}".format(float(meas.result)/float(meas.controlResult))))
      else:
         canv.itemconfig(textRatio, text="-.--")
      canv.coords(boxControl, meas.controlArea[0]*4.8,348,meas.controlArea[1]*4.8,144)
      canv.coords(boxResult, meas.resultArea[0]*4.8,348,meas.resultArea[1]*4.8,144)
      canv.coords(textControlText,(meas.controlArea[0]+meas.controlArea[1])/2*4.8,182)
      canv.coords(textResultText,(meas.resultArea[0]+meas.resultArea[1])/2*4.8,182)

def clear_results(): 
	#hide the graph by moving it above the screen
	for x in xrange(0,100):
		meas.values[x] = 7000000 
	for x in xrange(0,99):
		canv.coords(canv.graph[x],x*4.8,333-meas.values[x]/7000,(x+1)*4.8,333-meas.values[x+1]/7000)
	for x in xrange(0,2):
		meas.controlArea[x]=700
		meas.resultArea[x]=700

	#clear results
	meas.result = 0
	meas.controlResult = 0
	graph_results()

	#clear measurement settings
	meas.count = 0
	meas.control = 0

def read_serial():
	while ser.inWaiting():
		global result
		global resCount
		data = ser.readline()
		print data,
		info = data.split()
		if not len(info)== 0:
			if info[-1]=='result':
				if not resCount == -1:	#do we want to yield results?
					meas.values[meas.count] = result[resCount][meas.count]
					#meas.values[meas.count] = info[-2]
					if meas.values[meas.count] > 5000 and (meas.control==0 or meas.control==2):	#found the start of a signal
						if meas.control == 0:
							meas.controlArea[0] = meas.count-2
						else:
							meas.resultArea[0] = meas.count-2
						meas.control +=1
					if meas.control == 1:	#at the control signal
						if meas.values[meas.count] > 5000:
							meas.controlResult += meas.values[meas.count]
						else:
							meas.controlArea[1] = meas.count
							meas.control +=1
					if meas.control == 3:	#at the test signal
						if meas.values[meas.count] > 5000:
							meas.result += meas.values[meas.count]
						else:
							meas.resultArea[1] = meas.count
							meas.control +=1
				else:
					meas.values[meas.count] = 0
				meas.count += 1
				graph_results()
			if info[-1]=='donemeas':
				if resCount <2:
					resCount += 1
				else:
					resCount = 0
	root.after(10,read_serial)

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
   result = 2220000	#sum of counts
   points = 100	#how many measurements
   delay = 1	#delay between measurements
   dist = 3	#distance between measurements
   count = 0	#number of counts completed
   values = range(self.points)

#meas = range(100)
result = [1708,1697,1567,1674,1735,1810,1783,1805,1777,1839,1929,1767,1726,1805,2580,3959,4132,5746,9733,32121,155923,313493,514742,560879,508364,338033,137656,50096,22319,10980,5721,4889,2358,1618,1465,1542,1611,1345,1113,1162,1397,1177,815,737,641,835,1128,1597,1373,1011,1060,1387,1639,1555,1404,1783,2547,2378,1809,1530,1512,1728,2412,2657,2537,3673,3590,2806,4112,15804,50717,286707,595491,793036,825992,794012,621795,381754,214863,68211,18981,4193,4032,3723,4117,3886,4044,4379,3529,2812,3028,2668,2043,1674,1709,1721,1721,1690,1823,1728,1978],[1708,1697,1567,1674,1735,1810,1783,1805,1777,1839,1929,1767,1726,1805,2580,3959,4132,5746,10745,33452,156846,314648,515483,561650,509615,339462,138342,51211,23129,11735,5721,4889,2358,1618,1465,1542,1611,1345,1113,1162,1397,1177,815,737,641,835,1128,1597,1373,1011,1060,1387,1639,1555,1404,1783,2547,2378,1809,1530,1512,1728,2412,2657,2537,3673,3590,2806,4112,16376,51837,287837,596837,794613,826185,795614,622837,382615,215716,69635,19625,4193,4032,3723,4117,3886,4044,4379,3529,2812,3028,2668,2043,1674,1709,1721,1721,1690,1823,1728,1978],[1708,1697,1567,1674,1735,1810,1783,1805,1777,1839,1929,1767,1726,1805,2580,3959,4132,5746,8871,32015,155637,313837,514635,560635,508123,338416,137352,50173,22415,9715,5721,4889,2358,1618,1465,1542,1611,1345,1113,1162,1397,1177,815,737,641,835,1128,1597,1373,1011,1060,1387,1639,1555,1404,1783,2547,2378,1809,1530,1512,1728,2412,2657,2537,3673,3590,2806,4112,14746,50617,286617,595815,793065,815234,794649,621840,381325,214672,68954,18641,4193,4032,3723,4117,3886,4044,4379,3529,2812,3028,2668,2043,1674,1709,1721,1721,1690,1823,1728,1978]
resCount = 0


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
#canv.end = Button(root, text="quit", command=quit)
#canv.end.place(x=15, y=15, width=30, height=30)
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
#ser.close()
