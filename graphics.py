
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

class GraphWindow(tk.Tk):
    def __init__(self):
        super().__init__() 
        
        self.canvasWidth = 1300
        self.canvasHeight = int(self.canvasWidth/2) + 80
        
        self.canvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight, bg='blue')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_image)
            
        self.commitButton = tk.Button(
            self.canvas,
            text="Commit?",
            width=13,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.commit
        )
        
        self.notCommitButton = tk.Button(
            self.canvas,
            text="Don't commit",
            width=13,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.notCommit
        ) 

        self.genButton = tk.Button(
            self,
            text="Scatter",
            width=15,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.imageGen
        ) 

        self.resetButton = tk.Button(
            self,
            text="Blank 1",
            width=15,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.imageReset
        ) 
        
        self.colourButton = tk.Button(
            self,
            text="Blank 2",
            width=15,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.imageColour
        ) 

        self.exportButton = tk.Button(
            self,
            text="Blank 3",
            width=15,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.exportPrep
        ) 
 

        self.removeButton = tk.Button(
            self.canvas,
            text="Remove",
            width=13,
            height=3,
            bd = '5',
            bg="blue",
            fg="yellow",
            #command = self.remove
        ) 

        self.labInput = tk.StringVar(

        )

        self.executionTimeLabel = tk.Label(
            self,
            text="Execution time not available",
            width=15,
            height=3,
            wraplength=100, justify="center",
            bd = '5'
        ) 
        
        self.labelInput = tk.Entry (
            self.canvas,
            textvariable = self.labInput,
            width = 16
            
        )

        self.inputButton = tk.Button(
            self.canvas,
            text="Check Label",
            #command = self.textInput
        ) 

        self.removeLabelsButton = tk.Button(
            self.canvas,
            text="Remove labels",
            width=12,
            height=2,
            bd = '4',
            bg="blue",
            fg="yellow",
            #command = self.removeLabel
        ) 

        self.allLabButton = tk.Button(
            self.canvas,
            text="All Labels",
            width=12,
            height=2,
            bd = '4',
            bg="blue",
            fg="yellow",
            #command = self.allLabels
        ) 
        
        self.hover_window = tk.Label(
            self.canvas, 
            width=8, 
            height=2, 
            background="grey", 
            fg="white")
        
        self.label_file_explorer = tk.Text(self,
                                    width = 30, height = 1)
              
        self.button_explore = tk.Button(self,
                                text = "Submit Player",
                                #command = self.browseFiles
                                )
        
        # self.labelInput.bind("<1>", self.clickedLabel)
        # self.labelInput.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.inputButton.bind("<1>", self.clickedLabel)
        # self.inputButton.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.removeLabelsButton.bind("<1>", self.clickedLabel)
        # self.removeLabelsButton.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.executionTimeLabel.bind("<1>", self.clickedLabel)
        # self.executionTimeLabel.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.allLabButton.bind("<1>", self.clickedLabel)
        # self.allLabButton.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.colourButton.bind("<1>", self.clickedLabel)
        # self.colourButton.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.commitButton.bind("<1>", self.clickedLabel)
        # self.commitButton.bind("<ButtonRelease-1>", self.unclickedLabel)
        
        # self.notCommitButton.bind("<1>", self.clickedLabel)
        # self.notCommitButton.bind("<ButtonRelease-1>", self.unclickedLabel)
        
        # self.removeButton.bind("<1>", self.clickedLabel)
        # self.removeButton.bind("<ButtonRelease-1>", self.unclickedLabel)

        # self.exportButton.bind("<1>", self.clickedLabel)
        # self.exportButton.bind("<ButtonRelease-1>", self.unclickedLabel)


        self.executionTime_window = self.canvas.create_window(self.canvasWidth,self.canvasHeight-10, anchor='se', window=self.executionTimeLabel)
        self.export_window = self.canvas.create_window(self.canvasWidth - 120,int(self.canvasHeight * 755/765), anchor='se', window=self.exportButton)

        self.gen_window = self.canvas.create_window(int(10*self.canvasWidth/1300),int(self.canvasHeight * 755/765), anchor='sw', window=self.genButton)
        self.reset_window = self.canvas.create_window(int(210*self.canvasWidth/1300),int(self.canvasHeight * 755/765), anchor='sw', window=self.resetButton)
        self.colour_window = self.canvas.create_window(int(410*self.canvasWidth/1300),int(self.canvasHeight * 755/765), anchor='sw', window=self.colourButton)
        
        self.label_file_explore_window = self.canvas.create_window(int(410*self.canvasWidth/1300),int(self.canvasHeight * 755/765), anchor='sw', window=self.label_file_explorer)
        self.button_explore_window = self.canvas.create_window(int(700*self.canvasWidth/1300),int(self.canvasHeight * 755/765), anchor='sw', window=self.button_explore)
    
    
    def resize_image(self, e):
        print("Running resize_image")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.zoom_factor = 1
        self.centre_displace = (0,0)
        # open image to resize it
        #image = Image.fromarray(self.img_display)
        # resize the image with width and height of root
        self.canvasHeight = e.height - 80
        self.canvasWidth = e.width
        if self.canvasHeight/self.canvasWidth < 0.5:
            imageHeight = self.canvasHeight
            self.canvasWidth = 2 * imageHeight
        else:
            self.canvasWidth = self.canvasWidth
            imageHeight = int(0.5 * self.canvasWidth)
            
        #canvas.config(width=self.canvasWidth, height=self.canvasHeight)
        #canvas.pack(fill="both", expand=True, anchor='nw'):
        
        executionTime_window = self.canvas.create_window(self.canvasWidth,e.height - 12, anchor='se', window=self.executionTimeLabel)
        self.export_window = self.canvas.create_window(self.canvasWidth - 120,e.height - 10, anchor='se', window=self.exportButton)
        
        gen_window = self.canvas.create_window(10,e.height - 10, anchor='sw', window=self.genButton)
        reset_window = self.canvas.create_window(140,e.height - 10, anchor='sw', window=self.resetButton)
        colour_window = self.canvas.create_window(270,e.height - 10, anchor='sw', window=self.colourButton)
        
        if self.labelButtonsActive:
            self.allLab_window = self.canvas.create_window(0.5*self.canvasWidth - 130 ,e.height-10, anchor='sw', window=self.allLabButton)
            self.labelInput_window = self.canvas.create_window(self.canvasWidth - 506, e.height - 46, anchor='se', window=self.labelInput)
            self.inputButton_window = self.canvas.create_window(self.canvasWidth - 420,e.height - 46, anchor='se', window=self.inputButton)
        
        label_file_explore_window = self.canvas.create_window(self.canvasWidth - 250,e.height - 11, anchor='se', window=self.label_file_explorer)
        button_explore_window = self.canvas.create_window(self.canvasWidth - 250,e.height - 46, anchor='se', window=self.button_explore)


        #if self.labelButtonsActive:
        #    self.allLabButton.place(x=550, y=e.height - 10, anchor='sw')
        #    """ labelInput.place(x=610 * self.canvasWidth/1300, y=self.canvasHeight * 705/765, anchor='sw') """
        #    """ inputButton.place(x=610 * self.canvasWidth/1300,y=self.canvasHeight * 755/765, anchor='sw')  """
        ########################################################################################################################CHECK LABEL DISPLAY ISSUES############################################################################################################################
        if self.labelledStatus:
            try:

                for l, label in enumerate(self.labelsImg):
                    #print("Labnum = ",l)
                    if self.canvasHeight/self.canvasWidth >= 0.5:
                        label.place(x=int(self.segmentData[l, 1]* self.canvasWidth/2048), y= int(0.5*(self.canvasHeight - 0.5*self.canvasWidth) + (self.segmentData[l,0]* self.canvasWidth/2048)), anchor="center")
                        #label.config(width=10 * self.canvasWidth/1300, height=10 * self.canvasWidth/1300)
                    else:
                        label.place(x=int(0.5*(self.canvasWidth - self.canvasWidth) +(self.segmentData[l,1]* self.canvasWidth/2048)), y= int(self.segmentData[l,0]* self.canvasWidth/2048), anchor="center")
                        #label.config(width=10 * self.canvasWidth/1300, height=10 * self.canvasWidth/1300)

            except:
                pass
        
        self.displayImage(self.img_display)
        """ image = image.resize((self.canvasWidth, int(self.canvasWidth/2)), Image.LANCZOS)
        self.imgtk = ImageTk.PhotoImage(image=image)
        img_id = self.canvas.create_image(self.canvasWidth/2,self.canvasHeight/2,image=self.imgtk) """
        #canvas.itemconfig(img_id, offset=(im),image=self.imgtk, anchor='nw')
        #canvas.pack(fill="both", expand=True)

    def zoom_image(self, e):
        print("Running resize_image")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        zoomFactor = 1.25**(e.delta/120)
        
        x = e.x
        y = e.y
        
        self.zoom_factor = np.max([1, self.zoom_factor * zoomFactor])

        if self.labelButtonsActive:
            self.allLab_window = self.canvas.create_window(0.5*self.canvasWidth - 130 , self.canvasHeight + 70, anchor='sw', window=self.allLabButton)
            self.labelInput_window = self.canvas.create_window(self.canvasWidth - 506, self.canvasHeight + 38, anchor='se', window=self.labelInput)
            self.inputButton_window = self.canvas.create_window(self.canvasWidth - 420, self.canvasHeight +38, anchor='se', window=self.inputButton)
        
        
        self.displayImage(self.img_display, (y,x))
        
        try:
            for label in self.labelsImg:
                label.place_forget()
        except:
            pass
        if self.labelledStatus:
            try:

                for l, label in enumerate(self.labelsImg):
                    #print("Labnum = ",l)
                    y, x = self.segmentData[l, :2]
                    #print(x, self.x_displacement)
                    x = (x - self.x_displacement) * self.canvasWidth/2048
                    y = (y - self.y_displacement)  * self.canvasWidth/2048
                    if x < 0 or y < 0:
                        #print(x, y)
                        continue

                    if self.zoom_factor != 1 or self.centre_displace != (0,0):
                        x = x * self.zoom_factor
                        y = y * self.zoom_factor

                    if int(100*self.canvasHeight/self.canvasWidth) > 50:
                        #print("Shifted lower")
                        y = int(y + 0.5*(self.canvasHeight - 0.5*self.canvasWidth))
                    elif int(100*self.canvasHeight/self.canvasWidth) < 50:
                        #print("Shifted right")
                        x = int(x + 0.5*(self.canvasWidth - self.canvasWidth))

                    if 0.5*(self.canvasHeight - 0.5*self.canvasWidth) <= y <= self.canvasHeight - 0.5*(self.canvasHeight - 0.5*self.canvasWidth) and 0.5 * (self.canvasWidth - self.canvasWidth) <= x <= self.canvasWidth - 0.5*(self.canvasWidth - self.canvasWidth):
                        label.place(x=x, y= y, anchor="center")
                    
            except:
                pass


    def pan_image_init(self, e):
        
        self.x_pan_init = e.x
        self.y_pan_init = e.y
        self.y_pan_prev = int(self.y_pan_init)
        self.x_pan_prev = int(self.x_pan_init)

    def pan_image(self, e):
        print("Running pan_image")
        x = e.x
        y = e.y

        yLen, xLen = self.img_orig.shape[:2]
        newX = xLen / self.zoom_factor
        newY = yLen / self.zoom_factor

        if self.zoom_factor != 1:
            self.y_pan = e.y
            y_diff = int(self.y_pan - self.y_pan_prev)
            
            self.x_pan = e.x
            x_diff = int(self.x_pan - self.x_pan_prev)
            
            #print("Diffs are",y_diff, x_diff)
            ## fix edges
            if self.imageCoords[0] == 0 and y_diff > 0:
                y_diff = 0
                #print("T")
            if self.imageCoords[1] == newY and y_diff <= 0: 
                y_diff = 0
                #print("B")

            if self.imageCoords[2] == 0 and x_diff > 0:
                x_diff = 0
                #print("L")
            if self.imageCoords[3] == newX and x_diff <= 0: 
                x_diff = 0
                #print("R")
            #print("Diffs are",y_diff, x_diff)
            self.centre_displace = tuple(np.add(self.centre_displace, (y_diff,x_diff)))
            self.y_pan_prev = int(self.y_pan)
            self.x_pan_prev = int(self.x_pan)
        
        self.displayImage(self.img_display)
        
        try:
            for label in self.labelsImg:
                label.place_forget()
        except:
            pass
        if self.labelledStatus:
            try:

                for l, label in enumerate(self.labelsImg):
                    #print("Labnum = ",l)
                    y, x = self.segmentData[l, :2]
                    #print(x, self.x_displacement)
                    x = (x - self.x_displacement) * self.canvasWidth/2048
                    y = (y - self.y_displacement)  * self.canvasWidth/2048
                    if x < 0 or y < 0:
                        #print(x, y)
                        continue

                    if self.zoom_factor != 1 or self.centre_displace != (0,0):
                        x = x * self.zoom_factor
                        y = y * self.zoom_factor

                    if int(100*self.canvasHeight/self.canvasWidth) > 50:
                        #print("Shifted lower")
                        y = int(y + 0.5*(self.canvasHeight - 0.5*self.canvasWidth))
                    elif int(100*self.canvasHeight/self.canvasWidth) < 50:
                        #print("Shifted right")
                        x = int(x + 0.5*(self.canvasWidth - self.canvasWidth))

                    if 0.5*(self.canvasHeight - 0.5*self.canvasWidth) <= y <= self.canvasHeight - 0.5*(self.canvasHeight - 0.5*self.canvasWidth) and 0.5 * (self.canvasWidth - self.canvasWidth) <= x <= self.canvasWidth - 0.5*(self.canvasWidth - self.canvasWidth):
                        label.place(x=x, y= y, anchor="center")
                    
            except:
                pass
  