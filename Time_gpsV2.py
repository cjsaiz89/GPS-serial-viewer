import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import calendar
import serial

# ------------------------------------------------------
# Parameters to change:
usb_port = 'COM5' # change to your port, check where is connected the gps
text_font = ( 'Consolas' , 12) 
enable_progress_bar = False # change to False to disable green progress bar
# ------------------------------------------------------


class gpstime:
    def __init__(self, hh, mm, ss):
        self.hh = hh
        self.mm = mm
        self.ss = ss

class gpsdate:
    def __init__(self, d, m, y):
        self.d = d
        self.m = m
        self.y = y

def deg(x):
    lx = len(str(int(float(x))))
    xdeg = str(int(float(x)))
    if ( lx == 3):
        return xdeg[0:1]
    elif ( lx == 4):
        return xdeg[0:2]
    elif ( lx == 5):
        return xdeg[0:3]

def min(x):
    lx = len(str(int(float(x))))
    xmin = str(float(x))
    if (lx == 3):
        return xmin[1:]
    elif (lx == 4):
        return xmin[2:]
    elif (lx == 5):
        return xmin[3:]    

def zero(x):
    if x < 10:
        return '0'+str(x)
    elif x > 9:
        return str(x)

def get_gps():
        
    if(myport.in_waiting > 0):
        line = myport.readline()
        print(line)
        dline = line.decode('Ascii')
        
        if '$GPRMC' in dline:
            lline = dline.split(',')
            utc_date = lline[9]
            utc_time = lline[1]
            utc_date = gpsdate(utc_date[0:2], utc_date[2:4], utc_date[4:6])
            utc_time = gpstime(utc_time[0:2], utc_time[2:4], utc_time[4:6])
            lat = lline[3]
            lat_deg = int(deg(lat))
            lat_min = float(min(lat))
            ns = lline[4]
            lon = lline[5]
            lon_deg = int(deg(lon))
            lon_min = float(min(lon))
            ew = lline[6]
            v = lline[7]
            hdg = lline[8]            
            lbl_latd.configure( text = (lat_deg, '°', lat_min, "'", ns ), font = text_font)
            lbl_lond.configure( text = (lon_deg, '°',lon_min, "'", ew), font = text_font)
            lbl_v_hdg.configure( text = ( v, 'kt ',hdg,'°'), font = text_font)
            # deg min sec
            lat_int_min = zero(int(lat_min))
            lon_int_min = zero(int(lon_min))
            lat_sec = (lat_min - int(lat_min))*60
            lon_sec = (lon_min - int(lon_min))*60
            lbl_latd2.configure( text = (lat_deg, '°',lat_int_min,"'","{:.2f}".format(lat_sec), "\"" ), font = text_font)
            lbl_lond2.configure( text = (lon_deg, '°',lon_int_min, "'","{:.2f}".format(lon_sec) , "\""), font = text_font)
    

# updating loop
def get_time():
        # update local
        lblday.configure( text = datetime.now().day)
        lblmonth.configure( text = datetime.now().month)
        lblyear.configure( text = datetime.now().year)
        lblhour.configure( text = datetime.now().hour)
        lblminute.configure( text = datetime.now().minute)
        lblsecond.configure( text = datetime.now().second)
        ms = int(datetime.now().microsecond/1000)
        lblms.configure( text = ms )
        if enable_progress_bar == True :
            bar.configure( mode = 'determinate', maximum = 1000, value = ms )
        # update gmt
        lblgday.configure( text = datetime.utcnow().day)
        lblgmonth.configure( text = datetime.utcnow().month)
        lblgyear.configure( text = datetime.utcnow().year)
        lblghour.configure( text = datetime.utcnow().hour)
        lblgminute.configure( text = datetime.utcnow().minute)
        lblgsecond.configure( text = datetime.utcnow().second)
        lblgyearday.configure( text = time.gmtime().tm_yday)
        # calendar
        caltxt.delete('1.0','end')
        txt_cal = c.formatmonth(datetime.utcnow().year, datetime.utcnow().month)
        caltxt.insert('1.0', txt_cal)
        get_gps()
        root.after(1, get_time) # recursive



