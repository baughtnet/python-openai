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

html_window = None
html_content = ""

def update_html(prompt_txt, chat_response):
    global html_content
    html_content = prompt_txt + chat_response

    if html_window and html_window.winfo_exists():  # Check if html_window exists and is open
        frame.add_html(html_content)

def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    prompt_txt = "<h3>Welcome to ChatGPT Custom</h3><br><hr><br> <h4>You say:</h4>  " + content
    txt_gpt.add_html(prompt_txt)
    # txt_gpt.add_html("<h3>Welcome to ChatGPT Custom</h3><br><hr><br> <h4>You say:</h4>  " + content)
    # update_html(prompt_txt, "")
    txt_prompt.delete('1.0', END)
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" + "---------------------------------------" + "\n"

    print(chat_response)

    html_response = markdown(chat_response)
    txt_gpt.add_html(html_response)

    update_html(prompt_txt, html_response)
    
    # try:
        # frame.add_html(html_response)
    # except Exception:
        # pass

    

    print(html_response)

    def format_html():
        global frame, html_window
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
# txt_gpt.pack(padx=11, pady=10, expand=True, fill='both')

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
