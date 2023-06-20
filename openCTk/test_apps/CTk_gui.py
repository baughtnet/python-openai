import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("960x575")
        self.title("Test for GUI")
        self.minsize(500, 300)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)

        lbl_frame = customtkinter.CTkFrame(master=self)
        lbl_frame.grid_columnconfigure(0, weight=1)
        lbl_frame.grid_columnconfigure(1, weight=6)
        lbl_frame.grid_rowconfigure(0, weight=8)
        lbl_frame.grid_rowconfigure(1, weight=1)


        self.textbox = customtkinter.CTkTextbox(master=)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,0), sticky='nsew')

        self.combobox = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        self.combobox.grid(row=1, column=0, padx=20, pady=(20, 0), sticky='ew')
        self.button = customtkinter.CTkButton(master=self, command="", text="Insert Text")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky='ew')


if __name__ == "__main__":
    app = App()
    app.mainloop()
