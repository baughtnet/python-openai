# import libraries
from time import sleep
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os

# import openAI API key
openai.api_key = os.environ.get('OPENAI_API')

# prompt for normal tab
messages = [
        {'role': "user",
         "content": "You are a polite and helpful assistant.  Please summarize ideas with bullet points where appropriate, like after a paragraph of text explaining a concept for example.  Also make use of comparisons and/or analogies where appropriate.  Your responses shouldn't come off as patronizing or condescending."}
]

def get_response(prompt):
    global chat_response
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"

    print(chat_response)
    return chat_response

def update_win(target, content):
    print(target)
    print(content)
    if target == "main":
        txt_gpt.insert("end", content)
    elif target == "codef":
        txt_code_gpt.insert("end", content)
    elif target == "codeg":
        txt_code_gen.insert("end", content)

def chat(prompt, target):
    prompt = "You say:  " + prompt + "\n\n"
    
    if target == "main":
        txt_prompt.delete(1.0, "end")
        update_win(target, prompt)
    elif target == "codef":
        error = txt_error.get(1.0, "end-1c")
        prompt = prompt + "  " + error
        txt_code_gpt.delete(1.0, "end")
    elif target == "codeg":
        txt_code_gen.delete(1.0, "end")

    get_response(prompt)
    update_win(target, chat_response)

# Set up app appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Create the app
app = customtkinter.CTk()
app.geometry("800x600")
app.title("Custom OpenAI")

# Create the tab view
tab_view = customtkinter.CTkTabview(master=app)
tab_view.pack(fill='both', expand=True, padx=5, pady=5)

# Create the tabs
normal_tab = customtkinter.CTkFrame(tab_view)
code_tab = customtkinter.CTkFrame(tab_view)
document_tab = customtkinter.CTkFrame(tab_view)

tab_view.add("Normal")
tab_view.add("Code Fix")
tab_view.add("Code Gen")

# configure main frame for normal tab
main_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure main frame for code tab
code_frame = customtkinter.CTkFrame(tab_view.tab("Code Fix"))
code_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure main frame for code tab
code_gen_frame = customtkinter.CTkFrame(tab_view.tab("Code Gen"))
code_gen_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure rows and columns of the main_frame
main_frame.columnconfigure(0)
main_frame.columnconfigure(1, weight=8)
main_frame.columnconfigure(2)
main_frame.rowconfigure(0, weight=8)
main_frame.rowconfigure(1)

# configure rows and columns of the code_frame
code_frame.columnconfigure(0)
code_frame.columnconfigure(1, weight=8)
code_frame.columnconfigure(2)
code_frame.rowconfigure(0, weight=4)
code_frame.rowconfigure(1)
code_frame.rowconfigure(2)

# configure rows and columns of the code_gen_frame
code_gen_frame.columnconfigure(0)
code_gen_frame.columnconfigure(1, weight=8)
code_gen_frame.columnconfigure(2)
code_gen_frame.rowconfigure(0, weight=4)
code_gen_frame.rowconfigure(1)

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

# configure elements in code_gen_frame
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

# app.bind("<Shift-Return>", lambda event: chat(""))

# run the app
app.mainloop()
