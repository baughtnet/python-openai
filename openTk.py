import os
import openai
from tkinter import *
from tkinter import messagebox

# api_key = os.environ.get('OPENAI_API')
openai.api_key = os.environ.get('OPENAI_API')

window = Tk()
window.geometry("1024x450")
window.title("openTkv1.0")


messages = [
    {"role": "user", "content": "You are a polite and helpful assistant"}
]

def update_win():
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", content + "\n" + "\n")
    chat()

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

lbl_gpt = Label(window, text="Chat says...").pack()
txt_gpt = Text(window, height = 15, width = 125)
txt_gpt.pack()

lbl_prompt = Label(window, text="Prompt: ").pack()
txt_prompt = Text(window, height = 3, width = 125)
txt_prompt.pack()

btn_chat = Button(window, text="Send", command=update_win)
btn_chat.pack()

btn_close = Button(window, text="Close", command=window.destroy)
btn_close.pack()

window.mainloop()

    #messages.append({"role": "user", "content": content})
#
    #completion = openai.ChatCompletion.create(
      #model="gpt-3.5-turbo",
      #messages=messages
    #)
#
    #chat_response = completion.choices[0].message.content
#
    #print(completion.choices[0].message.content)