root = Tk()
#root.geometry('400x200')
root.title('Clock')
frame_font = 'consolas'
frame1 = LabelFrame(root, text = 'LOCAL', font = (frame_font), fg = 'blue')
frame2 = LabelFrame(root, text = 'UTC', font = (frame_font), fg = 'red')
frame3 = LabelFrame(root, text = 'CALENDAR', font = (frame_font), fg = 'green')
frame4 = LabelFrame(root, text = 'GPS', font = (frame_font), fg = 'magenta')
# organize frames
frame1.grid(row = 0, column = 1, sticky = 'nsew')
frame2.grid(row = 0, column = 2, sticky = 'nsew')
frame3.grid(row = 0, column = 3, sticky = 'nsew')
frame4.grid(row = 0, column = 4, sticky = 'nsew')
# Local values
Label(frame1, text = 'Day:', justify = RIGHT, font = text_font ).grid(row = 0, column = 1)
lblday = Label(frame1, width = 2 , font = text_font)
lblday.grid(row = 0, column = 2)
Label(frame1, text = 'Month:', justify = RIGHT, font = text_font).grid(row = 1, column = 1)
lblmonth = Label(frame1, justify = RIGHT, font = text_font)
lblmonth.grid(row = 1, column = 2)
Label(frame1, text = 'Year:', justify = RIGHT, font = text_font).grid(row = 2, column = 1)
lblyear = Label(frame1, justify = RIGHT, font = text_font)
lblyear.grid(row = 2, column = 2)
Label(frame1, text = 'Hour:', justify = RIGHT, font = text_font).grid(row = 3, column = 1)
lblhour = Label(frame1, justify = RIGHT, font = text_font)
lblhour.grid(row = 3, column = 2)
Label(frame1, text = 'minute:', justify = RIGHT, font = text_font).grid(row = 4, column = 1)
lblminute = Label(frame1, justify = RIGHT, font = text_font)
lblminute.grid(row = 4, column = 2)
Label(frame1, text = 'Second:', justify = RIGHT, font = text_font).grid(row = 5, column = 1)
lblsecond = Label(frame1, justify = RIGHT, font = text_font)
lblsecond.grid(row = 5, column = 2)
Label(frame1, text = 'uS:', justify = RIGHT, font = text_font).grid(row = 6, column = 1)
lblms = Label(frame1, justify = RIGHT, width = 3 , font = text_font)
lblms.grid(row = 6, column = 2)
# Progressbar
if enable_progress_bar == True :
    bar = ttk.Progressbar(root, orient = 'horizontal', length = 180)
    bar.grid(row = 7, column = 1, columnspan = 2 )
# GMT values
Label(frame2, text = 'Day:', justify = RIGHT, font = text_font).grid(row = 0, column = 1)
lblgday = Label(frame2, width = 2 , font = text_font)
lblgday.grid(row = 0, column = 2)
Label(frame2, text = 'Month:', justify = RIGHT, font = text_font).grid(row = 1, column = 1)
lblgmonth = Label(frame2, justify = RIGHT, font = text_font)
lblgmonth.grid(row = 1, column = 2)
Label(frame2, text = 'Year:', justify = RIGHT, font = text_font).grid(row = 2, column = 1)
lblgyear = Label(frame2, justify = RIGHT, font = text_font)
lblgyear.grid(row = 2, column = 2)
Label(frame2, text = 'Hour:', justify = RIGHT, font = text_font).grid(row = 3, column = 1)
lblghour = Label(frame2, justify = RIGHT, font = text_font)
lblghour.grid(row = 3, column = 2)
Label(frame2, text = 'minute:', justify = RIGHT, font = text_font).grid(row = 4, column = 1)
lblgminute = Label(frame2, justify = RIGHT, font = text_font)
lblgminute.grid(row = 4, column = 2)
Label(frame2, text = 'Second:', justify = RIGHT, font = text_font).grid(row = 5, column = 1)
lblgsecond = Label(frame2, justify = RIGHT, font = text_font)
lblgsecond.grid(row = 5, column = 2)
Label(frame2, text = 'Year-day:', justify = RIGHT, font = text_font).grid(row = 6, column = 1)
lblgyearday = Label(frame2, justify = RIGHT, font = text_font)
lblgyearday.grid(row = 6, column = 2)

# Calendar
c = calendar.TextCalendar(calendar.SUNDAY)
caltxt = Text(frame3, width = 20, height = 10 , font = text_font)
caltxt.grid(row = 0, column = 1)



# GPS start serial
myport = serial.Serial(port = usb_port, baudrate=4800, bytesize=8,timeout=2, stopbits=serial.STOPBITS_ONE)


Label(frame4, text = 'Position dm.m: ', justify = LEFT, font = text_font).grid(row = 0, column = 1)
# LAT
lbl_latd = Label(frame4, justify = RIGHT)
lbl_latd.grid(row = 0, column = 2)

# LONG
lbl_lond = Label(frame4, justify = RIGHT)
lbl_lond.grid(row = 0, column = 3)

# MOTION
Label(frame4, text = 'Speed/Heading: ', justify = LEFT, font = text_font).grid(row = 1, column = 1)

lbl_v_hdg = Label(frame4, justify = RIGHT)
lbl_v_hdg.grid(row = 1, column = 2)

Label(frame4, text = 'Position dms: ', justify = LEFT, font = text_font).grid(row = 2, column = 1)
lbl_latd2 = Label(frame4, justify = RIGHT)
lbl_latd2.grid(row = 2, column = 2)

lbl_lond2 = Label(frame4, justify = RIGHT)
lbl_lond2.grid(row = 2, column = 3)


get_gps()


# enter infinite loop
get_time()      

root.mainloop()