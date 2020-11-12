import tkinter as tk       
import random

from src.classifier import Classifier
from src.inputgroup import InputGroup

operators = {
    0: {
        "name": "multiplication",
        "f": lambda a,b: a*b,
        "symbol": "*"
    },
    1: {
        "name": "addition",
        "f": lambda a,b: a+b,
        "symbol": "+"
    }
}

IMAGE_SIZE = (100,100)

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.numberOfInputs = 2
        self.grid()                       
        self.createWidgets()

        self.classifier = Classifier()
        self.classifier.fit(fromFile=True)


    def createWidgets(self):
        self.operatorIndex = tk.IntVar(self, 0)
        self.addInputDrawField()
        self.addOperatorSelectField()
        self.addFields()
        self.addFeedBack()
        self.addExit()
        self.nextGame()
    
    def addOperatorSelectField(self):
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1)
        for k,v in operators.items():
            self.listbox.insert(k, v["name"])

        self.listbox.bind("<Button1-ButtonRelease>", self.changeOperator)

    
    def addFields(self):
        """
        Fields to show the calculation
        """
        self.left = tk.IntVar(self)
        self.right = tk.IntVar(self)
        self.answer = tk.IntVar(self)
        symbol = operators[self.operatorIndex.get()]["symbol"]
        self.operatorValue = tk.StringVar(self, value = symbol)

        elements = [
            tk.Label(self, textvariable=self.left),
            tk.Label(self, textvariable=self.operatorValue),
            tk.Label(self, textvariable=self.right),
            tk.Label(self, text="="),
            tk.Label(self, textvariable=self.answer)
        ]
        for i, e in enumerate(elements):
            e.grid(row=2, column=i)
            setattr(self, str(i), e)
        

    def addFeedBack(self):
        self.feedbackValue = tk.StringVar(self)
        self.feedback = tk.Label(self, textvariable=self.feedbackValue)
        self.feedback.grid(row=3, column=0)

    def addExit(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)            
        self.quitButton.grid(row=4, column=1)    


    def addInputDrawField(self):
        w,h = IMAGE_SIZE
        if hasattr(self, "input"):
            self.input.clear()
            self.input.destroy()

        input = InputGroup(self, self.handleUserInput, w,h,self.numberOfInputs)
        input.grid(row=0)
        self.input = input

    def changeOperator(self, event):
        """
        Change the operator used and update it on gui
        """
        index, = self.listbox.curselection()
        self.operatorIndex.set(index)
        symbol = operators[self.operatorIndex.get()]["symbol"]
        self.operatorValue.set(symbol)


    def handleUserInput(self, images):
        """
        Predict drawn number and update it to gui
        """
        #plt.imsave("digit.png", img)
        answer = ""
        for image in images:
            digit = self.evaluateAsDigit(image)
            answer += str(digit)

        print(answer)
        answer = int(answer)

        self.answer.set(answer)
        self.check()

    def evaluateAsDigit(self, img):
        digit = self.classifier.predict(img)
        return digit

    def nextGame(self):
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.left.set(a)
        self.right.set(b)

        f = operators[self.operatorIndex.get()]["f"]
        answer = f(a,b)
        length_answer = len(str(answer))
        self.numberOfInputs = length_answer

        self.addInputDrawField()

    def check(self):
        """
        Check if the math checks out
        """
        left = self.left.get()
        right = self.right.get()
        f = operators[self.operatorIndex.get()]["f"]
        actual = f(left, right)
        given = self.answer.get()

        symbol = operators[self.operatorIndex.get()]["symbol"]
        if actual == given:
            message = "nice"
            self.nextGame()
        else:
            message = f"{left} {symbol} {right} != {given}"

        self.feedbackValue.set(message)



def run():
    app = Application()                       
    app.master.title('Draw math')    
    app.mainloop()