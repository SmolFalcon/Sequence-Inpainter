import cv2
import os
import time
import numpy as np
import argparse
import torch.cuda
from lama_cleaner.lama import LaMa
import Mask_Processing
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk

def norm_img(np_img):
    if len(np_img.shape) == 2:
        np_img = np_img[:, :, np.newaxis]
    np_img = np.transpose(np_img, (2, 0, 1))
    np_img = np_img.astype("float32") / 255
    return np_img

def resize_max_size(
    np_img, size_limit: int, interpolation=cv2.INTER_CUBIC
) -> np.ndarray:
    # Resize image's longer size to size_limit if longer size larger than size_limit
    h, w = np_img.shape[:2]
    if max(h, w) > size_limit:
        ratio = size_limit / max(h, w)
        new_w = int(w * ratio + 0.5)
        new_h = int(h * ratio + 0.5)
        return cv2.resize(np_img, dsize=(new_w, new_h), interpolation=interpolation)
    else:
        return np_img

def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8080, type=int)
    parser.add_argument("--model", default="lama", choices=["lama", "ldm"])
    parser.add_argument(
        "--ldm-steps",
        default=50,
        type=int,
        help="Steps for DDIM sampling process."
        "The larger the value, the better the result, but it will be more time-consuming",
    )
    parser.add_argument("--device", default="cuda", type=str)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()

def Inpaint(pInput, pMask, pOutput): #Inpaints image using paths to Input, Mask and Output
    global model
    global device
    args = get_args_parser()
    device = torch.device(args.device)
    model = LaMa(device)

    image = cv2.cvtColor(cv2.imread(pInput), cv2.COLOR_BGR2RGB) #Convert from BGR to RGB
            
    mask = cv2.imread(pMask,cv2.IMREAD_GRAYSCALE)
       
    interpolation = cv2.INTER_CUBIC
    size_limit = max(image.shape)
    
    image = resize_max_size(image, size_limit=size_limit, interpolation=interpolation)
    image = norm_img(image)
    
    mask = resize_max_size(mask, size_limit=size_limit, interpolation=interpolation)
    mask = norm_img(mask)
    
    start = time.time()
    res_np_img = model(image, mask)
    
    torch.cuda.empty_cache()
    
    cv2.imwrite(pOutput, res_np_img) 

    return time.time()-start
    
#def SetMask(pDir):
    
#def SetOutput(pDir):


In = "D:/Desktop/lama-cleaner/Test_Img/IMG.png"   
Mask = "D:/Desktop/lama-cleaner/Test_Img/MASK.png"
Out = "D:/Desktop/lama-cleaner/Test_Img/RES.png"
#Inpaint(In,Mask,Out)


