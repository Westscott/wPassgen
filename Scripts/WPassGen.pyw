import os
import csv
import string
import random
import secrets
import datetime
import customtkinter as ctk

class WPassGen:
    def __init__(self):
        self.activeFont = ("Consolas", 12)
        self.scaleValue = "100 %"

        self.passwordList = []
        self.finalPassList = []

        self.chars_lower = string.ascii_lowercase * 5
        self.chars_upper = string.ascii_uppercase * 5
        self.chars_digits = string.digits * 5
        self.chars_specChar = "&!_*$^@#%" * 5

        # Initialize the main application window
        self.root = ctk.CTk()
        self.root.geometry("650x500")
        self.root.title("Matthew's Pass Gen")
        self.root.eval('tk::PlaceWindow . center')
        #self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.initFrames()
        self.initWidgets()
        self.update_progress_bar()

        self.root.mainloop()

    def initFrames(self):
        self.mainFrame = ctk.CTkFrame(self.root)
        self.mainFrame.pack(fill=ctk.BOTH, expand=True)

        self.subFrameLeft = ctk.CTkFrame(self.mainFrame)
        self.subFrameLeft.pack(side=ctk.LEFT, padx=20, pady=20, fill=ctk.Y)
 
        self.sbf_passLenFrame = ctk.CTkFrame(self.subFrameLeft)
        self.sbf_passLenFrame.pack(side=ctk.TOP, padx=10, pady=10)

        self.sbf_densityFrame = ctk.CTkFrame(self.subFrameLeft)
        self.sbf_densityFrame.pack(side=ctk.TOP, padx=10, pady=10)

        self.sbf_phraseFrame = ctk.CTkFrame(self.subFrameLeft)
        self.sbf_phraseFrame.pack(side=ctk.TOP, padx=10, pady=10)
        
        self.subFrameRight = ctk.CTkFrame(self.mainFrame)
        self.subFrameRight.pack(side=ctk.RIGHT, padx=20, pady=20, fill=ctk.BOTH, expand=True)

        self.bottomFrame = ctk.CTkFrame(self.root)
        self.bottomFrame.pack(side=ctk.BOTTOM, fill=ctk.X)

        self.complexityBar = ctk.CTkProgressBar(self.bottomFrame)
        self.complexityBar.pack(fill=ctk.BOTH)

        #marker = ctk.CTkLabel(self.bottomFrame, text='|', font=self.activeFont, text_color='#2fa572')
        #marker.place(relx=0.5, rely=0.5, anchor='center')


    def initWidgets(self):
        # Password listbox
        self.passList = ctk.CTkTextbox(self.subFrameRight, font=self.activeFont)
        self.passList.pack(fill=ctk.BOTH, pady=10, padx=10, expand=True)

        # Action Button
        self.copyAllButton = ctk.CTkButton(self.subFrameRight, text="COPY ALL", font=self.activeFont, command=self.CopyAllPasswords)
        self.copyAllButton.pack(side=ctk.LEFT,padx=10, pady=10, fill=ctk.X, expand=True)
       
        self.creditsButton = ctk.CTkButton(self.subFrameRight, text="SETTINGS", font=self.activeFont, command=self.SimpleSettingsMenu)
        self.creditsButton.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.X, expand=True)

        #Password Amount
        self.passwordAmountLabel = ctk.CTkLabel(self.sbf_passLenFrame, text="QTY: 1", font=self.activeFont)
        self.passwordAmountLabel.pack(anchor=ctk.N)
        self.passwordAmount = ctk.CTkSlider(self.sbf_passLenFrame, from_=1, to=50, number_of_steps=49, command=self.UpdateQtySlider)
        self.passwordAmount.set(1)
        self.passwordAmount.pack(side=ctk.TOP, padx=5)

        # Password length
        self.configPassLen = 12
        self.passLenLabel = ctk.CTkLabel(self.sbf_passLenFrame, text="PASSWORD LENGTH: 12", font=self.activeFont)
        self.passLenLabel.pack(anchor=ctk.N)
        self.cPassLenScale = ctk.CTkSlider(self.sbf_passLenFrame, from_=6, to=42, number_of_steps=36, command=self.ReConfigSliders)
        self.cPassLenScale.set(self.configPassLen)
        self.cPassLenScale.pack(anchor=ctk.CENTER)

        # Custom phrase
        self.customPhraseLbl = ctk.CTkLabel(self.sbf_phraseFrame, text="CUSTOM PHRASE", font=self.activeFont)
        self.customPhraseLbl.pack(anchor=ctk.N)
        self.customPhraseInput = ctk.CTkEntry(self.sbf_phraseFrame, font=self.activeFont)
        self.customPhraseInput.pack(pady=5)
        self.customPhraseInput.bind("<KeyRelease>", self.ReConfigSliders)

        # Phrase position
        self.customPhrasePosLbl = ctk.CTkLabel(self.sbf_phraseFrame, text="PHRASE POSITION", font=self.activeFont)
        self.customPhrasePosLbl.pack(anchor=ctk.CENTER)
        self.customPhrasePosScale = ctk.CTkSlider(self.sbf_phraseFrame, from_=0, to=self.cPassLenScale.get() - 1, number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1, command=self.ConfigSliderValueSet)
        self.customPhrasePosScale.set(int(0))
        self.customPhrasePosScale.pack(anchor=ctk.CENTER)

        # Special character density
        self.specCharDensityLbl = ctk.CTkLabel(self.sbf_densityFrame, text="SPECIAL CHARACTER DENSITY", font=self.activeFont)
        self.specCharDensityLbl.pack(anchor=ctk.CENTER)
        self.specCharDensityScale = ctk.CTkSlider(self.sbf_densityFrame, from_=0, to=self.cPassLenScale.get() - 1, number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1, command=self.ConfigSliderValueSet)
        self.specCharDensityScale.set(int(self.cPassLenScale.get() / 4))
        self.specCharDensityScale.pack(anchor=ctk.CENTER)

        # Uppercase density
        self.upperDensityLbl = ctk.CTkLabel(self.sbf_densityFrame, text="UPPERCASE DENSITY", font=self.activeFont)
        self.upperDensityLbl.pack(anchor=ctk.CENTER)
        self.upperDensityScale = ctk.CTkSlider(self.sbf_densityFrame, from_=0, to=self.cPassLenScale.get() - 1, number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1,command=self.ConfigSliderValueSet)
        self.upperDensityScale.set(int(self.cPassLenScale.get() / 4))
        self.upperDensityScale.pack(anchor=ctk.CENTER)

        # Number density
        self.numberDensityLbl = ctk.CTkLabel(self.sbf_densityFrame, text="NUMBER DENSITY", font=self.activeFont)
        self.numberDensityLbl.pack(anchor=ctk.CENTER)
        self.numberDensityScale = ctk.CTkSlider(self.sbf_densityFrame, from_=0, to=self.cPassLenScale.get() - 1, number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1,command=self.ConfigSliderValueSet)
        self.numberDensityScale.set(int(self.cPassLenScale.get() / 4))
        self.numberDensityScale.pack(anchor=ctk.CENTER)

        # Generate Button
        self.genPasswordBtn = ctk.CTkButton(self.subFrameLeft, text="GENERATE", font=self.activeFont, command=self.GeneratePassword)
        self.genPasswordBtn.pack(side=ctk.BOTTOM, padx=20, pady=10, fill=ctk.X)
        

    def on_closing(self):
        self.passList.delete("0.0", ctk.END)
        self.chars = None
        self.currVal = None
        self.lastVal = None
        self.root.destroy()
        exit()
        

    def CustomPhraseManager(self):
        print("basic setup for the custom phrase")

    def GeneratePassword(self):
        self.ClearAllPasswords()
        for index in range(int(self.passwordAmount.get())):
            self.chars = ""
            self.currVal = None
            self.lastVal = None
            lastVal = None

            # Uppercase characters
            if self.upperDensityScale.get() > 0:
                for _ in range(int(self.upperDensityScale.get())):
                    newVal = self.CharSelector(self.chars_upper)
                    self.chars += newVal

            # Digits
            if self.numberDensityScale.get() > 0:
                for _ in range(int(self.numberDensityScale.get())):
                    newVal = self.CharSelector(self.chars_digits)
                    self.chars += newVal

            # Special characters
            if self.specCharDensityScale.get() > 0:
                for _ in range(int(self.specCharDensityScale.get())):
                    newVal = self.CharSelector(self.chars_specChar)
                    self.chars += newVal

            # Remaining characters
            max_val = int(self.cPassLenScale.get())
            curr_sum = int(self.upperDensityScale.get() + self.numberDensityScale.get() + self.specCharDensityScale.get())
            if len(self.customPhraseInput.get()) > 0:
                curr_sum += len(self.customPhraseInput.get())
            remains = max_val - curr_sum
            _basePass = ''

            for _ in range(remains):
                newVal = self.CharSelector(self.chars_lower)
                _basePass += newVal
            _FP = self.TempShuffler(_basePass + self.chars)
            _FP = _FP[:int(self.customPhrasePosScale.get())] + str(self.customPhraseInput.get()) + _FP[int(self.customPhrasePosScale.get()):]
            self.passList.insert(ctk.END, _FP + "\n")
            _FP = None
            _basePass = None
            self.chars = None
            newVal = None

    def CharSelector(self, targetList):
        self.currVal = secrets.choice(targetList)
        while self.currVal == self.lastVal:
            self.currVal = secrets.choice(targetList)
        self.lastVal = self.currVal
        return self.currVal

    def TempShuffler(self, stringToShuffle):
        char_list = list(stringToShuffle)
        random.shuffle(char_list) 
        return "".join(char_list)

    def check_password_complexity(self):
        complexity = 0

        if int(self.cPassLenScale.get()) > 38:
            complexity += 0.6
        elif int(self.cPassLenScale.get()) > 32:
            complexity += 0.6
        elif int(self.cPassLenScale.get()) > 25:
            complexity += 0.6
        elif int(self.cPassLenScale.get()) > 20:
            complexity += 0.5
        elif int(self.cPassLenScale.get()) > 18:
            complexity += 0.4
        elif int(self.cPassLenScale.get()) > 16:
            complexity += 0.3
        elif int(self.cPassLenScale.get()) > 14:
            complexity += 0.2
        elif int(self.cPassLenScale.get()) > 12:
            complexity += 0.175
        elif int(self.cPassLenScale.get()) > 10:
            complexity += 0.135
        elif int(self.cPassLenScale.get()) > 8:
            complexity += 0.1
        elif int(self.cPassLenScale.get()) > 6:
            complexity += 0.05

        if int(self.specCharDensityScale.get()) >= 3:
            complexity += 0.2
        elif int(self.specCharDensityScale.get()) >= 2:
            complexity += 0.1
        elif int(self.specCharDensityScale.get()) >= 1:
            complexity += 0.05

        if int(self.upperDensityScale.get()) >= 3:
            complexity += 0.2
        elif int(self.upperDensityScale.get()) >= 2:
            complexity += 0.1
        elif int(self.upperDensityScale.get()) >= 1:
            complexity += 0.05

        if int(self.numberDensityScale.get()) >= 3:
            complexity += 0.2
        elif int(self.numberDensityScale.get()) >= 2:
            complexity += 0.1
        elif int(self.numberDensityScale.get()) >= 1:
            complexity += 0.05

        return complexity

    def update_progress_bar(self):
        start_color = self.hex_to_rgb("#c42b1c")  # red
        end_color = self.hex_to_rgb("#2fa572") # green
        complexity = self.check_password_complexity()
        self.complexityBar.set(complexity)
        self.complexityBar['value'] = complexity
        interpolated_color = self.interpolate_color(start_color, end_color, complexity)
        hex_color = f'#{interpolated_color[0]:02x}{interpolated_color[1]:02x}{interpolated_color[2]:02x}'
        self.complexityBar.configure(progress_color=hex_color)

        #print (f"{complexity}")

    def hex_to_rgb(self, hex_color):
        """Convert HEX color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def interpolate_color(self, color1, color2, factor):
        """Interpolate between two colors.""" 
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor),
        )

    def ReConfigSliders(self, event=None):
        try:
            self.passLenLabel.configure(text=f"PASS LENGTH: {int(self.cPassLenScale.get())}")
            self.specCharDensityScale.configure(number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1, from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
            self.upperDensityScale.configure(number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1, from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
            self.numberDensityScale.configure(number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1, from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()) - 1)
            self.customPhrasePosScale.configure(number_of_steps=self.cPassLenScale.get()-len(self.customPhraseInput.get()), from_=0, to=self.cPassLenScale.get()-len(self.customPhraseInput.get()))
            self.ConfigSliderValueSet()
        except Exception as e:
            print(f"-")

    def ConfigSliderValueSet(self, event=None):
        try:
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
        except Exception as e:
            print("~")
        self.update_progress_bar()

    def UpdateQtySlider(self, event=None):
        self.passwordAmountLabel.configure(text=f"QTY: {int(self.passwordAmount.get())}")

    def CopyAllPasswords(self):
        text = self.passList.get("1.0", ctk.END)
        self.root.clipboard_clear()  # Clear the clipboard
        self.root.clipboard_append(text)
        self.SimplePopupWindow("TEXT COPIED", "ALL PASSWORDS COPIED")

    def ClearAllPasswords(self):
        self.passList.delete('0.0', ctk.END)

    def SimplePopupWindow(self, title1, text):
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"")
        popup_width = 200
        popup_height = 150
        popup.geometry(f"{popup_width}x{popup_height}")
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup_width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup_height // 2)
        popup.geometry(f"+{x}+{y}")
        #popup.resizable(False, False)
        popup.attributes('-topmost', True)

        label_text = ctk.CTkLabel(popup, text=f"{text}", font=self.activeFont)
        label_text.pack(pady=20)

        close_button = ctk.CTkButton(
            popup,
            text="CLOSE",
            font=self.activeFont,
            command=popup.destroy
        )
        close_button.pack(pady=10)

    def SimpleSettingsMenu(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"SETTINGS")
        popup_width = 275
        popup_height = 300
        popup.geometry(f"{popup_width}x{popup_height}")
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup_width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup_height // 2)
        popup.geometry(f"+{x}+{y}")
        #popup.resizable(False, False)
        popup.attributes('-topmost', True)

        contentFrame1 = ctk.CTkFrame(popup)
        contentFrame1.pack(padx=10, pady=10)

        #contentFrame2 = ctk.CTkFrame(popup)
        #contentFrame2.pack(padx=10, pady=10)

        contentFrame3 = ctk.CTkFrame(popup)
        contentFrame3.pack(padx=10, pady=10)

        appearance_mode_text = ctk.CTkLabel(contentFrame1, text="PRIMARY COLOR", font=self.activeFont)
        appearance_mode_text.pack()
        appearance_mode_optionemenu = ctk.CTkOptionMenu(contentFrame1, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.pack()

        scaling_optiontext = ctk.CTkLabel(contentFrame3, text="UI SCALING", font=self.activeFont)
        scaling_optiontext.pack()
        scaling_optionmenu = ctk.CTkOptionMenu(contentFrame3, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        scaling_optionmenu.set(self.scaleValue)
        scaling_optionmenu.pack()

        close_button = ctk.CTkButton(
            popup,
            text="CLOSE",
            font=self.activeFont,
            command=popup.destroy
        )
        close_button.pack(side=ctk.BOTTOM, pady=10)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def change_scaling_event(self, new_scaling: str):
        self.scaleValue = new_scaling
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    WPassGen()