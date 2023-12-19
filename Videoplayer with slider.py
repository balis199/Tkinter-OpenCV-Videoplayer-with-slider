import cv2
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog

class videoplayerwithslider:
    def __init__(self):
        # Create main window, specify video size
        self.window = tk.Tk()  
        self.VideoWidth = 640
        self.VideoHeight = 360
        
        #Define variables
        self.value = tk.DoubleVar()
        self.play_state = False
        self.TotalFrames = 1
        self.cap = None
        
        #Configure window
        self.window.geometry(str(self.VideoWidth+20)+"x"+str(self.VideoHeight+60))
        self.window.wm_title("Video Player")
        self.window.config(background="#FFFFFF")
        
        #Create 'open file' menu 
        main_menu = tk.Menu(master=self.window)
        new_item = tk.Menu(main_menu, tearoff=0)
        new_item.add_command(label="open file", command=self.Open_file)
        main_menu.add_cascade(label="File", menu=new_item)
        self.window.config(menu=main_menu)
        
        #Make Frame for Video
        self.imageFrame = tk.Frame(self.window, width=self.VideoWidth, height=self.VideoHeight)
        self.imageFrame.grid(row=0, column=0, padx=10, pady=2)
             
        #Put label into videoframe
        self.lmain = tk.Label(self.imageFrame)
        self.lmain.grid(row=0, column=0)

        #Create video slider
        self.sliderFrame = tk.Frame(self.window, width=self.VideoWidth, height=60)
        self.VideoSlider = tk.Scale(self.sliderFrame, from_=0, to=self.TotalFrames,  orient=tk.HORIZONTAL, length=self.VideoWidth-100, variable = self.value, command= self.slideshow_frame) 
        self.VideoSlider.grid(row=0, column = 1, sticky = tk.W)
        #Add play button next to slider
        self.Playbutton = tk.Button(self.sliderFrame, text="Play", command = self.Playbutton, height = 2)
        self.Playbutton.grid(row=0, column = 0, sticky = tk.W)
        self.sliderFrame.grid(row = 1, column=0, padx=10, pady=2)
        
        
        self.window.mainloop()
        
    def show_frame(self):
        '''
        Show video frame:
        Read Frame
        Resize Frame to specified size
        Process frame into tkinter label
        Assign new frame value to slider
        If 'play' is on: Repeat
        '''
        _, frame = self.cap.read()
        resize = cv2.resize(frame, (self.VideoWidth, self.VideoHeight)) 
        cv2image = cv2.cvtColor(resize, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.value.set(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        if self.play_state is True:
            self.lmain.after(1, self.show_frame) #Change '1' to alter playback speed
                

    def slideshow_frame(self, FrameNumber):
        '''
        Shows frame from slider:
        Set Cap position to Framenumber (slider output)
        Retrieve frame
        Resize frame to specified size
        Process frame into tkinter label
        '''
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(FrameNumber))
        _, frame = self.cap.retrieve()
        resize = cv2.resize(frame, (self.VideoWidth, self.VideoHeight)) 
        cv2image = cv2.cvtColor(resize, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        
        
    def Playbutton(self):
        '''
        When play button is pressed:
        If there is a video change play state (True -> False or False -> True)
        '''
        if self.cap is not None:
            self.play_state = not self.play_state
            self.show_frame()
        else:
            tk.messagebox.showerror('Python Error', 'Error: No file selected')
                
    
    def Open_file(self):
        ''' 
        Used in menu: Dialog to select file and create file path, 
        also configures Slider max, and shows first frame of video
        '''
        #get folder location from user
        self.file_path = filedialog.askopenfilename(title="Select A video", filetypes=(("mp4 files", "*.mp4"), ("mkv files", "*.mkv*"), ("avi files", "*.avi")))
        self.cap = cv2.VideoCapture(self.file_path)
        self.TotalFrames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.VideoSlider.configure(from_=0, to=self.TotalFrames)
        self.show_frame()

videoplayerwithslider()  #Starts GUI