class GUI:
    def __init__(self):
        self.InDir = ""
        self.InDirList = []
        self.MaskDir = ""
        self.MaskDirList = []
        self.OutDir = ""
        self.ListIndx = 0
        
        self.window = Tk()
        self.window.resizable(width=False, height=False)
        self.window['background']='#3D3D3D'
        
        self.Bprompt_Input = StringVar()
        self.Bprompt_Mask = StringVar()
        self.Bprompt_Output = StringVar()
        
        self.window.title("Project Boastful")  
        
        self.CanvasH = 0
        self.CanvasW = 400
        
            
        Label(text = "Input Image", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 0,column=0)     
        self.Bprompt_Input.set("Select Image")
        
        Input_Button = Button(textvariable = self.Bprompt_Input, width = 70, command = self.GUI_LoadInput, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        Input_Button.grid(row = 1,column=0, sticky = S)#place in grid   
        
        #Canvas to display a preview of the selected image
        self.Canvas_Input = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.Input_Preview = PhotoImage(file=self.InDir)
        self.Preview_Canvas_1 = self.Canvas_Input.create_image(0, 0, anchor = NW, image = self.Input_Preview)
        self.Canvas_Input.grid(row = 2,column=0)
    
        
        
        
                
        Label(text = "Mask", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 3,column=0,sticky = S)
        self.Bprompt_Mask.set("Select Mask")
        
        Mask_Button = Button(textvariable = self.Bprompt_Mask, width = 70, command = self.GUI_LoadMask, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        Mask_Button.grid(row = 4,column=0,sticky = N)

        #Canvas to display a preview of the selected image
        self.Canvas_Mask = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.Mask_Preview = PhotoImage(file=self.MaskDir)
        self.Preview_Canvas_2 = self.Canvas_Mask.create_image(0, 0, anchor = NW, image = self.Mask_Preview)
        self.Canvas_Mask.grid(row = 5,column=0,rowspan = 2)
        
        
        
        
        
        Label(text = "Output Directory", bg='#3D3D3D', fg='#d6d6d6', font=("Orbitron", 15)).grid(row = 0,column=1)
        self.Bprompt_Output.set("Select output directory")
        
        Output_Button = Button(textvariable = self.Bprompt_Output, width = 70, command = self.GUI_LoadOutput, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e')
        Output_Button.grid(row = 1,column=1)
        
        #Canvas to display a preview of the selected image
        self.Canvas_Output = Canvas(width = self.CanvasW, height = self.CanvasH, bg = '#3D3D3D', highlightbackground = '#3D3D3D')
        self.Output_Preview = PhotoImage(file=self.OutDir)
        self.Preview_Canvas_3 = self.Canvas_Output.create_image(0, 0, anchor = NW, image = self.Output_Preview)
        self.Canvas_Output.grid(row = 2,column=1)

    
    
        Execute_Button = Button(text = "Inpaint Current", width = 30,height = 1, command = self.CallInpaint, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e',font=("Orbitron", 13))
        Execute_Button.grid(row = 4,column=1,sticky = N)
        
        Execute_Button = Button(text = "Inpaint Sequence",width = 30,height = 1, command = self.InpaintSequence, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e',font=("Orbitron", 13))
        Execute_Button.grid(row = 5,column=1,sticky = N)

        Execute_Button = Button(text = "TW Mask Processor",width = 30,height = 1, command = self.MaskProcessor, bg='#4f4f4f', fg='#d6d6d6', activeforeground='#d6d6d6', activebackground='#2e2e2e',font=("Orbitron", 13))
        Execute_Button.grid(row = 7,column=1,sticky = N)        
        
        self.OutText = Text(width = 45, height = 10, bg = '#313131', fg='#d6d6d6',state = NORMAL)
        
        for i in range(10):
            self.OutText.insert(INSERT,"\n") #Insert a linebreak to fill the text box
        
        self.OutText.replace('1.0','2.0', "No Input images loaded\n")
        self.OutText.replace('3.0','4.0', "No Masks loaded\n")
        self.OutText.replace('5.0','6.0', "No Output directory set\n")
        
        self.OutText.config(state = DISABLED)
        self.OutText.grid(row = 6, column=1, sticky = N)
    
    
    
    
    
        self.window.mainloop()
    def MaskProcessor(self):
        self.window.destroy()
        Mask_Processing.StartGUI()
        GUI()
        
    def InpaintSequence(self):
        if not self.Check_Ready():
            self.Show_Error("Not all parameters have been set")
            return
        
        if len(self.InDirList) == 1 and len(self.MaskDirList) == 1: #There is only one file of each, no need for sequence
            self.Show_Error("Only 1 Input and Mask loaded")
            
        else:
            if len(self.InDirList) == len(self.MaskDirList): #check there is the same quantity of Inputs and Masks
            
                for i in range(len(self.InDirList)):
                    self.window.update() #Update window each iteration
                    self.GUI_LoadInput(True)
                    self.GUI_LoadMask(True)
                    self.CallInpaint()
                    
                    if self.ListIndx+1 < len(self.InDirList): #Update Input and Mask for every image in the list       
                        self.ListIndx = self.ListIndx + 1
                        
                self.ListIndx = 0
               
            else:
                self.Show_Error("Input and Mask quantity does not match")
        
    def CallInpaint(self, Update = False):
        
        if not self.Check_Ready():
            self.Show_Error("Not all parameters have been set")
            return
        else:
            self.Show_Error("")
    
        if len(self.InDirList) != len(self.MaskDirList):
            self.Show_Error("Input and Mask quantity does not match")
            
        else:
            ProcessTime = Inpaint(self.InDir, self.MaskDir, self.OutDir)
            
            self.Show_State("Completed "+str(self.ListIndx+1)+" of "+str(len(self.InDirList))+" in " + str(round(ProcessTime,2)) +"s\n" + os.path.basename(self.InDir))
            
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
            self.OutText.replace('1.0','2.0', "Loaded "+str(len(self.InDirList))+ " Input images\n")
            self.OutText.config(state = DISABLED)
            
            #Set image to preview zone
            TempImg = Image.open(self.InDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.Input_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_Input.itemconfig(self.Preview_Canvas_1, image = self.Input_Preview)
            self.Canvas_Input.config(width = self.Input_Preview.width(), height = self.Input_Preview.height()) #resize canvas to fit image
            
    def GUI_LoadMask(self, Update = False):
        if not Update:
            self.MaskDirList = list(fd.askopenfilenames())
            self.Check_Ready()
            self.ListIndx = 0 #Reset sequence list index when opening new batch
            
        self.MaskDir = self.MaskDirList[self.ListIndx]
        
        if self.MaskDir != "":
            self.Bprompt_Mask.set(self.MaskDir)
            
            self.OutText.config(state = NORMAL)
            self.OutText.replace('3.0','4.0', "Loaded "+str(len(self.MaskDirList))+ " Masks\n")
            self.OutText.config(state = DISABLED)
            
            #Set image to preview zone
            TempImg = Image.open(self.MaskDir) #Use PIL to open image because gives less errors than native tkinter
            TempImg.thumbnail((self.CanvasW, self.CanvasW)) #resize image as thumbnail
            self.Mask_Preview = ImageTk.PhotoImage(TempImg)
            self.Canvas_Mask.itemconfig(self.Preview_Canvas_2, image = self.Mask_Preview)
            self.Canvas_Mask.config(width = self.Mask_Preview.width(), height = self.Mask_Preview.height()) #resize canvas to fit image
            
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
            self.OutText.replace('5.0','6.0', "Output directory has been set\n")
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
        if self.InDir != "" and self.MaskDir != "" and self.OutDir != "":
            self.Show_Error("")
            return True
        else:
            return False
        
        
        
    def GetInDir(self):
        return self.InDir
    def GetMaskDir(self):
        return self.MaskDir
    def GetOutDir(self):
        return self.OutDir
        
Interface = GUI()





