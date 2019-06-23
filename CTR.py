

from tkinter import *
import time
import subprocess
import os
from tkinter import ttk
from tkinter import filedialog
from winreg import *
from pynput.keyboard import Key, Controller
import serial
import threading












           





consoleregkey=OpenKey(HKEY_CURRENT_USER, r"console", 0, KEY_WRITE)
SetValueEx(consoleregkey ,"WindowPosition",1,REG_DWORD, 0xfe0018)
SetValueEx(consoleregkey ,"WindowsIZE",1,REG_DWORD, 0X190050)

'''pythonregkey=OpenKey(HKEY_CURRENT_USER, r"console\C:_Python 3.7_python.exe", 0, KEY_WRITE)
SetValueEx(pythonregkey ,"WindowPosition",1,REG_DWORD, 0XC8001E)
SetValueEx(pythonregkey ,"WindowsIZE",1,REG_DWORD, 0X190050) '''


class state():
     firstmenu=0
     browsekdiag=1
     usb = 2
     testmenu=3
     back = 4
     com = 5
     reset = 6
     full = 7

class TouchButton(Widget):

    def __init__(self, master=None, **kw):
        self.x=kw['x']
        self.y=kw['y']
        self.command=kw['command']
        self.root=Label(
           master,
           image=kw['image'],
           bd=0 ,
           relief=FLAT,
           bg="#CCCCFF")
        self.root.bind(
            '<Button-1>', 
            lambda _:self.movewidget())
        self.root.bind('<ButtonRelease-1>',
            lambda _:self.movewidget(1))
        self.root.pack()
        self.place()


    def movewidget(self,i=0,event=None):

        
        try:           
            xx=int(self.root.place_info().get('x'))
            yy=int(self.root.place_info().get('y'))
            if i == 0:
                self.root.after(0,self.command)
                self.root.place(x= xx+2 , y=yy+2)
                self.root.update()
                #self.root.after(100,lambda  : self.movewidget(1))
            elif i == 1:
                self.root.place(x= xx-2 , y=yy-2)            
                self.root.update()
        except:
            pass
    def place_forget(self):
        self.root.place_forget()
    def place(self):
        self.root.place(x=self.x, y=self.y )


    def state(self, i):
        if i == DISABLED :
            self.root.config(state=DISABLED)
            self.root.unbind('<Button-1>')
            self.root.unbind('<ButtonRelease-1>')
        if i == NORMAL :
            self.root.config(state=NORMAL)
            self.root.bind(
                '<Button-1>', 
                lambda _:self.movewidget())
            self.root.bind('<ButtonRelease-1>',
                lambda _:self.movewidget(1))

class GUI():
    def __init__(self):
        self.root=Tk()
        self.clr="#CCCCFF"
        self.i=1
        self.shutternumber=10
        self.oldstate=state.firstmenu
        self.kybrd=Controller()
        self.kdiagaddress=""
        self.state=state.firstmenu
        self.images()
        self.mainframe()
        self.kdiagaddress,self.v2x=self.CTRconfig()
        self.kdiag=self.kdiagaddress+"/CHDV2X.exe"
        self.settingframe()
        self.exitframe()
        self.buttons()
        self.ser = serial.Serial(
            port = 'COM1',
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 2)
        self.cmnd = self.readcommand()



