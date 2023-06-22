import os
import openai
from tkinter import *
from tkinter import messagebox
from markdown import markdown
from tkinterweb import HtmlFrame

openai.api_key = os.environ.get('OPENAI_API')

window = Tk()
window.geometry("950x850")
window.title("openTkv1.0")

messages = [
    {"role": "user", "content": "You are a polite and helpful assistant"}
]

def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    html_response = "<h2>Welcome to ChatGPT Custom</h2><br><hr><br>"
    txt_gpt.add_html("You say:  " + content)
    txt_prompt.delete('1.0', END)
    chat()

def chat():
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" + "---------------------------------------" + "\n"
    # txt_gpt.insert("end", chat_response)
    # txt_gpt.see(END)

    print(chat_response)

    html_response = markdown(chat_response)
    txt_gpt.add_html(html_response)

    print(html_response)

    def format_html():
        html_window = Toplevel(window)
        html_window.geometry("800x600")
        html_window.title("Chat Response")

        frame = HtmlFrame(html_window)
        frame.load_html(html_response)
        frame.pack(fill="both", expand=True)

    btn_format["command"] = format_html

lbl_gpt = Label(window, text="Chat says...").pack()
txt_gpt = HtmlFrame(window)
txt_gpt.pack(fill='both', expand=True)
# txt_gpt = Text(window, wrap=WORD)
# txt_gpt.pack(padx=10, pady=10, expand=True, fill='both')

lbl_prompt = Label(window, text="Prompt: ").pack()
txt_prompt = Text(window, height=8, wrap=WORD)
txt_prompt.pack(fill='x', padx=10, pady=10)

btn_close = Button(window, text="Close", command=window.destroy)
btn_close.pack(side=RIGHT, padx=5, pady=5)

btn_format = Button(window, text="Format")
btn_format.pack(side=RIGHT, padx=5, pady=5)

btn_chat = Button(window, text="Send", command=lambda: update_win(""))
btn_chat.pack(side=RIGHT, padx=5, pady=5)

window.bind("<Shift-Return>", lambda event: update_win(""))
window.mainloop()
