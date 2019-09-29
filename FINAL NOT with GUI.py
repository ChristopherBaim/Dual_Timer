from tkinter import *
from tkinter import messagebox
import datetime
import time
import csv
import sys

master = Tk()
started = False
paused = False
finished = False
error = False
statusLbl = StringVar()
statusLbl.set("Start")
aTotal = 0
aStart = 0
aEnd = 0
dTotal = 0
dStart = 0
dEnd = 0
aKeyHeld = False
dKeyHeld = False
aInteracts = []
dInteracts = []
aTimes = 0
dTimes = 0


class App(object):
    def __init__(self, master1, **kwargs):
        self.master1=master
        master1.bind('<KeyRelease>',self.release)
        master1.bind('<KeyPress>',self.press)
        
    def press(self,event):
        global aKeyHeld
        global dKeyHeld
        global aStart
        global dStart    
        global aTimes
        global dTimes
        global paused
        global finished

        if started and not paused and not finished:
            if event.keysym=='a':
                canvas.itemconfig(rectN, fill='red')
                if aKeyHeld == False:
                    aStart = time.time()
                    aKeyHeld = True
                    aTimes = aTimes + 1

                
            elif event.keysym=='d':
                canvas.itemconfig(rectF, fill='red')
                if dKeyHeld == False:
                    dStart = time.time()
                    dKeyHeld = True
                    dTimes = dTimes +1


        if event.keysym=='space':
            print("\n")
            print("total time 'a' (sec): " + str(aTotal))
            print("total time 'd' (sec): " + str(dTotal))
            print("number of times 'a' interacted: " + str(aTimes))
            print("number of times 'd' interacted: " + str(dTimes))

            
    def release(self,event):
        global aKeyHeld
        global dKeyHeld
        global aEnd
        global aStart
        global aTotal
        global dEnd
        global dStart
        global dTotal
        global aInteracts
        global dInteracts
        global aTimes
        global dTimes
        

        
        if event.keysym=='a':
            if aKeyHeld:
                canvas.itemconfig(rectN, fill='gray')
                aEnd = time.time()
                dif = aEnd-aStart
                aInteracts.append(dif)
                aTotal = dif + aTotal
                dif = 0
                aKeyHeld = False
                #print('a Released') #troubleshooting
            
        elif event.keysym=='d':
            if dKeyHeld:
                canvas.itemconfig(rectF, fill='gray')
                dEnd = time.time()
                dif = dEnd-dStart
                dInteracts.append(dif)
                dTotal = dif + dTotal
                dif = 0
                dKeyHeld = False
                #print('d Released') #troubleshooting

#clock management            
def clockCheck():
    global clockRunning
    global clockDead

    clockDead = True

    if clockRunning:
        clockDead = False
##    if clockDead:
##        print("RIP clock")

def clock():
    global secTotal
    global finished
    global paused
    global clockRunning
    
    clockRunning = False
    
    if secTotal > -1 and not paused:
        master.after(1000,clock)
        clockRunning = True
        m, s = divmod(secTotal, 60)
        h, m = divmod(m, 60)
        #print("tick tock")
        if h==0:
            #print("%02d:%02d" % (m,s)) #troubleshooting
            currentTimeLbl.configure(text="%02d:%02d" % (m,s))
        elif h>0:
            #print("%d:%02d:%02d" % (h,m,s)) #troubleshooting
            currentTimeLbl.configure(text="%d:%02d:%02d" % (h,m,s))

        secTotal = secTotal - 1
        
        
        master.after(1005, clockCheck)

    if secTotal == -1:
        currentTimeLbl.configure(text="DONE", fg="red")
        finished = True
        statusLbl.set("End/Print")
        statusButton.place_forget()
        statusButton.place(x=60, y=60)
        
########Buttons and their functions
def start():
    global secTotal
    global error
    global started
    
    emptyMin = False
    emptySec = False
    minIn = minEnt.get()
    secIn = secEnt.get()
    
    if not minEnt.get():
        emptyMin = True
        minIn = 0
    if not secEnt.get():
        emptySec = True
        secIn = 0
        
    if emptyMin and emptySec:
        messagebox.showwarning("No Input", "Enter the duration of your experiment before pressing click 'Start'")
        error = True
    else:
        try:
            minIn = int(minIn)
            secIn = int(secIn)
            error = False
        except ValueError:
            messagebox.showwarning("Invalid Input", "Only put numbers in 'min' and 'sec' boxes. Letters, spaces, and non-numeric symbols are not allowed")
            error = True
            minEnt.delete(0,END)
            secEnt.delete(0,END)
       
    if not error:
        #print("start run")
        secTotal = secIn + (60*minIn)
        started = True
        statusLbl.set("Pause")
        statusButton.place_forget()
        statusButton.place(x=68, y=60)
        
        minEnt.place_forget()
        secEnt.place_forget()
        minLbl.place_forget()
        secLbl.place_forget()
        colonLbl.place_forget()
        entLbl.place_forget()
        
        Timelbl.place(x=40, y=10)
        currentTimeLbl.place(x=70,y=30)

        clock()
        