#_____________________________________________________________________________________________________________________________________________
    def images(self):
        self.imgexit=PhotoImage (
            file=self.resource_path('Shutdown.png'))               #75x75
        self.imggear=PhotoImage (
            file=self.resource_path('gear.png'))
        self.imgarm=PhotoImage (
            file=self.resource_path("adonis.png"))
        self.imgtik=PhotoImage (
            file=self.resource_path('Tik.png'))                 #120x49
        self.imgcross=PhotoImage (
            file=self.resource_path('cross.png'))               #120x49
        self.imgfrmexit1=PhotoImage (
            file=self.resource_path("exitframe1.png"))    #375x200
        self.imgfrmexit2=PhotoImage (
            file=self.resource_path("exitframe2.png")) 
        self.imgfrmsetting1=PhotoImage (
            file=self.resource_path("setting1.png"))
        self.imgfrmsetting2=PhotoImage (
            file=self.resource_path("setting2.png")) 
        self.imgbtnusb=PhotoImage(
            file=self.resource_path("USB.png"))#600X243
        self.imgbtncom=PhotoImage(
            file=self.resource_path("COM.png"))
        self.imgbrowse=PhotoImage(
            file=self.resource_path("browse.png"))   #99x40
        self.imgaddr=PhotoImage(
            file=self.resource_path("address.png"))  #40x325
        self.imgdrop1=PhotoImage(
            file=self.resource_path("drop1.png"))
        self.imgdrop2=PhotoImage(
            file=self.resource_path("drop2.png"))
        self.imgCOM1=PhotoImage(
            file=self.resource_path("COM_1.png"))
        self.imgshutter=PhotoImage(
            file=self.resource_path("shutter.png"))
        self.imgreset=PhotoImage(     
            file=self.resource_path("reset.png"))
        self.imgtrack=PhotoImage(
            file=self.resource_path("track.png"))
        self.imgreject=PhotoImage(
            file=self.resource_path("reject.png"))        
        self.imgup=PhotoImage(
            file=self.resource_path("up.png"))
        self.imgdown=PhotoImage(
            file=self.resource_path("down.png"))
        self.imgfull=PhotoImage(
            file=self.resource_path("full.png"))
        self.imgconfirm=PhotoImage(
            file=self.resource_path("confirm.png"))
        self.imgsensor=PhotoImage(
            file=self.resource_path("sensor.png"))
        self.imgback=PhotoImage(
            file=self.resource_path("Back.png"))
        self.imgstop=PhotoImage(
            file=self.resource_path("stop.png"))

    def mainframe(self):
        self.root.config(bg=self.clr)
        self.root.title('CTR')
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Button-1>",self.ontop)
        self.lbladonisarm=Label(
            self.root,
            image=self.imgarm,
            bd=0, 
            relief=FLAT, 
            bg=self.clr)
        self.lbladonisarm.pack()
        self.lbladonisarm.place(x=15 , y=15)

    def cnftoplevel(self,**kw):
        kw['name'].geometry(kw['geometry'])
        kw['name'].attributes("-topmost",True)
        kw['name'].overrideredirect(True)
        kw['name'].withdraw()
        kw['label'].config(image=kw['image1'], bd=0)
        kw['label'].pack()
        kw['label'].place()
        kw['label'].focus_force()
        if kw['alarm'] == 1:
            kw['label'].bind("<FocusOut>", 
                             lambda   _: self.alarm(kw['label'], 
                                          kw['image1'], 
                                          kw['image2'])) 
        else:
            pass
    
    def settingframe(self, event = None):
        self.frmsetting=Toplevel(self.root)
        self.lblsetting=Label(self.frmsetting) 
        self.cnftoplevel(name=self.frmsetting, 
                         label=self.lblsetting, 
                         geometry="480x320+443+224", 
                         image1=self.imgfrmsetting1, 
                         image2=self.imgfrmsetting2, 
                         alarm=None)
        self.lblkdiag1=Label(self.frmsetting, 
                               bg=self.clr, 
                               text="مسیـــــــر نرم افزار", 
                               font='Nazanin 13 bold', 
                               bd=0)
        self.lblkdiag1.pack()
        self.lblkdiag1.place(x=338, y=30)
        self.lblkdiag2=Label(self.frmsetting, 
                               bg=self.clr, 
                               text="KDIAG", 
                               font='thoma 11 bold', 
                               bd=0)
        self.lblkdiag2.pack()
        self.lblkdiag2.place(x=289, y=30)

        self.entkdiag=Entry(
            self.frmsetting,               
            bg='#53B2FD',                
            fg="black",              
            font="Thoma 17",               
            bd=3, 
            width=23,                              
            highlightthickness=2,     
            highlightbackground="black", 
            selectbackground="black")
        self.entkdiag.pack()
        self.entkdiag.place(x=146, y=54)
        self.entkdiag.insert(0, self.kdiag)

        self.entshutternumber=Entry(
            self.root,                                       
            bg='#53B2FD',
            fg="black", 
            font="BNazanin 60 bold",                          
            bd=4,                      
            highlightthickness=5,             
            highlightbackground="black",                 
            selectbackground="black",      
            width=2)
        self.entshutternumber.pack()
        self.entshutternumber.place(x=918, y=417.4)
        self.entshutternumber.insert(0,self.shutternumber)
        self.entshutternumber.place_forget()


    def buttons(self):
        self.btnusb=TouchButton(
            self.root,              
            image=self.imgbtnusb,                
            x=58,              
            y=276.5,             
            command=lambda : self.popupkdiag("USB"))

        self.btncom=TouchButton(
            self.root, 
            image=self.imgbtncom,    
            x=708, 
            y=276.5,       
            command=lambda : self.popupkdiag("COM"))

        self.btnback=TouchButton(
            self.root, 
            image=self.imgback, 
            x=15, 
            y=650, 
            command=lambda :self.changestate(state.back))


        self.btnreset=TouchButton(
            self.root, 
            image=self.imgreset, 
            x=1040, 
            y=56.8, 
            command=self.reset)
        self.btnreset.place_forget()

        self.btnfull=TouchButton(
            self.root, 
            image=self.imgfull, 
            x=720, 
            y=56.8, 
            command=self.full)
        self.btnfull.place_forget()

        self.btntrack=TouchButton(
            self.root, 
            image=self.imgtrack, 
            x=1040, 
            y=234.8, 
            command=self.alttab)
        self.btntrack.place_forget()

        self.btnsensor=TouchButton(
            self.root,                                   
            image=self.imgsensor, 
            x=720, 
            y=234.8, 
            command=self.alttab)
        self.btnsensor.place_forget()

        self.btnshutter=TouchButton(
            self.root, 
            image=self.imgshutter, 
            x=1040, 
            y=410, 
            command=self.alttab)
        self.btnshutter.place_forget()

        self.btnup=TouchButton(
            self.root, 
            image=self.imgup, 
            x=845, 
            y=412.4, 
            command=lambda _:self.shutter(0))
        self.btnup.place_forget()

        self.btndown=TouchButton(
            self.root, 
            image=self.imgdown, 
            x=845, 
            y=473.4, 
            command=lambda _:self.shutter(1))
        self.btndown.place_forget()

        self.btnconfirm=TouchButton(
            self.root, 
            image=self.imgconfirm, 
            x=720, 
            y=412.4, 
            command=None)
        self.btnconfirm.place_forget()

        self.btnreject=TouchButton(
            self.root, 
            image=self.imgreject, 
            x=720, 
            y=590.2, 
            command=None)
        self.btnreject.place_forget()

        self.btnstop=TouchButton(
            self.root, 
            image=self.imgstop, 
            x=1040, 
            y=590.2, 
            command=None)
        self.btnstop.place_forget()

        self.btnexit=TouchButton(
            self.root, 
            image=self.imgexit, 
            x=15, 
            y=15, 
            command=self.buttonexit)

        self.btnconfirmexit=TouchButton(
            self.frmexit, 
            image=self.imgtik, 
            x=190, 
            y=141, 
            command=self.exit)

        self.btncancelexit=TouchButton(
            self.frmexit, 
            image=self.imgcross, 
            x=75, 
            y=141, 
            command=self.cancel)
          
        self.btnsetting=TouchButton(
            self.root, 
            image=self.imggear, 
            x=115, 
            y=15, 
            command=self.buttonsetting)

        self.btnconfirmsetting=TouchButton(
            self.frmsetting, 
            image=self.imgtik, 
            x=242.5, 
            y=261, 
            command=self.confirmsetting)

        self.btncancelsetting=TouchButton(
            self.frmsetting, 
            image=self.imgcross, 
            x=127.5, 
            y=261, 
            command=self.cancel)

        self.btnbrowse=TouchButton(
            self.frmsetting, 
            image=self.imgbrowse, 
            x=29, 
            y=51, 
            command=self.browse)
  


        self.btnselectcom=Menubutton(
            self.frmsetting,
            image=self.imgdrop1,
            borderwidth=0, 
            activebackground=self.clr, 
            background=self.clr)
        self.btnselectcom.pack()
        self.btnselectcom.place(x= 29, y=126)
        self.btnselectcom.bind(
            '<Button-1>',
            lambda _:(self.btnselectcom.place(x=31, y=128),
                      self.root.after(
                          100,
                          lambda :self.btnselectcom.place(x=29, y=126)
                          )
                      )   
            )
        self.menucom=Menu(self.btnselectcom, tearoff=0)
        self.menucom.add_command(
            label="     COM1    ",
            command=lambda :self.comselect(1),
            background=self.clr)
        self.menucom.add_command(
            label="     COM2    ", 
            command=lambda :self.comselect(2), 
            background=self.clr)
        self.btnselectcom.config(menu=self.menucom)

    def changestate(self, newstate, event=None):
        self.oldstate=self.state
        self.state=newstate
        if newstate == state.testmenu or newstate == state.usb or newstate == state.com:    
            self.testmode() 
        elif newstate == state.back:
                self.killkdiag()
                self.changestate(state.firstmenu)
        elif newstate == state.firstmenu and self.oldstate == state.back:
            self.buttonplace("firstmenu")

        elif newstate == state.reset:
            self.buttonstate(0)
        elif newstate == state.full:
            self.killkdiag()
            self.popupkdiag(2)
            self.root.after(2000,self.magnet)



            
            

    def magnet(self, event = None):
            self.kybrd.press(Key.down)
            self.kybrd.release(Key.down)
            self.kybrd.press('+')
            self.kybrd.release('+')
            for i in range(8):
                self.kybrd.press(Key.down)
                self.kybrd.release(Key.down)
            self.press_s()
              

            

    def press_s(self, event = None):
        self.kybrd.press('s')
        self.kybrd.release('s')
    
    def killkdiag(self, event=None):
            self.i = 0
            self.kdiagrun.kill()


        
    def testmenu(self, event = None):
        self.buttonplace()

   
    def firstmenu(self, event = None):
        self.btnusb.place()
        self.btncom.place()

    def browse(self, event=None):
        self.frmsetting.attributes("-topmost",False)
        self.newkdiag=filedialog.askopenfilename(
            title=("را انتخاب کنید KDIAG مسیر نرم افزار"),
            filetypes=[('exe Files','.exe'),("all files",'*')])
        self.entkdiag.delete(0, END)
        self.entkdiag.insert(0, self.newkdiag)
        self.frmsetting.attributes("-topmost",True)

    def exitframe(self):
        self.frmexit=Toplevel(self.root)
        self.lblexit=Label(self.frmexit)
        self.cnftoplevel(
            name=self.frmexit, 
            label=self.lblexit, 
            geometry="375x200+495+284", 
            image1=self.imgfrmexit1, 
            image2=self.imgfrmexit2, 
            alarm=1)
        
    def alarm(self,popup,alarmimage1,alarmimage2):
            if self.i == 1 :
                self.i=2
                popup.focus_force()
                popup.bell()
                popup.config(image=alarmimage2)
                self.root.after(
                    100,lambda : self.alarm(popup,alarmimage1,alarmimage2))
            else:
                popup.config(image=alarmimage1)
                self.i=1

    def buttonexit(self, event=None):
        self.buttonstate(0)
        self.frmexit.deiconify()

    def buttonsetting(self, event=None):   
        self.buttonstate(0)
        self.frmsetting.deiconify()

    def exit(self, event=None):
        try:
            self.kdiagrun.kill()
        except:
            pass
        self.root.after(200,lambda :os._exit(0))

    def cancel(self, event=None):
        self.buttonstate(1)
        self.frmexit.withdraw()
        self.frmsetting.withdraw()

    def buttonplace(self, i, event=None):
        if i == 1:
            self.btnusb.place_forget()
            self.btncom.place_forget()
        elif i == "firstmenu":
            self.btnreset.place_forget()
            self.btnfull.place_forget()
            self.btnshutter.place_forget()
            self.btnreject.place_forget()
            self.btntrack.place_forget()
            self.btnsensor.place_forget()
            self.btnstop.place_forget()
            self.entshutternumber.place_forget()
            self.btnup.place_forget()
            self.btndown.place_forget()
            self.btnconfirm.place_forget()
            self.btnusb.place()
            self.btncom.place()
            



    def buttonstate(self, i, event=None):
        if (i == 0):
            self.btncom.state(DISABLED)
            self.btnusb.state(DISABLED)
            self.btnexit.state(DISABLED)
            self.btnsetting.state(DISABLED)
            self.btnreset.state(DISABLED)
            self.btnfull.state(DISABLED)
            self.btnshutter.state(DISABLED)
            self.btnreject.state(DISABLED)
            self.btntrack.state(DISABLED)
            self.btnsensor.state(DISABLED)
            self.btnstop.state(DISABLED)
            self.entshutternumber.config(state=DISABLED)
            self.btnup.state(DISABLED)
            self.btndown.state(DISABLED)
            self.btnconfirm.state(DISABLED)
            if self.state == state.usb:
                self.btnselectcom.config(state=DISABLED)
                self.btnselectcom.unbind('<Button-1>')
                self.btnselectcom.unbind('<ButtonRelease-1>')
            else:
                self.btnselectcom.config(state=NORMAL)
                self.btnselectcom.bind(
                    '<Button-1>',
                    lambda _:(
                        self.btnselectcom.place(x=31, y=128),
                        self.root.after(
                            100,
                            lambda :self.btnselectcom.place(x=29, y=126)
                            )
                        )
                    )


        elif (i == 1):
            self.btncom.state(NORMAL)
            self.btnusb.state(NORMAL)
            self.btnexit.state(NORMAL)
            self.btnsetting.state(NORMAL)
            self.btncom.state(NORMAL)
            self.btnusb.state(NORMAL)
            self.btnexit.state(NORMAL)
            self.btnsetting.state(NORMAL)
            self.btnreset.state(NORMAL)
            self.btnfull.state(NORMAL)
            self.btnshutter.state(NORMAL)
            self.btnreject.state(NORMAL)
            self.btntrack.state(NORMAL)
            self.btnsensor.state(NORMAL)
            self.btnstop.state(NORMAL)
            self.entshutternumber.config(state=NORMAL)
            self.btnup.state(NORMAL)
            self.btndown.state(NORMAL)
            self.btnconfirm.state(NORMAL)





 




    def comselect(self, i, event=None):
        if i == 1:
            self.btnselectcom.config(image=self.imgdrop1)
            self.v2xbuff="COM1"   
        elif i == 2 :
            self.btnselectcom.config(image=self.imgdrop2)
            self.v2xbuff="COM2"   

    def confirmsetting(self, event=None):
        if not self.oldstate == state.firstmenu:
            self.kdiagrun.kill()
            self.popupkdiag(2)
        self.kdiag=self.entkdiag.get()
        try:
            self.v2x=self.v2xbuff
        except:
            pass
        self.kdiagaddress,self.v2x = self.CTRconfig(i=1)
        self.buttonstate(1)
        self.frmsetting.withdraw()



    def reset(self, event = None):
        self.killkdiag()
        self.popupkdiag(2)
        self.changestate(state.reset)
        self.sendcommand("reset")

    def full(self, event = None):
        self.changestate(state.full)
        self.root.after(3000,lambda : self.sendcommand("full"))



    def shutter(self, i, event=None):
        if i == 0 and self.shutternumber<25 :
            self.shutternumber += 1
        elif i == 1 and self.shutternumber > 1:
            self.shutternumber -= 1
        if self.shutternumber < 10 :
            self.entshutternumber.delete(0,END)
            self.entshutternumber.insert(0,("0"+str(self.shutternumber)))
        else:
            self.entshutternumber.delete(0,END)
            self.entshutternumber.insert(0,self.shutternumber)

    def alttab(self, event=None):
        self.kybrd.press(Key.alt)
        self.kybrd.press(Key.tab)
        self.kybrd.release(Key.tab)
        self.kybrd.release(Key.alt)

    def popupkdiag(self, i, event=None):
        if i == "USB":
            self.v2x="USB"
        elif i == "COM":
            try:
                self.v2x=self.v2xbuff
            except:
                self.v2x="COM1"
        self.kdiagaddress,self.v2x = self.CTRconfig(i=1)
        iniadrress=self.kdiagaddress+"/CHDV2X.INI"
        cnf=open(iniadrress,"r")
        txt=cnf.read().splitlines()
        txt[34]=txt[34][:(txt[34].find("=")+1)]+" "+self.v2x
        txt[12]="CHDV2X&Auto-FW-Info=32"
        for j in range (72):
            if j == 0:
                s=txt[j]
            else:
                s += "\n"+txt[j]
        txt=s
        cnf=open(iniadrress,"w")
        cnf.write(txt)
        cnf.close()
        self.changestate(state.testmenu)
        try:
            self.kdiagrun=subprocess.Popen(self.kdiag, shell=False)
            #self.root.after(200,self.alttab)
            if self.v2x == "USB":
                self.changestate(state.usb)
            else:
                self.changestate(state.com)
        except:
            self.browse()

    


    def testmode(self, event=None):

        self.btncom.place_forget()
        self.btnusb.place_forget()
        #self.root.after(1000,self.alttab)
        self.btnshutter.place()
        self.btnreset.place()
        self.btntrack.place()
        self.btnreject.place()
        self.btnup.place()
        self.btndown.place()
        self.btnfull.place()
        self.btnconfirm.place()
        self.btnsensor.place()
        self.btnstop.place()
        self.entshutternumber.place(x=918, y=415)
        self.buttonstate(1)





    def resource_path(self,relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path=sys._MEIPASS
        except Exception:
            base_path=os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def CTRconfig(self, 
                     path="C:/Users/"
                     +os.getlogin()+
                     "/AppData/Roaming/CTR", 
                     i=0, 
                     event=None):
        self.path=path 
        kdiagaddress=""
        kdiag=""
        v2x="USB"
        self.cnf=  path + "/cnf.ini"
        if i == 1:
            kdiag=self.kdiag
            v2x=self.v2x
            kdiagaddress=self.kdiagaddress
            f=open(self.cnf,"r")
            txt=f.read().splitlines()
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            try:
                f=open(self.cnf,"r")
            except:
                f=open(self.cnf,"w")
                f.write("This is CTR controller config file\nKDIAG Address         ="
                        +" C:/Users/\n[Interface]\nCHDV2X&Channel        ="
                        +" USB\nCHDV2X&Channel list  =CH05,CH08,USB\n"
                        +"CHDV2X&Baud          =38400\nCHDV2X&Baud list      ="+
                        " 19200,9600,38400\nCHDV2X&Handshake      ="
                        +" RTS/CTS\nCHDV2X&USB device number=0")
                f.close()
                f=open(self.cnf,"r")
            txt=f.read().splitlines()
            v2x=txt[3][txt[3].find("=")+1:]
            if ":/" in txt[1]:
                kdiag=txt[1][txt[1].find(":/")-1:]
                kdiagaddress=kdiag [:kdiag.find("/CHDV2X.exe")]
        if not os.path.isfile(kdiag):
            print("helloooooo")
            kdiag=filedialog.askopenfilename(
                title=("را انتخاب کنید KDIAG مسیر نرم افزار"),
                filetypes=[('exe Files','.exe'),("all files",'*')])
            kdiagaddress=kdiag [:kdiag.find("/CHDV2X.exe")]
        txt[1]="KDIAG Address         = "+kdiag
        txt[3]="CHDV2X&Channel        = "+v2x
        for j in range(8):
            if j == 0:
                s=txt[j]
            else:
                s += "\n"+txt[j]
        txt=s
        f=open(self.cnf,"w")
        f.write(txt)
        f.close()
        return kdiagaddress,v2x


    def sendcommand(self, cmnd, event = None):
        try:
            self.ser.open()
        except:
            pass
        if cmnd == "reset":
            self.ser.write("400".encode('utf-8'))
        elif cmnd == "clear":
            self.ser.write("100".encode('utf-8'))
        elif cmnd == "full":
            self.ser.write("103".encode('utf-8'))


    def readcommand(self, event = None):
            try:
                self.ser.open()
            except:
                pass
            cmnd = self.ser.read_until().decode('utf-8')
            self.ser.close()
            return cmnd

    def checkloop(self):
        while(1):
            self.cmdfromctr = self.readcommand()
            if "400" in self.cmdfromctr:
                self.sendcommand("clear")
            elif "000" in self.cmdfromctr:
                self.changestate(self.oldstate)

    def ontop(self, event = None):
        if self.state == state.usb or self.state == state.com:
            if self.i == 2:
                self.alttab()
            self.i = 2

    def MainLoop(self):
        self.root.mainloop()
#_____________________________________________________________________________________________________________________________________________



#_____________________________________________________________________________________________________________________________________________
def main():

    ctr=GUI()
    t1 = threading.Thread(target = ctr.checkloop)
    t1.start()
    ctr.MainLoop()
    

if __name__ == "__main__":main()   

