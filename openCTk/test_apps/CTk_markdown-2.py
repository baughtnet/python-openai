# import libraries
from time import sleep
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os
import markdown
import webbrowser

# import openAI API key
openai.api_key = os.environ.get('OPENAI_API')

# messages = [
    # {"role": "user", "content": "You are a polite and helpful assistant"}
# ]

messages = [
    {'role': "user",
     "content": "You are a polite and helpful assistant. Please summarize ideas with bullet points where appropriate, like after a paragraph of text explaining a concept, for example. Also, make use of comparisons and/or analogies where appropriate. Your responses shouldn't come off as patronizing or condescending."}
]

code_messages = [
    {'role': "user",
     "content": "You are a polite and helpful coding assistant. Your main goal is to fix code given to you, based on your knowledge and the error given to you. Should you encounter a comment in the code and it begins with the string 'prompt:', interpret the remaining text of the comment as a prompt from the user regarding specific output that should be generated, rather than implicit code completion. If any changes have been made to the code, the response should end with a list of changes made."}
]

create_messages = [
    {'role': "user",
     "content": "You are a polite and helpful coding assistant, someone with years of experience across all programming languages. Your main goal is to create code based on information given to you by the user. Code created should be efficient, commented, and have a brief overview of the code given at the end of the response. You should always ask clarifying questions before generating code to reduce the need to debug."}
]

# chat function for sending prompt and clearing the prompt box on the normal tab
def chat(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt.delete(1.0, 'end')

    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n\n" + "---------------------------------------------------------------" + "\n"
    txt_gpt.insert("end", chat_response)
    txt_gpt.see('end')
    print(chat_response)

def code_help(event):
    global codeHelp_prompt
    code = txt_code.get(1.0, "end-1c")
    error = txt_error.get(1.0, "end-1c")
    txt_code_gpt.insert("end", "You say: " + code + "\n\n" + error + "\n" + "---------------------------------------------------------------" + "\n")
    txt_code.delete(1.0, 'end')
    txt_error.delete(1.0, 'end')

    codeHelp_prompt = "I am writing a program, the code looks like this:\n" + code + "\nThe error I get looks like this:\n" + error + "\nCan you help me fix my code?"

    code_messages.append({"role": "user", "content": codeHelp_prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=code_messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n\n" + "---------------------------------------------------------------" + "\n"
    txt_code_gpt.insert("end", chat_response)
    txt_code_gpt.see('end')
    print(chat_response)

def code_create(event):
    global codeCreate_prompt
    code = txt_prompt_gen.get(1.0, "end-1c")
    txt_code_gen.insert("end", "You say: " + code + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt_gen.delete(1.0, 'end')
    codeCreate_prompt = code

    create_messages.append({"role": "user", "content": codeCreate_prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=create_messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n\n" + "---------------------------------------------------------------" + "\n"
    txt_code_gen.insert("end", chat_response)
    txt_code_gen.see('end')
    print(chat_response)

def format_window(event, chat_response):
    markdown_response = chat_response
    html_content = markdown.markdown(markdown_response)

    app_two = customtkinter.CTk()
    app_two.title("Formatted Response")

    text_widget = customtkinter.CTkTextbox(app_two)
    text_widget.insert(customtkinter.CTk.INSERT, html_content)
    text_widget.pack()

    app_two.mainloop()# Set up app appearance

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Create the app
app = customtkinter.CTk()
app.geometry("720x950")
app.title("Custom OpenAI")

# Create the tab view
tab_view = customtkinter.CTkTabview(master=app)
tab_view.pack(fill='both', expand=True, padx=5, pady=5)

# Create the tabs
normal_tab = customtkinter.CTkFrame(tab_view)
code_tab = customtkinter.CTkFrame(tab_view)
gen_tab = customtkinter.CTkFrame(tab_view)

tab_view.add("Normal", normal_tab)
tab_view.add("Code Fix", code_tab)
tab_view.add("Code Gen", gen_tab)

# configure main frame for normal tab
main_frame = customtkinter.CTkFrame(normal_tab)
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure main frame for code tab
code_frame = customtkinter.CTkFrame(code_tab)
code_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure main frame for code tab
code_gen_frame = customtkinter.CTkFrame(code_gen_frame)
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
code_gen_frame.rowconfigure(2)

# configure elements in main_frame
txt_gpt = customtkinter.CTkTextbox(master=main_frame, wrap='word')
txt_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
txt_prompt = customtkinter.CTkTextbox(master=main_frame, wrap='word')
txt_prompt.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says:")
lbl_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:")
lbl_prompt.grid(row=1, column=0, padx=5, pady=5, sticky='ne')

btn_chat = customtkinter.CTkButton(master=main_frame, width=20, text="Send", command=chat)
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
lbl_code_input = customtkinter.CTkLabel(master=code_frame, text="Current Code:")
lbl_code_input.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
lbl_code_error = customtkinter.CTkLabel(master=code_frame, text="Error:")
lbl_code_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

btn_code = customtkinter.CTkButton(master=code_frame, text="Send", width=20, command=code_help)
btn_code.grid(row=2, column=2, pady=15, padx=5, sticky='ns')

# configure elements in code_gen_frame
txt_code_gen = customtkinter.CTkTextbox(master=code_gen_frame, wrap='word')
txt_code_gen.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
txt_prompt_gen = customtkinter.CTkTextbox(master=code_gen_frame, wrap='word')
txt_prompt_gen.grid(rowspan=2, row=1, column=1, padx=5, pady=5, sticky='nsew')

lbl_code_gen_gpt = customtkinter.CTkLabel(master=code_gen_frame, text="Chat Says:")
lbl_code_gen_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
lbl_code_gen_input = customtkinter.CTkLabel(master=code_gen_frame, text="Current Code:")
lbl_code_gen_input.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

btn_code_gen = customtkinter.CTkButton(master=code_gen_frame, width=20, text="Send", command=code_create)
btn_code_gen.grid(row=1, column=2, padx=5, pady=15, sticky='nsew')

btn_gen_mark = customtkinter.CTkButton(master=code_gen_frame, width=20, text="Format", command=format_window)
btn_gen_mark.grid(row=2, column=2, padx=5, pady=15, sticky='nsew')

# exit button
btn_close = customtkinter.CTkButton(app, text="Exit", command=app.destroy)
btn_close.pack(padx=5, pady=5, side='right')

# run the app
app.mainloop()
