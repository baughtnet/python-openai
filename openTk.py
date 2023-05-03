# Import libraries
import os
import openai
from tkinter import *
from tkinter import messagebox

# Getting API key from environment variable
openai.api_key = os.environ.get('OPENAI_API')

# Setting up Tkinter window
window = Tk()
window.geometry("1024x450")
window.title("openTkv1.0")

# Setting variable for OPENAI role
messages = [
    {"role": "user", "content": "You are a polite and helpful assistant"}
]

# called when "chat" button is pressed.  gets user input and places it in the chat window
# data is put into global variable content and then is passed to the chat() function
def update_win():
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", content + "\n" + "\n")
    chat()

# function clears text box for input, sends prompt to gpt and then prints response in the chat window below the user input  
def chat():
#    print("You pressed the chat button!")
#    content = txt_prompt.get(1.0, "end-1c")
#    txt_gpt.insert("end", content + "\n" +"\n")
    txt_prompt.delete('1.0', END)
    txt_gpt.pack()

    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" + "\n"
    txt_gpt.insert("end", chat_response)
    txt_gpt.pack()
    print(chat_response)


# sets up textboxes for chat and input
lbl_gpt = Label(window, text="Chat says...").pack()
txt_gpt = Text(window, height = 15, width = 125)
txt_gpt.pack()

lbl_prompt = Label(window, text="Prompt: ").pack()
txt_prompt = Text(window, height = 3, width = 125)
txt_prompt.pack()

# sets up chat and close button
btn_chat = Button(window, text="Send", command=update_win)
btn_chat.pack()

btn_close = Button(window, text="Close", command=window.destroy)
btn_close.pack()

window.mainloop()
