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
aKeyHeld = False
dKeyHeld = False
aStart = 0
dStart = 0
aInteracts = []
dInteracts = []
statusLbl = StringVar()
statusLbl.set("Start")

### Button event monitor
class App(object):
    def __init__(self, master1, **kwargs):
        self.master1=master
        master1.bind('<KeyRelease>',self.release)
        master1.bind('<KeyPress>',self.press)
        
    def press(self,event):
        global aKeyHeld, dKeyHeld, aStart, dStart

        if started and not paused and not finished:
            if event.keysym=='a':
                canvas.itemconfig(rectN, fill='red')
                if aKeyHeld == False:
                    aStart = time.time()
                    aKeyHeld = True

            elif event.keysym=='d':
                canvas.itemconfig(rectF, fill='red')
                if dKeyHeld == False:
                    dStart = time.time()
                    dKeyHeld = True

        if event.keysym=='space':
            status()
            
    def release(self,event):
        global aKeyHeld, dKeyHeld, aInteracts, dInteracts

        if event.keysym=='a':
            if aKeyHeld:
                canvas.itemconfig(rectN, fill='gray')
                aEnd = time.time()
                dif = aEnd-aStart
                aInteracts.append(dif)
                aKeyHeld = False
            
        elif event.keysym=='d':
            if dKeyHeld:
                canvas.itemconfig(rectF, fill='gray')
                dEnd = time.time()
                dif = dEnd-dStart
                dInteracts.append(dif)
                dKeyHeld = False

### Clock management:

# Fixes potential issue with user rapidly clicking pause
def clockCheck():
    global clockDead

    clockDead = True

    if clockRunning:
        clockDead = False

# Updates timer display and checks if time is up
def clock():
    global secTotal, finished, clockRunning
    
    clockRunning = False
    
    if secTotal > -1 and not paused:
        master.after(1000, clock)
        clockRunning = True
        m, s = divmod(secTotal, 60)
        h, m = divmod(m, 60)

        if h==0:
            currentTimeLbl.configure(text="%02d:%02d" % (m,s))
        elif h>0:
            currentTimeLbl.configure(text="%d:%02d:%02d" % (h,m,s))

        secTotal = secTotal - 1

        master.after(1005, clockCheck)

    if secTotal == -1:
        currentTimeLbl.configure(text="DONE", fg="red")
        finished = True
        statusLbl.set("End/Print")
        statusButton.place_forget()
        statusButton.place(x=60, y=60)
        
### Button Functions:

# Start the timer for the amount of time input
def start():
    global secTotal, started
    
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
            messagebox.showwarning("Invalid Input", "Only put whole numbers in 'min' and 'sec' boxes. Letters, spaces, and non-numeric symbols are not allowed")
            error = True
            minEnt.delete(0,END)
            secEnt.delete(0,END)
       
    if not error:
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

# Toggle paused state
def status():
    global paused
    
    if(finished):
        done()

    elif(not started):
        start()

    elif(started and not paused):
        paused = True
        statusLbl.set("Resume")
        currentTimeLbl.configure(fg="red")
        statusButton.place_forget()
        statusButton.place(x=63, y=60)

    elif(started and paused):
        paused = False
        statusLbl.set("Pause")
        currentTimeLbl.configure(fg="black")
        statusButton.place_forget()
        statusButton.place(x=68, y=60)

        if clockDead:
            master.after(500,clock)

# Export data as CSV file and close program
def done():
    time = datetime.datetime.now().strftime("%H-%M-%S")
    date = datetime.datetime.now().strftime("%d-%m-%y")
    dateStr = str(date)
    timeStr = str(time)
    
    with open('DualTimer_' + dateStr + '_' + timeStr + '.csv', 'w', newline= '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Timer 1 (a key)", 'Duration (sec)']])
        for i in range(0,len(aInteracts),1):
            writer.writerows([[i+1, str(aInteracts[i])]])
        writer.writerow('')
        writer.writerows([["Timer 2 (d key)", 'Duration (sec)']])
        for i in range(0,len(dInteracts),1):
            writer.writerows([[i+1, str(dInteracts[i])]])
            
    messagebox.showinfo("File Location", "CSV file including experiment data exported to folder containing program file")
    
    canvas.master.destroy()

# Before closing window, gives the option to export data
def closed():
    result = messagebox.askyesno("DATA NOT SAVED","Would you like save to your data? If you click no, your data will not be exported")
    if result:
        done()
    else:
        canvas.master.destroy()

### Graphics:

#Key pressed displays
canvas = Canvas(master, width=175, height=175)
rectN = canvas.create_rectangle(  25, 100 , 75, 150, fill='gray')
rectF = canvas.create_rectangle(  100, 100 , 150, 150, fill='gray')
canvas.create_text(50,115, text="Timer 1")
canvas.create_text(125,115, text="Timer 2")
canvas.create_text(50,135, text="('a' Key)")
canvas.create_text(125,135, text="('d' Key)")

#Time Input objects
entLbl = Label(master, text="Enter Time:")
entLbl.place(x=55,y=0)
minLbl = Label(master, text="min", bd=0)
minLbl.place(x=60,y=15)
secLbl = Label(master, text="sec", bd=0)
secLbl.place(x=95,y=15)
colonLbl = Label(master, text=":")
colonLbl.place(x=84,y=28)
minEnt = Entry(master, width=3)
minEnt.place(x=60,y=30)
secEnt = Entry(master, width=3)
secEnt.place(x=95,y=30)

#Time Display objects
Timelbl = Label(master, text="Time Remaining:")
currentTimeLbl = Label(master, text="00:00")
statusButton = Button(master, textvariable=statusLbl,command=status)
statusButton.place(x=70,y=60)


master.protocol("WM_DELETE_WINDOW",closed)
canvas.pack()
app=App(master)
mainloop()
