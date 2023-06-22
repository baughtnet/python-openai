import tkinter as tk
from tkinter import messagebox
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from tkinter import ttk
from tkinter.ttk import Progressbar
import os
import openai
from tkhtmlview import HTMLScrolledText
import re
from tkinter import filedialog
import webbrowser

# Getting API key from environment variable
openai.api_key = os.environ.get('OPENAI_API')

# Setting up Tkinter window
window = tk.Tk()
window.geometry("950x850")
window.title("openTkv1.0")

# Setting variable for OPENAI role
messages = [
    {"role": "user", "content": "You are a polite and helpful assistant"}
]

# called when "chat" button is pressed. gets user input and places it in the chat window
# data is put into global variable content and then is passed to the chat() function
def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "\n")
    txt_prompt.delete('1.0', tk.END)
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
    txt_gpt.see(tk.END)

    print(chat_response)

    # Convert the chat response to HTML
    html_response = markdown(chat_response)

    # Generate code block with Solarized Dark colors
    code_block = generate_code_block(html_response)

    # Display the code block
    txt_response.set_html(code_block)

    # Save the chat_response as an .md file
    save_as_md(chat_response)

    # Save the html_response as an html file
    save_as_html(html_response)

# Generate code block with Solarized Dark colors
def generate_code_block(text):
    lexer = get_lexer_by_name("python")
    formatter = HtmlFormatter(
        style="solarized-dark",
        full=True,
        cssclass="code-block"
    )
    code = highlight(text, lexer, formatter)
    return f'<pre class="{formatter.cssclass}"><code>{code}</code></pre>'

# Save the chat_response as an .md file
def save_as_md(content):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown Files", "*.md")])
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("File Saved", "Chat response saved as Markdown!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Save the html_response as an html file
def save_as_html(content):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("File Saved", "HTML response saved as HTML file!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to copy the code to clipboard
def copy_code_to_clipboard():
    code = txt_response.selection_get()
    window.clipboard_clear()
    window.clipboard_append(code)
    messagebox.showinfo("Code Copied", "Code copied to clipboard!")

# sets up text boxes for chat and input
lbl_gpt = tk.Label(window, text="Chat says...")
lbl_gpt.pack()

txt_gpt = tk.Text(window, wrap=tk.WORD)
txt_gpt.pack(padx=10, pady=10, expand=True, fill='both')

lbl_prompt = tk.Label(window, text="Prompt: ")
lbl_prompt.pack()

txt_prompt = tk.Text(window, height=8, wrap=tk.WORD)
txt_prompt.pack(fill='x', padx=10, pady=10)

# sets up chat, format, and close button
btn_close = tk.Button(window, text="Close", command=window.destroy)
btn_close.pack(side=tk.RIGHT, padx=5, pady=5)

btn_format = tk.Button(window, text="Format")
btn_format.pack(side=tk.RIGHT, padx=5, pady=5)

btn_chat = tk.Button(window, text="Send", command=lambda: update_win(""))
btn_chat.pack(side=tk.RIGHT, padx=5, pady=5)

# handles shift + enter input to press chat button
window.bind("<Shift-Return>", lambda event: update_win(""))

# Generate copy button
btn_copy_code = tk.Button(window, text="Copy Code", command=copy_code_to_clipboard)
btn_copy_code.pack(side=tk.LEFT)

# Generate ScrolledText to display HTML content
txt_response = HTMLScrolledText(window)
txt_response.pack(fill='both', padx=10, pady=10, expand=True)

# CSS for the code block
code_css = """
            .code-block {
                border: 1px solid #ccc;
                padding: 10px;
                background-color: #002b36;
                color: #839496;
                text-align: left;
                margin: 0px auto;
                width: 70%;
                overflow-x: auto;
                font-family: "Courier New", Courier, monospace;
            }
            """

# Add CSS to ScrolledText
txt_response.insert(tk.END, f'<style>{code_css}</style>')

# Start Tkinter main loop
window.mainloop()
