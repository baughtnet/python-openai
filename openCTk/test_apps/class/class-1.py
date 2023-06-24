# import libraries
from time import sleep
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os


# Set up app appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class BaseLayout:
    def __init__(self, root):
        self.root = root

class MaximizedLayout(BaseLayout):
    def __init__(self, root):
        super().__init__(root)

class NormalLayout(BaseLayout):
    def __init__(self, root):
        super().__init__(root)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("Custom OpenAI")
        # self.tab_view

        # Create the tab view
        tab_view = customtkinter.CTkTabview(master=self)
        tab_view.pack(fill='both', expand=True, padx=5, pady=5)

        # Create the tabs
        normal_tab = customtkinter.CTkFrame(tab_view)
        code_tab = customtkinter.CTkFrame(tab_view)
        document_tab = customtkinter.CTkFrame(tab_view)

        tab_view.add("Normal")
        tab_view.add("Code Fix")
        tab_view.add("Code Gen")

        self.create_normal_tab(normal_tab)
        self.create_code_frame(code_fix_tab)
        self.code_gen_frame(code_gen_tab)

        self.layout = None
        self.set_layout()

        self.bind("<Configure>", lambda event: self.check_window_state())

        self.mainloop()

    def set_layout(self):
        wm_state = self.wm_state()
        if wm_state == "-zoomed":
            self.layout = MaximizedLayout(self)
        else:
            self.layout = NormalLayout(self)

    def check_window_state(self):
        self.set_layout()

    def create_main_frame(self, parent_tab):
        # configure main frame for normal tab
        main_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        
        # configure rows and columns of the main_frame
        parent_tab.columnconfigure(0)
        parent_tab.columnconfigure(1, weight=8)
        parent_tab.columnconfigure(2)
        parent_tab.rowconfigure(0, weight=8)
        parent_tab.rowconfigure(1)


        # configure elements in main_frame 
        txt_gpt = customtkinter.CTkTextbox(master=main_frame, wrap='word')
        txt_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
        txt_prompt = customtkinter.CTkTextbox(master=main_frame, wrap='word')
        txt_prompt.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
        lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says:")
        lbl_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
        lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:")
        lbl_prompt.grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        
        btn_chat = customtkinter.CTkButton(master=main_frame, width=20, text="Send", command=lambda: chat(txt_prompt.get(1.0, "end-1c"), "main"))
        btn_chat.grid(row=1, column=2, padx=5, pady=15, sticky='ns')

    def create_code_frame(self, parent_tab):
        # configure main frame for normal tab
        code_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
        code_frame.pack(fill='both', expand=True, padx=5, pady=5)

        
        # configure rows and columns of the code_frame
        parent_tab.columnconfigure(0)
        parent_tab.columnconfigure(1, weight=8)
        parent_tab.columnconfigure(2)
        parent_tab.rowconfigure(0, weight=4)
        parent_tab.rowconfigure(1)
        parent_tab.rowconfigure(2)

        # configure elements in code_frame
        txt_code_gpt = customtkinter.CTkTextbox(master=code_frame, wrap='word')
        txt_code_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
        txt_code = customtkinter.CTkTextbox(master=code_frame, wrap='word')
        txt_code.grid(columnspan=2, row=1, column=1, padx=5, pady=5, sticky='nsew')
        txt_error = customtkinter.CTkTextbox(master=code_frame, wrap='word')
        txt_error.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
        
        lbl_code_gpt = customtkinter.CTkLabel(master=code_frame, text="Chat Says:")
        lbl_code_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
        lbl_code_input = customtkinter.CTkLabel(master=code_frame, text="Current Code")
        lbl_code_input.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        lbl_code_error = customtkinter.CTkLabel(master=code_frame, text="Error")
        lbl_code_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        btn_code = customtkinter.CTkButton(master=code_frame, width=20, text="Send", command=lambda: chat(txt_code.get(1.0, "end-1c"), "codef"))
        # btn_code = customtkinter.CTkButton(master=code_frame, text="Send", width=20, command=lambda: code_help(""))
        btn_code.grid(row=2, column=2, pady=15, padx=5, sticky='ns')

    def code_gen_frame(self, parent_tab):
        # configure main frame for normal tab
        code_gen_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
        code_gen_frame.pack(fill='both', expand=True, padx=5, pady=5)

        
        # configure rows and columns of the code_gen_frame
        parent_tab.columnconfigure(0)
        parent_tab.columnconfigure(1, weight=8)
        parent_tab.columnconfigure(2)
        parent_tab.rowconfigure(0, weight=4)
        parent_tab.rowconfigure(1)

        txt_code_gen = customtkinter.CTkTextbox(master=code_gen_frame, wrap='word')
        txt_code_gen.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
        txt_prompt_gen = customtkinter.CTkTextbox(master=code_gen_frame, wrap='word')
        txt_prompt_gen.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        lbl_code_gen_gpt = customtkinter.CTkLabel(master=code_gen_frame, text="Chat Says:")
        lbl_code_gen_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
        lbl_code_gen_input = customtkinter.CTkLabel(master=code_gen_frame, text="Current Code")
        lbl_code_gen_input.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        btn_code_gen = customtkinter.CTkButton(master=code_gen_frame, width=20, text="Send", command=lambda: code_create(""))
        btn_code_gen.grid(row=1, column=2, padx=5, pady=15, sticky='ns')

        btn_close = customtkinter.CTkButton(app, text="Exit", command=app.destroy)
        btn_close.pack(padx=5, pady=5, side='right')

    def create_html_frame(self, parent_tab):
        html_frame = HtmlFrame(parent_tab, horizontal_scrollbar="auto")
        html_frame.pack(fill='both', expand=True, padx=5, pady=5)
    
    def chat(self, text, tab):
        # Handle chat functionality
        pass
    
    def code_create(self, text):
        # Handle code creation functionality
        pass
    
app = App()
app.mainloop()
