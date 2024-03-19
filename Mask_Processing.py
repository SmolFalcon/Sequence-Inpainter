import cv2
import os
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk

class GUI():
    def __init__(self):
        self.InDir = ""
        self.InDirList = []
        self.TWMaskedDir = ""
        self.TWMaskedDirList = []
        self.TWOccluderDir = ""
        self.TWOccluderDirList = []
        self.OutDir = ""
        self.ListIndx = 0
        
        self.window = Tk()
        self.window.resizable(width=False, height=False)
        self.window['background']='#3D3D3D'
        
        self.Bprompt_Input = StringVar()
        self.Bprompt_TWMasked = StringVar()
        self.Bprompt_TWOccluder = StringVar()
        self.Bprompt_Output = StringVar()
        
        self.window.title("TheWeapon Mask Processing")  
        
        self.CanvasH = 0
        self.CanvasW = 400
        
            
        Label(text = "Feather AOV", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 0,column=0)     
        self.Bprompt_Input.set("Select Feather AOV")
        
        Input_Button = Button(textvariable = self.Bprompt_Input, width = 70, command = self.GUI_LoadInput, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        Input_Button.grid(row = 1,column=0, sticky = S)#place in grid   
        
        #Canvas to display a preview of the selected image
        self.Canvas_Input = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.Input_Preview = PhotoImage(file=self.InDir)
        self.Preview_Canvas_1 = self.Canvas_Input.create_image(0, 0, anchor = NW, image = self.Input_Preview)
        self.Canvas_Input.grid(row = 2,column=0)
    
        
        
        
                
        Label(text = "TWMasked", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 3,column=0,sticky = S)
        self.Bprompt_TWMasked.set("Select TWMasked")
        
        TWMasked_Button = Button(textvariable = self.Bprompt_TWMasked, width = 70, command = self.GUI_LoadTWMasked, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        TWMasked_Button.grid(row = 4,column=0,sticky = N)

        #Canvas to display a preview of the selected image
        self.Canvas_TWMasked = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.TWMasked_Preview = PhotoImage(file=self.TWMaskedDir)
        self.Preview_Canvas_2 = self.Canvas_TWMasked.create_image(0, 0, anchor = NW, image = self.TWMasked_Preview)
        self.Canvas_TWMasked.grid(row = 5,column=0,rowspan = 2)
        
        
        
        
        Label(text = "TWOccluder", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 7,column=0,sticky = S)
        self.Bprompt_TWOccluder.set("Select TWOccluder")
        
        TWOccluder_Button = Button(textvariable = self.Bprompt_TWOccluder, width = 70, command = self.GUI_LoadTWOccluder, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        TWOccluder_Button.grid(row = 8,column=0,sticky = N)

        #Canvas to display a preview of the selected image
        self.Canvas_TWOccluder = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.TWOccluder_Preview = PhotoImage(file=self.TWOccluderDir)
        self.Preview_Canvas_2 = self.Canvas_TWOccluder.create_image(0, 0, anchor = NW, image = self.TWOccluder_Preview)
        self.Canvas_TWOccluder.grid(row = 9,column=0,rowspan = 2)
        
        
        
        
        
        Label(text = "Output Directory", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 0,column=1)
        self.Bprompt_Output.set("Select output directory")
        
        Output_Button = Button(textvariable = self.Bprompt_Output, width = 70, command = self.GUI_LoadOutput, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        Output_Button.grid(row = 1,column=1)
        
        #Canvas to display a preview of the selected image
        self.Canvas_Output = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.Output_Preview = PhotoImage(file=self.OutDir)
        self.Preview_Canvas_3 = self.Canvas_Output.create_image(0, 0, anchor = NW, image = self.Output_Preview)
        self.Canvas_Output.grid(row = 2,column=1)

    
    
        Execute_Button = Button(text = "Process Current", width = 30,height = 1, command = self.CallProcess, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e',font=("Orbitron", 13))
        Execute_Button.grid(row = 4,column=1,sticky = N)
        
        Execute_Button = Button(text = "Process Sequence",width = 30,height = 1, command = self.ProcessSequence, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e',font=("Orbitron", 13))
        Execute_Button.grid(row = 5,column=1,sticky = N)
        
        self.OutText = Text(width = 45, height = 10, bg = '#313131', fg='#d6d6d6',state = NORMAL)
        
        
        Label(text = "Occluder Erosion-Dilation", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 10)).grid(row = 7,column=1,sticky = N)
        var = StringVar()
        self.spin_DilateErode = Spinbox(from_= -100, to=100, textvariable=var, bg='#4f4f4f', fg='#d6d6d6')
        var.set(0)
        self.spin_DilateErode.grid(row = 7,column=1,sticky = NE)


        Label(text = "Mask Dilation", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 10)).grid(row = 8,column=1,sticky = N)
        self.spin_DilateIter = Spinbox(from_= 0, to=100, bg='#4f4f4f', fg='#d6d6d6')
        self.spin_DilateIter.grid(row = 8,column=1,sticky = NE)
        
        
        
        
        for i in range(10):
            self.OutText.insert(INSERT,"\n") #Insert a linebreak to fill the text box
        
        self.OutText.replace('1.0','2.0', "No Feather AOVs loaded\n")
        self.OutText.replace('3.0','4.0', "No TWMasked loaded\n")
        self.OutText.replace('5.0','6.0', "No TWOccluder loaded\n")
        self.OutText.replace('7.0','8.0', "No Output directory set\n")
        
        self.OutText.config(state = DISABLED)
        self.OutText.grid(row = 6, column=1, sticky = N)
    
    
    
    
    
        self.window.mainloop()
        
        
        
        
    def ProcessMask(self, InDir, TWMaskedDir, TWOccluderDir, OutDir):
        kernel = np.ones((3, 3), 'uint8')
        AOV = cv2.imread(InDir)
        TWMasked = cv2.imread(TWMaskedDir)
        TWOccluder = cv2.imread(TWOccluderDir)
        Stray = cv2.imread(InDir)#Image to store stray feathers mask
        
        if int(self.spin_DilateErode.get()) < 0: #dilate or erode occluder mask
            TWOccluder = cv2.erode(TWOccluder, kernel, iterations = abs(int(self.spin_DilateErode.get())))
        else:
            TWOccluder = cv2.dilate(TWOccluder, kernel, iterations = int(self.spin_DilateErode.get()))
        
        cv2.subtract(TWMasked, TWOccluder, TWMasked) #Subtract cloth from body mask
              
        cv2.bitwise_and(AOV, TWOccluder, AOV) #Get intersection between feathers and Cloth
        
        cv2.subtract(AOV, TWMasked, AOV) #Subtract body mask
        
        AOV = cv2.dilate(AOV, kernel, iterations = int(self.spin_DilateIter.get())) #Dilate feather mask
        
        #Get stray feathers (feathers separated from the body and not intersecting cloth)
        cv2.subtract(Stray, TWMasked, Stray)
        cv2.subtract(Stray, TWOccluder, Stray)
        
        Stray = cv2.dilate(Stray, kernel, iterations = int(self.spin_DilateIter.get())) #dilate stray feathers mask
        
        cv2.add(AOV, Stray,AOV) #combine masks
        
        cv2.imwrite(OutDir, AOV)
        
    
        
    def ProcessSequence(self):
        if not self.Check_Ready():
            self.Show_Error("Not all parameters have been set")
            return
        
        if len(self.InDirList) == 1 and len(self.TWMaskedDirList) == 1: #There is only one file of each, no need for sequence
            self.Show_Error("Only 1 Input and TWMasked loaded")
            
        else:
            if len(self.InDirList) == len(self.TWMaskedDirList) and len(self.InDirList) == len(self.TWOccluderDirList) : #check there is the same quantity of Inputs and TWMaskeds
            
                for i in range(len(self.InDirList)):
                    self.window.update() #Update window each iteration
                    self.GUI_LoadInput(True)
                    self.GUI_LoadTWMasked(True)
                    self.GUI_LoadTWOccluder(True)
                    self.CallProcess()
                    
                    if self.ListIndx+1 < len(self.InDirList): #Update Input and TWMasked for every image in the list       
                        self.ListIndx = self.ListIndx + 1
                        
                self.ListIndx = 0
               
            else:
                self.Show_Error("Image quantity does not match")
        
    def CallProcess(self, Update = False):
        
        if not self.Check_Ready():
            self.Show_Error("Not all parameters have been set")
            return
        else:
            self.Show_Error("")
    
        if len(self.InDirList) != len(self.TWMaskedDirList):
            self.Show_Error("Input and TWMasked quantity does not match")
            
        else:
            self.ProcessMask(self.InDir, self.TWMaskedDir, self.TWOccluderDir, self.OutDir)
            
            self.Show_State("Completed: " + os.path.basename(self.InDir))
            
            #Set image to preview zone
            TempImg = Image.open(self.OutDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.Output_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_Output.itemconfig(self.Preview_Canvas_3, image = self.Output_Preview)
            self.Canvas_Output.config(width = self.Output_Preview.width(), height = self.Output_Preview.height()) #resize canvas to fit image
        
        
    def GUI_LoadInput(self, Update = False):
        if not Update:
            self.InDirList = list(fd.askopenfilenames())
            self.Check_Ready()
            self.ListIndx = 0 #Reset sequence list index when opening new batch

        self.InDir = self.InDirList[self.ListIndx]
        
        self.GUI_LoadOutput(True)#update Output file name
        
        if self.InDir != "":
            self.Bprompt_Input.set(self.InDir)
            
            self.OutText.config(state = NORMAL)
            self.OutText.replace('1.0','2.0', "Loaded "+str(len(self.InDirList))+ " Feather AOVs\n")
            self.OutText.config(state = DISABLED)
            
            #Set image to preview zone
            TempImg = Image.open(self.InDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.Input_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_Input.itemconfig(self.Preview_Canvas_1, image = self.Input_Preview)
            self.Canvas_Input.config(width = self.Input_Preview.width(), height = self.Input_Preview.height()) #resize canvas to fit image
            
    def GUI_LoadTWMasked(self, Update = False):
        if not Update:
            self.TWMaskedDirList = list(fd.askopenfilenames())
            self.Check_Ready()
            self.ListIndx = 0 #Reset sequence list index when opening new batch
            
        self.TWMaskedDir = self.TWMaskedDirList[self.ListIndx]
        
        if self.TWMaskedDir != "":
            self.Bprompt_TWMasked.set(self.TWMaskedDir)
            
            self.OutText.config(state = NORMAL)
            self.OutText.replace('3.0','4.0', "Loaded "+str(len(self.TWMaskedDirList))+ " TWMasked\n")
            self.OutText.config(state = DISABLED)
            
            #Set image to preview zone
            TempImg = Image.open(self.TWMaskedDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.TWMasked_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_TWMasked.itemconfig(self.Preview_Canvas_2, image = self.TWMasked_Preview)
            self.Canvas_TWMasked.config(width = self.TWMasked_Preview.width(), height = self.TWMasked_Preview.height()) #resize canvas to fit image
            
            
    def GUI_LoadTWOccluder(self, Update = False):
        if not Update:
            self.TWOccluderDirList = list(fd.askopenfilenames())
            self.Check_Ready()
            self.ListIndx = 0 #Reset sequence list index when opening new batch
            
        self.TWOccluderDir = self.TWOccluderDirList[self.ListIndx]
        
        if self.TWOccluderDir != "":
            self.Bprompt_TWOccluder.set(self.TWOccluderDir)
            
            self.OutText.config(state = NORMAL)
            self.OutText.replace('5.0','6.0', "Loaded "+str(len(self.TWOccluderDirList))+ " TWOccluder\n")
            self.OutText.config(state = DISABLED)
            
            #Set image to preview zone
            TempImg = Image.open(self.TWOccluderDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.TWOccluder_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_TWOccluder.itemconfig(self.Preview_Canvas_2, image = self.TWOccluder_Preview)
            self.Canvas_TWOccluder.config(width = self.TWOccluder_Preview.width(), height = self.TWOccluder_Preview.height()) #resize canvas to fit image
            
            
    def GUI_LoadOutput(self, Update = False):
        SplitDir = os.path.splitext(os.path.basename(self.InDir)) #Get original image name and extension
        NewFilename = SplitDir[0]+str("_Corrected")
        Extension = SplitDir[1]
        
        if not Update:
            self.OutDir = fd.askdirectory()
            self.Check_Ready()
            
        else:
            self.OutDir = os.path.dirname(self.OutDir)
            
        if self.OutDir != "":
            self.OutText.config(state = NORMAL)
            self.OutText.replace('7.0','8.0', "Output directory has been set\n")
            self.OutText.config(state = DISABLED)
            
            self.OutDir = self.OutDir+str("/")+NewFilename+Extension
            self.Bprompt_Output.set(self.OutDir)
            
    def Show_Error(self, Msg):
        self.OutText.config(state = NORMAL)
        self.OutText.replace('7.0','8.0', Msg+"\n")
        self.OutText.config(state = DISABLED)
        
    def Show_State(self, Msg):
        self.OutText.config(state = NORMAL)
        self.OutText.replace('9.0','10.0', Msg+"\n")
        self.OutText.config(state = DISABLED)
        
    def Check_Ready(self):
        if self.InDir != "" and self.TWMaskedDir != "" and self.TWOccluderDir != "" and self.OutDir != "":
            self.Show_Error("")
            return True
        else:
            return False
        
        
        
    def GetInDir(self):
        return self.InDir
    def GetTWMaskedDir(self):
        return self.TWMaskedDir
    def GetOutDir(self):
        return self.OutDir
    
def StartGUI():    
    window = GUI()




