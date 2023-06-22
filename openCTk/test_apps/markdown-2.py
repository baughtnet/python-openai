# Import libraries
import os
import openai
from tkinter import *
from tkinter import messagebox
from markdown import markdown
from tkhtmlview import HTMLScrolledText

# Getting API key from environment variable
openai.api_key = os.environ.get('OPENAI_API')

# Setting up Tkinter window
window = Tk()
window.geometry("950x850")
window.title("openTkv1.0")

# Setting variable for OPENAI role
messages = [
    {"role": "user", "content": "You are a polite and helpful assistant"}
]

# Output file paths
chat_response_file = "chat_response.md"
html_response_file = "html_response.html"

# called when "chat" button is pressed. gets user input and places it in the chat window
# data is put into global variable content and then is passed to the chat() function
def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "\n")
    txt_prompt.delete('1.0', END)
    chat()

# function clears text box for input, sends prompt to gpt and then prints response in the chat window below the user input
def chat():
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" + "---------------------------------------" + "\n"
    txt_gpt.insert("end", chat_response)
    txt_gpt.see(END)

    print(chat_response)
    
    # Save chat response as .md file
    with open(chat_response_file, "w") as file:
        file.write(chat_response)

    # Convert the chat response to HTML
    html_response = markdown(chat_response)

    # Convert the code blocks to HTML
    html_response = generate_code_box(html_response)

    print(html_response)

    # Save HTML response as .html file
    with open(html_response_file, "w") as file:
        file.write(html_response)

    # Open new window to display HTML content
    def format_html():
        html_window = Toplevel(window)
        html_window.geometry("800x600")
        html_window.title("Chat Response")

        # Display HTML content in a label
        lbl_html = HTMLScrolledText(html_window, html=html_response)
        lbl_html.pack(expand=True, fill='both')

    # Format button event handler
    btn_format["command"] = format_html

def generate_code_box(html):
    lines = html.split("\n")
    in_code_flag = False
    formatted_html_lines = []
    
    for line in lines:
        if line.startswith("```"):
            line = "<pre>" + line[3:] + "</pre>"
            if in_code_flag:
                line += "</div>"
                in_code_flag = False
            else:
                line += "<div>"
                in_code_flag = True
        formatted_html_lines.append(line)
    return "\n".join(formatted_html_lines)

# sets up text boxes for chat and input
lbl_gpt = Label(window, text="Chat says...").pack()
txt_gpt = Text(window, wrap=WORD)
txt_gpt.pack(padx=10, pady=10, expand=True, fill='both')

lbl_prompt = Label(window, text="Prompt: ").pack()
txt_prompt = Text(window, height=8, wrap=WORD)
txt_prompt.pack(fill='x', padx=10, pady=10)

# sets up chat, format, and close button
btn_close = Button(window, text="Close", command=window.destroy)
btn_close.pack(side=RIGHT, padx=5, pady=5)

btn_format = Button(window, text="Format")
btn_format.pack(side=RIGHT, padx=5, pady=5)

btn_chat = Button(window, text="Send", command=lambda: update_win(""))
btn_chat.pack(side=RIGHT, padx=5, pady=5)

# handles shift + enter input to press chat button
window.bind("<Shift-Return>", lambda event: update_win(""))
window.mainloop()
