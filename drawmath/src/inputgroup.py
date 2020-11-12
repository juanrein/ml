from tkinter import Frame, Button
import numpy as np
from src.drawinput import DrawInput

class InputGroup(Frame):
    def __init__(self, master, handler, w,h, numberOfInputs):
        super().__init__(master)

        self.inputs = []
        self.handler = handler
        self.w = w
        self.h = h
        self.numberOfInputs = numberOfInputs
        self.initUI()

    def initUI(self):
        for i in range(self.numberOfInputs):
            input = DrawInput(self, self.w, self.h)
            self.inputs.append(input)
            input.grid(row=0, column=i)

        checkButton = Button(self, text="Check", command=self.handleData)
        checkButton.grid(row=1, column=0)

        button = Button(self, text="Reset", command=self.clearCanvas)
        button.grid(row=1, column=1)

    def clear(self):
        for input in self.inputs:
            input.destroy()

    def clearCanvas(self):
        for input in self.inputs:
            input.clearCanvas()
        
    def handleData(self):
        images = []

        for input in self.inputs:
            image = input.getImage()
            images.append(image)

        self.handler(images)