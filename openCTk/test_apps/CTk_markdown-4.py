# Import libraries
import os
import openai
from tkinter import *
from markdown import Markdown
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

# Create a Markdown instance
markdown_converter = Markdown()

# Function to convert Markdown to HTML
def convert_to_html(markdown_text):
    html_body = markdown_converter.convert(markdown_text)
    
    # Set the background and text color
    html_body = f'<div style="background-color: black; color: white;">{html_body}</div>'
    
    # Replace code blocks with styled code boxes
    html_body = html_body.replace('<pre><code>', '<div style="background-color: white; color: black; padding: 10px;"><code>')
    html_body = html_body.replace('</code></pre>', '</code></div>')
    
    return html_body

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
    
    # Convert chat_response to HTML
    html_response = convert_to_html(chat_response)
    
    # Open new window to display HTML content
    html_window = Toplevel(window)
    html_window.geometry("800x600")
    html_window.title("Chat Response")
    
    # Display HTML content in a scrollable text box
    lbl_html = HTMLScrolledText(html_window, html=html_response)
    lbl_html.pack(expand=True, fill='both')

# sets up text boxes for chat and input
lbl_gpt = Label(window, text="Chat says...").pack()
txt_gpt = Text(window, wrap=WORD)
txt_gpt.pack(padx=10, pady=10, expand=True, fill='both')

lbl_prompt = Label(window, text="Prompt: ").pack()
txt_prompt = Text(window, height=8, wrap=WORD)
txt_prompt.pack(fill='x', padx=10, pady=10)

# sets up chat, format, and close buttons
btn_close = Button(window, text="Close", command=window.destroy)
btn_close.pack(side=RIGHT, padx=5, pady=5)

btn_format = Button(window, text="Format", command=chat)
btn_format.pack(side=RIGHT, padx=5, pady=5)

btn_chat = Button(window, text="Send", command=lambda: update_win(""))
btn_chat.pack(side=RIGHT, padx=5, pady=5)

# handles shift + enter input to press chat button
window.bind("<Shift-Return>", lambda event: update_win(""))
window.mainloop()
