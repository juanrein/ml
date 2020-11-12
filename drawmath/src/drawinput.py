from tkinter import Canvas, Frame, Button
import numpy as np

class DrawInput(Frame):
    def __init__(self, master, w, h):
        super().__init__(master)
        self.w = w
        self.h = h
        self.initUI()
        
        #container for visited pixels on the canvas
        #keep between [0,1]
        self.image = np.zeros((h,w))
        self.lastx = None
        self.lasty = None


    def initUI(self):
        canvas = Canvas(self, width=self.w, height=self.h, background="white")
        canvas.bind("<Button-1>", self.savePosition)
        canvas.bind("<B1-Motion>", self.drawLine)
        
        canvas.pack()
        self.canvas = canvas

    def clearCanvas(self):
        self.canvas.delete("all")
        self.image = np.zeros((self.h,self.w))

    def savePosition(self, event):
        x = event.x
        y = event.y
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return

        self.lastx = x
        self.lasty = y

        #add events location and it's adjacent pixels
        for i in range(x-2, x+3):
            for j in range(y-2, y+3):
                #skip points outside the drawing area
                if i < 0 or i >= self.w or j < 0 or j >= self.h:
                    continue
                self.image[j][i] = 1.0

    def drawLine(self, event):
        if event.x < 0 or event.y < 0:
            return

        self.canvas.create_line((self.lastx, self.lasty, event.x,event.y), width=4)
        self.savePosition(event)

    def getImage(self):
        return self.image