def status():
    global started
    global paused
    global finished
    global error
    global clockDead
    
    if(finished):
        done()
        #print("Done")
    elif(not started):
        start()
        #print("Start pressed")
    elif(started and not paused):
        paused = True
        statusLbl.set("Resume")
        currentTimeLbl.configure(fg="red")
        statusButton.place_forget()
        statusButton.place(x=63, y=60)
        #print("Paused")
    elif(started and paused):
        paused = False
        statusLbl.set("Pause")
        currentTimeLbl.configure(fg="black")
        statusButton.place_forget()
        statusButton.place(x=68, y=60)

        if clockDead:
            master.after(500,clock)

      
def done():
    print("\n")
    print("At end of experiment, totals were:")
    print("total time 'a' (sec): " + str(aTotal))
    print("total time 'd' (sec): " + str(dTotal))
    print("number of times 'a' interacted: " + str(aTimes))
    print("number of times 'd' interacted: " + str(dTimes))
    if aTimes != 0:
        aAvg = aTotal/aTimes
        print("avg time per 'a' interaction (sec): " + str(aAvg) + " seconds")
    elif aTimes == 0:
        print("avg time per 'a' interaction: 0 because no interactions!")
    if dTimes != 0:
        dAvg = dTotal/dTimes
        print("avg time per 'd' interaction (sec): " + str(dAvg) +  " seconds")
    elif dTimes == 0:
        print("avg time per 'd' interaction: 0 because no interactions!")        

    time = datetime.datetime.now().strftime("%H-%M-%S")
    date = datetime.datetime.now().strftime("%d-%m-%y")
    dateStr = str(date)
    timeStr = str(time)
    
    with open('Novel Object Test_' + dateStr + '_' + timeStr + '.csv', 'w', newline= '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([['Novel Object Interaction number', 'Duration']])
        for i in range(0,len(aInteracts),1):
            writer.writerows([[i+1, str(aInteracts[i])]])
        writer.writerow('')
        writer.writerows([['Familiar Object Interaction number', 'Duration']])
        for i in range(0,len(dInteracts),1):
            writer.writerows([[i+1, str(dInteracts[i])]])
            
    messagebox.showinfo("File Location", "CSV file including experiment data exported to folder containing python file")
    
    canvas.master.destroy()





######Graphics:     

#Key pressed displays
canvas = Canvas(master, width=175, height=175)
rectN = canvas.create_rectangle(  25, 100 , 75, 150, fill='gray')
rectF = canvas.create_rectangle(  100, 100 , 150, 150, fill='gray')
canvas.create_text(50,115, text="Novel")
canvas.create_text(125,115, text="Familiar")
canvas.create_text(50,135, text="(aKey)")
canvas.create_text(125,135, text="(dKey)")

#Enter Time objects
entLbl = Label(master, text="Enter Time:")
minLbl = Label(master, text="min", bd=0)
secLbl = Label(master, text="sec", bd=0)
colonLbl = Label(master, text=":")
minEnt = Entry(master, width=3)
secEnt = Entry(master, width=3)

#Time Display objects
Timelbl = Label(master, text="Time Remaining:")
currentTimeLbl = Label(master, text="00:00")
statusButton = Button(master, textvariable=statusLbl,command=status)
#endButton = Button(master, text="End/Print",command=done)

#Enter Time placement
entLbl.place(x=55,y=0)
minLbl.place(x=60,y=15)
secLbl.place(x=95,y=15)
colonLbl.place(x=84,y=28)
minEnt.place(x=60,y=30)
secEnt.place(x=95,y=30)

#Buttons
statusButton.place(x=70,y=60)
#endButton.place(x=95,y=60)

def closed():
    result = messagebox.askyesno("DATA NOT SAVED","Would you like save to your data? If you click no, your data will not be exported")
    if result:
        done()
    else:
        canvas.master.destroy()

master.protocol("WM_DELETE_WINDOW",closed)
canvas.pack()
app=App(master)
mainloop()
