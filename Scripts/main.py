import os
import csv
import string
import random
import secrets
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mb

import config as cf

class AppMain:
    def __init__(self):
        super().__init__()
        self.activeFont = (cf._selectedTypeface, cf._fontSize)
        
        # Frame & Widget Arrays
        self.totalFrames = []
        self.totalWidgets = []
        self.secondaryFrames = []

        # CONTENT
        self.isWorking = False
        self.user_list = []
        self.pass_list = []
        self.formatted_passwords = []
        self.chars_lower = string.ascii_lowercase
        self.chars_upper = string.ascii_uppercase
        self.chars_digits = string.digits
        self.config_digits = [
            "!", "_", "*", "$", "^", "@"
        ]
        self.chars_lower*5
        self.chars_upper*=5
        self.chars_digits*=10

        # Command line in/out variables
        self.clOutText = ""
        self.clOutIndex = 0
        self.isWriting = False
        self.breakLoop = False

        # Root Frame
        self.root = tk.Tk()
        self.root.geometry("465x350")
        self.root.title("W-")
        self.root.eval('tk::PlaceWindow . center')
        self.totalFrames.append(self.root)
        
        # Init UI
        self.initBaseUI()
        self.initContentUI()
        
        self.changeColorTheme(0)
        
        # Setup Keybinds
        self.root.bind("<Control-space>", lambda event: self.clInput.focus())
        self.clInput.bind("<KeyRelease>", self.checkInput)
        self.clInput.bind("<Return>", self.runCommand)

        # Run Main UI Loop
        self.root.mainloop()



    def initBaseUI(self):
        #! COMMAND FRAME
        self.commandFrame = tk.Frame(self.root)
        self.commandFrame.pack(side=tk.BOTTOM, fill=tk.X)
        self.secondaryFrames.append(self.commandFrame)
        
        self.clInput = tk.Entry(self.commandFrame, width=10, font=self.activeFont)
        self.clInput.pack(side=tk.LEFT)
        self.clInput.insert(tk.END, "/")
        self.totalWidgets.append(self.clInput)
        
        self.clOutput = tk.Entry(self.commandFrame, font=self.activeFont)
        self.clOutput.insert(tk.END, ">>")
        self.clOutput.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.totalWidgets.append(self.clOutput)

        #! NOTEBOOK / TAB FRAME
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.nstyle = ttk.Style()
        self.nstyle.theme_use('default')

        self.mainFrame = tk.Frame(self.notebook)
        self.notebook.add(self.mainFrame, text="[APP]")
        self.totalFrames.append(self.mainFrame)

        self.configFrame = tk.Frame(self.notebook)
        self.notebook.add(self.configFrame, text="[CONFIG]")
        self.totalFrames.append(self.configFrame)

        #!----- CONTENT -----!#
        #?--- MAIN ---?#
        self.subFrame = tk.Frame(self.mainFrame)
        self.subFrame.pack(fill=tk.BOTH, expand=True)
        self.totalFrames.append(self.subFrame)

        self.mainFrameLeft = tk.Frame(self.subFrame)
        self.mainFrameLeft.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.totalFrames.append(self.mainFrameLeft)
        self.mainFrameRight = tk.Frame(self.subFrame)
        self.mainFrameRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.totalFrames.append(self.mainFrameRight)

        #?--- CONFIG ---?#
        self.configLeftFrame = tk.Frame(self.configFrame)
        self.configLeftFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=3)
        self.totalFrames.append(self.configLeftFrame)

        self.configMiddleFrame = tk.Frame(self.configFrame)
        self.configMiddleFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=3)
        self.totalFrames.append(self.configMiddleFrame)

        self.configRightFrame = tk.Frame(self.configFrame)
        self.configRightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=3)
        self.totalFrames.append(self.configRightFrame)


        self.rsep = tk.Label(self.configRightFrame, text="", font=self.activeFont)
        self.rsep.pack(pady=2)
        self.totalWidgets.append(self.rsep)
        self.themeValue = tk.StringVar()
        self.themeValue.set(cf._themeOptions[0])
        self.themeComboBox = tk.OptionMenu(self.configRightFrame, self.themeValue, *cf._themeOptions, command= lambda event: self.changeColorTheme(0, 3))
        self.themeComboBox.configure(font=self.activeFont)
        menu = self.root.nametowidget(self.themeComboBox.menuname)
        menu.configure(font=self.activeFont)
        self.themeComboBox.pack()
        self.totalWidgets.append(self.themeComboBox)

    def initContentUI(self):
        self.userListLabel = tk.Label(self.mainFrameLeft, text="-- USER LIST --", font=self.activeFont)
        self.userListLabel.pack()
        self.totalWidgets.append(self.userListLabel)
        self.userList = tk.Listbox(self.mainFrameLeft, font=self.activeFont)
        self.userList.pack(fill=tk.BOTH, expand=True)
        self.totalWidgets.append(self.userList)

        self.addUserBtn = tk.Button(self.mainFrameLeft, text="ADD", font=self.activeFont, command=self.AddUser)
        self.addUserBtn.pack(side=tk.LEFT)
        self.totalWidgets.append(self.addUserBtn)

        self.delUserBtn = tk.Button(self.mainFrameLeft, text="DEL", font=self.activeFont, command=self.GetUserSelection)
        self.delUserBtn.pack(side=tk.LEFT)
        self.totalWidgets.append(self.delUserBtn)

        self.importUserBtn = tk.Button(self.mainFrameLeft, text="IMPORT", font=self.activeFont, command=self.ImportUserList)
        self.importUserBtn.pack(side=tk.LEFT)
        self.totalWidgets.append(self.importUserBtn)

        self.passListLabel = tk.Label(self.mainFrameRight, text="-- PASSWORD LIST --", font=self.activeFont)
        self.passListLabel.pack()
        self.totalWidgets.append(self.passListLabel)
        self.passList = tk.Listbox(self.mainFrameRight, font=self.activeFont)
        self.passList.pack(fill=tk.BOTH, expand=True)
        self.totalWidgets.append(self.passList)

        self.clearPassBtn = tk.Button(self.mainFrameRight, text="CLEAR", font=self.activeFont)
        self.clearPassBtn.pack(side=tk.RIGHT)
        self.totalWidgets.append(self.clearPassBtn)

        self.delPassBtn = tk.Button(self.mainFrameRight, text="DEL", font=self.activeFont)
        self.delPassBtn.pack(side=tk.RIGHT)
        self.totalWidgets.append(self.delPassBtn)
        

        self.genPassBtn = tk.Button(self.subFrame, text="GENERATE", font=self.activeFont, command=self.GeneratePasswords)
        self.genPassBtn.pack(side=tk.BOTTOM)
        self.totalWidgets.append(self.genPassBtn)
        
        #! CONFIG
        self.configPassLen = 12

        self.lsep = tk.Label(self.configLeftFrame, text="", font=self.activeFont)
        self.lsep.pack(pady=2)
        self.totalWidgets.append(self.lsep)

        self.passLenLbl = tk.Label(self.configLeftFrame, text="PASSWORD LENGTH", font=self.activeFont)
        self.passLenLbl.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.passLenLbl)

        self.cPassLenScale = tk.Scale(self.configLeftFrame, from_=4, to=42, orient=tk.HORIZONTAL, font=self.activeFont, troughcolor="black", command=self.ReConfigSliders)
        self.cPassLenScale.set(self.configPassLen)
        self.cPassLenScale.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.cPassLenScale)
        #self.totalWidgets.append(self.lsep0)

        self.specCharDensityLbl = tk.Label(self.configLeftFrame, text="SPECIAL CHARACTER DENSITY", font=self.activeFont)
        self.specCharDensityLbl.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.specCharDensityLbl)
        self.specCharDensityScale = tk.Scale(self.configLeftFrame, from_=0, to=self.cPassLenScale.get()-1, orient=tk.HORIZONTAL, font=self.activeFont, troughcolor="black", command=self.ConfigSliderValueSet)
        self.specCharDensityScale.set(int(self.cPassLenScale.get()/4))
        self.specCharDensityScale.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.specCharDensityScale)

        self.upperDensityLbl = tk.Label(self.configLeftFrame, text="UPPERCASE DENSITY", font=self.activeFont)
        self.upperDensityLbl.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.upperDensityLbl)
        self.upperDensityScale = tk.Scale(self.configLeftFrame, from_=0, to=self.cPassLenScale.get()-1, orient=tk.HORIZONTAL, font=self.activeFont, troughcolor="black", command=self.ConfigSliderValueSet)
        self.upperDensityScale.set(int(self.cPassLenScale.get()/4))
        self.upperDensityScale.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.upperDensityScale)

        self.numberDensityLbl = tk.Label(self.configLeftFrame, text="NUMBER DENSITY", font=self.activeFont)
        self.numberDensityLbl.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.numberDensityLbl)
        self.numberDensityScale = tk.Scale(self.configLeftFrame, from_=0, to=self.cPassLenScale.get()-1, orient=tk.HORIZONTAL, font=self.activeFont, troughcolor="black", command=self.ConfigSliderValueSet)
        self.numberDensityScale.set(int(self.cPassLenScale.get()/4))
        self.numberDensityScale.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.numberDensityScale)

        #self.lsep0 = ttk.Separator(self.configLeftFrame, orient=tk.VERTICAL)
        #self.lsep0.pack(side=tk.RIGHT, pady=5, fill=tk.Y, expand=1)

        self.msep0 = tk.Label(self.configMiddleFrame, text="", font=self.activeFont)
        self.msep0.pack(pady=2)
        self.totalWidgets.append(self.msep0)

        self.customPhraseLbl = tk.Label(self.configMiddleFrame, text="CUSTOM PHRASE", font=self.activeFont)
        self.customPhraseLbl.pack()
        self.totalWidgets.append(self.customPhraseLbl)

        self.customPhraseInput = tk.Entry(self.configMiddleFrame, font=self.activeFont)
        self.customPhraseInput.pack()
        self.customPhraseInput.bind("<KeyRelease>", self.ReConfigSliders)
        self.totalWidgets.append(self.customPhraseInput)

        self.msep1 = tk.Label(self.configMiddleFrame, text="", font=self.activeFont)
        self.msep1.pack(pady=2)
        self.totalWidgets.append(self.msep1)

        self.customPhrasePosLbl = tk.Label(self.configMiddleFrame, text="PHRASE POSITION", font=self.activeFont)
        self.customPhrasePosLbl.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.customPhrasePosLbl)
        self.customPhrasePosScale = tk.Scale(self.configMiddleFrame, from_=0, to=self.cPassLenScale.get()-1, orient=tk.HORIZONTAL, font=self.activeFont, troughcolor="black", command=self.ConfigSliderValueSet)
        self.customPhrasePosScale.set(int(0))
        self.customPhrasePosScale.pack(anchor=tk.CENTER)
        self.totalWidgets.append(self.customPhrasePosScale)

        self.repeatingCharLbl = tk.Label(self.configMiddleFrame, text="", font=self.activeFont)
        self.repeatingCharLbl.pack()
        self.totalWidgets.append(self.repeatingCharLbl)

        self.repeatingCharVal = tk.IntVar(value=1)
        self.repeatingCharBox = tk.Checkbutton(self.configMiddleFrame, text="REPEATING CHAR", font=self.activeFont, variable=self.repeatingCharVal)
        self.repeatingCharBox.pack()
        self.totalWidgets.append(self.repeatingCharBox)

    def changeColorTheme(self, event=None, tIndex=None):
        if tIndex == 3:
            _index = cf._themeOptions.index(self.themeValue.get())
        elif tIndex != None: 
            _index = tIndex
        else:
            _index = 0
        
        if tIndex != None:
            if _index == 0:
                self.clOutText=">> Color theme change to dark"
            else:
                self.clOutText=">> Color theme change to light"
            self.clOutIndex = 0
            self.clOutput.delete(0, tk.END)
            self.writingOut = 1
            if self.isWriting:
                self.breakLoop = True
            self.outputTyper()


        for _frame in self.totalFrames:
            _frame.configure(bg=cf._backgroundColors[_index])
            
        for _widget in self.totalWidgets:
            _widget.configure(
                bg=cf._backgroundColors[_index], 
                fg=cf._typefaceColors[_index], 
                highlightcolor=cf._backgroundColors[_index]
            )
            
        self.nstyle.configure('TNotebook.Tab',
            background=cf._tabColors[_index][1],
            foreground=cf._backgroundColors[_index],
            bordercolor=cf._backgroundColors[_index],
            borderwidth=0, 
            tabmargins=0
        )
        self.nstyle.configure('TSeparator',
            background=cf._extraColors[_index],
            borderwidth=0, 
            tabmargins=0
        )
        self.nstyle.map("TNotebook.Tab", background=[("selected", cf._tabColors[_index][0])])
        self.nstyle.configure('TNotebook', 
            background=cf._backgroundColors[_index],
            highlightbackground=cf._backgroundColors[_index],
            bordercolor=cf._backgroundColors[_index],
            borderwidth=0, 
            tabmargins=0
        )
        self.clInput.configure(insertbackground=cf._typefaceColors[_index])
        self.clOutput.configure(insertbackground=cf._typefaceColors[_index])
        self.customPhraseInput.configure(insertbackground=cf._typefaceColors[_index])
        self.repeatingCharBox.configure(selectcolor=cf._backgroundColors[_index])
        self.repeatingCharBox.configure(activebackground=cf._backgroundColors[_index])

    def checkInput(self, event=None):
        _input = str(self.clInput.get()[1:])
        self.clInput.delete(0, tk.END)
        self.clInput.insert(0, f"/{_input}")

    def runCommand(self, event=None):
        _input = str(self.clInput.get()[1:])

        if _input == "1":
            self.notebook.select(0)
            self.clOutText=">> Main Page Loaded"
        elif _input == "2":
            self.notebook.select(1)
            self.clOutText=">> Settings Page Loaded"
        elif "help" in _input.lower():
            self.popupWindow("", "BASIC COMMANDS\n'help' - Basic command list\ninfo - General info on app & pc\n[1,2] - Change active tab")
            self.clOutText=">> help, info, 1, 2"
        elif "light" in _input.lower():
            self.changeColorTheme(0, 1)
        elif "dark" in _input.lower():
            self.changeColorTheme(0, 0)
        elif "exit" in _input.lower():
            self.clOutText=">> Goodbye < 3 "
        elif _input.lower() == "gen":
            self.GeneratePasswords()
        elif "." in _input.lower():
            _command = _input.lower()[2:]
        elif _input.lower() =="import":
            self.clOutText = ">> Importing CSV"
            self.ImportUserList()
        else:
            self.clOutText=f">> Command '{_input}' not found"

        self.clInput.delete(0, tk.END)
        self.clOutIndex = 0
        self.clOutput.delete(0, tk.END)
        self.writingOut = 1
        if self.isWriting:
            self.breakLoop = True
        self.outputTyper()

    

    #! CONTENT
    def GetUserSelection(self):
        _selected = self.userList.curselection()
        if not _selected:
            mb.showerror("", "No Selected Item")
            return
        _index = self.userList.get(_selected)
        self.DeleteUser(_index)
        #? Create a dynamic cout method

    def AddUser(self):
        _user = self.clInput.get()[1:]
        if _user == "":
            _user = f"tempUser{len(self.user_list)}"
        self.user_list.append(f"{_user}")
        self.userList.delete(0, tk.END)
        self.userList.insert(0, *self.user_list)

        self.userList.selection_set(tk.END)
        self.userList.see(tk.END)

        self.clInput.delete(0, tk.END)
        self.checkInput()
        
    def DeleteUser(self, index):
        self.user_list.remove(index)
        self.userList.delete(0, tk.END)
        self.userList.insert(0, *self.user_list)

    def ImportUserList(self):
        _fp = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        _tempUserList = []
        with open(_fp, 'r') as _file:
            reader = csv.reader(_file)
            print(reader)
            for row in reader:
                self.user_list.append(row[0])
        self.userList.delete(0, tk.END)
        self.userList.insert(0, *self.user_list)

    def GeneratePasswords(self):
        if self.isWorking == False:
            self.isWorking = True
            self.pass_list.clear()
            _tempDate = datetime.date.today()

            _specCharStr = ''.join(self.config_digits)
            _specCharStr*=10

            self.chars = ""
            self.chars_lower = self.TempShuffler(self.chars_lower)
            _phraseVal = self.customPhraseInput.get()

            if len(self.user_list) == 0:
                self.AddUser()
            for index in range(len(self.user_list)):

                if self.upperDensityScale.get() > 0:
                    self.chars_upper = self.TempShuffler(self.chars_upper)
                    _upperList = self.chars_upper[:self.upperDensityScale.get()]
                    self.chars += _upperList

                if self.numberDensityScale.get() > 0:
                    self.chars_digits = self.TempShuffler(self.chars_digits)
                    _digitList = self.chars_digits[:self.numberDensityScale.get()]
                    self.chars += _digitList

                if self.specCharDensityScale.get() > 0:
                    _specCharStr = self.TempShuffler(_specCharStr)
                    _specCharList = _specCharStr[:self.specCharDensityScale.get()]
                    self.chars += _specCharList

                max_val = self.cPassLenScale.get()
                curr_sum = self.upperDensityScale.get() + self.numberDensityScale.get() + self.specCharDensityScale.get()
                _customPhrase = ""
                if len(_phraseVal) > 0:
                    curr_sum += len(_phraseVal)
                    _customPhrase = f"{self.customPhraseInput.get()}"
                remains = max_val - curr_sum
                _basePass = ''
                _lastChar = None
                for i in range(remains):
                    _newChar = secrets.choice(self.chars_lower)
                    if self.repeatingCharVal.get() == 0:
                        while _newChar == _lastChar:
                            _newChar = secrets.choice(self.chars_lower)
                    _basePass += _newChar
                    _lastChar = _newChar
                _password = self.TempShuffler(_basePass + self.chars)
                _password = _password[:self.customPhrasePosScale.get()] + _customPhrase + _password[self.customPhrasePosScale.get():]
                self.pass_list.append(_password)
                self.formatted_passwords.append(f"{self.user_list[index]}, {_password}")
                _password = ""
                self.chars = ""
            self.passList.delete(0, tk.END)
            self.passList.insert(0, *self.pass_list)

            self.clOutText = ">> Passwords Generated"
            #self.clInput.delete(0, tk.END)
            self.clOutIndex = 0
            self.clOutput.delete(0, tk.END)
            self.writingOut = 1
            if self.isWriting:
                self.breakLoop = True
            self.outputTyper()
            self.isWorking = False
        else:
            mb.showerror("", "Already attempting to generate password")

    def TempShuffler(self, stringToShuffle):
        _tempList = list(stringToShuffle)
        _finalList = []
        _lastChar = ""
        for _i in range(len(_tempList)):
            _newChar = str(secrets.choice(_tempList))
            if self.repeatingCharVal.get() == 0:
                while _newChar == _lastChar:
                    _newChar = str(secrets.choice(_tempList))
            _tindex = _tempList.index(_newChar)
            _finalList.append(_newChar)
            print(_tempList)
            print(_tindex)
            del _tempList[_tindex]
            print(_tempList)
            _lastChar = _newChar
        _return = ''.join(_finalList)
        return _return

    def ReConfigSliders(self, event=None):
        self.specCharDensityScale.configure(from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
        self.upperDensityScale.configure(from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
        self.numberDensityScale.configure(from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
        self.customPhrasePosScale.configure(from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()))
        self.ConfigSliderValueSet()

    def ConfigSliderValueSet(self, event=None):
        max_val = self.cPassLenScale.get()-1
        curr_sum = self.specCharDensityScale.get() + self.upperDensityScale.get() + self.numberDensityScale.get()
        _phraseVal = self.customPhraseInput.get()
        if len(_phraseVal) > 0:
            curr_sum += len(_phraseVal)
        remains = max_val - curr_sum
        adj = remains // 4
        if (curr_sum > max_val):
            self.specCharDensityScale.set(self.specCharDensityScale.get()+adj)
            self.upperDensityScale.set(self.upperDensityScale.get()+adj)
            self.numberDensityScale.set(self.numberDensityScale.get()+adj)


    # DEFAULT VISUAL
    def outputTyper(self):
        self.isWriting = True
        if self.breakLoop:
            self.breakLoop = False
            self.clOutIndex = 0
            return
        self.clOutput.insert(tk.END, self.clOutText[self.clOutIndex])
        self.clOutIndex += 1 
        if self.clOutIndex < len(self.clOutText):
            typeDelay = random.randint(5, 50)
            if typeDelay >= 40:
                typeDelay = random.randint(75, 200)
            self.root.after(typeDelay, self.outputTyper)
        else:
            self.clOutIndex = 0
            self.isWriting = False
            if ">> Goodbye < 3 " in self.clOutText: exit()

    def popupWindow(self, type, msg):
        if type == "alert":
            mb.showinfo("", f"{msg}")
        else:
            _index = cf._themeOptions.index(self.themeValue.get())
            _tempWindow = tk.Toplevel(self.root)
            _tempWindow.geometry("200x175")
            _tempWindow.title("INFO")
            _tempWindow.configure(background=cf._backgroundColors[_index])
            _tempLbl = tk.Label(_tempWindow, text=f"{msg}", font=self.activeFont, background=cf._backgroundColors[_index], fg=cf._typefaceColors[_index])
            _tempLbl.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, pady=15)
            
if __name__ == "__main__":
    AppMain()