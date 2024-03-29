# import libraries
from time import sleep
import tkinter
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os
import torch
from time import sleep
from playsound import playsound as pl
from TTS.api import TTS
import speech_recognition as sr

# import openAI API key
openai.api_key = os.environ.get('OPENAI_API')

# messages = [
    # {"role": "user", "content": "You are a polite and helpful assistant"}
#]

messages = [
        {'role': "user",
         "content": "You are a polite and helpful assistant."}
]


code_messages = [
        {'role': "user",
         "content": "You are a polite and helpful coding assistant.  Your main goal is to fix code given to you, based on your knowledge and the error given to you.  Should you encounter a comment in the code and ti begins with the string 'prompt:', interepret the remaining text of the comment as a prompt from the user regarding specific output that should be generated, rather than implicit code completion.  If any changes have been made to the code, the response should end with a list of changes made."}
        ]

create_messages = [
        {'role': "user",
         "content": "You are a polite and helpful coding assistant, you are someone with years of experience accross all programming languages.  Your main goal is to create code based on information given to you by the user. Code created should be efficient, commented and a brief overview of the code given at the end of the response.  You should always ask clarifiying questions before generating code to reduce the need to debug."}
        ]

# function for handling speech checkbox
def speechbox_event():
    # speak_txt(chat_response)
    pass

def speak_txt(command):
    # setup device for torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "tts_models/en/jenny/jenny"
    tts = TTS(model_name)

    # run tts
    file = tts.tts_to_file(text=command, file='/tmp/temp.wav')
    pl(file)

# initialize the recognizer
r = sr.Recognizer()

def record_txt():
    try:
        with sr.Microphone() as source2:

            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2)
            
            text = r.recognize_google(audio2)
            txt_prompt.insert("end", text)
            # return text
    except sr.RequestError as e:
        print("Could not request results: {0}".format(e))
    except sr.UnknownValueError:
            print("An unknown error has occured!")
# chat function for sending prompt and clearing the prompt box on the normal tab
def chat(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt.delete(1.0, 'end')

    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"
    txt_gpt.insert("end", chat_response)
    txt_gpt.see('end')
    print(chat_response)

    if check_var_speech.get() == "on":
        speak_txt(chat_response)

def code_help(event):
    global codeHelp_prompt
    code = txt_code.get(1.0, "end-1c")
    error = txt_error.get(1.0, "end-1c")
    txt_code_gpt.insert("end", "You say: " + code + "\n\n" + error + "\n" + "---------------------------------------------------------------" + "\n")
    txt_code.delete(1.0, 'end')
    txt_error.delete(1.0, 'end')

    codeHelp_prompt = "I am writing a program, the code looks like this: " + "\n" + code + "The error I get looks like this:" + error + "Can you help me fix my code?"

    code_messages.append({"role": "user", "content": codeHelp_prompt})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = code_messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"
    txt_code_gpt.insert("end", chat_response)
    txt_code_gpt.see('end')
    print(chat_response)

    # checks to see whether response should be read aloud
    if check_var_speech.get() == "on":
        speak_txt(chat_response)

def code_create(event):
    global codeCreate_prompt
    code = txt_prompt_gen.get(1.0, "end-1c")
    txt_code_gen.insert("end", "You say: " + code + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt_gen.delete(1.0, 'end')
    codeCreate_prompt = code

    create_messages.append({"role": "user", "content": codeCreate_prompt})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = create_messages,
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"
    txt_code_gen.insert("end", chat_response)
    txt_code_gen.see('end')
    print(chat_response)

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

btn_chat = customtkinter.CTkButton(master=main_frame, width=20, text="Send", command=lambda: chat(""))
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

btn_code = customtkinter.CTkButton(master=code_frame, text="Send", width=20, command=lambda: code_help(""))
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

check_var_speech = tkinter.StringVar(value="off")
checkbox_speech = customtkinter.CTkCheckBox(app, text="Speech", command=speechbox_event,
                                            variable=check_var_speech, onvalue="on", offvalue="off")
checkbox_speech.pack(padx=5, pady=5, side='left')
# checkbox = customtkinter.CTkbutton(app, text="Speech", variable=checkbox_var)
# checkbox.pack(padx=5, pady=5, side='right')

btn_stt = customtkinter.CTkButton(app, text="Speech to Text", command=record_txt)
btn_stt.pack(padx=5, pady=5, side='right')

btn_close = customtkinter.CTkButton(app, text="Exit", command=app.destroy)
btn_close.pack(padx=5, pady=5, side='right')

# app.bind("<Shift-Return>", lambda event: chat(""))

# run the app
app.mainloop()
