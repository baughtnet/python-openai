# import libraries
import markdown
import tkinter as tk
from tkhtmlview import HTMLLabel, HTMLText, RenderHTML
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os

global gpt_html

# import openAI API key
openai.api_key = os.environ.get('OPENAI_API')
# messages = [
    # {"role": "user", "content": "You are a polite and helpful assistant"}
#]

messages = [
        {'role': "user",
         "content": "You are a polite and helpful assistant.  Please summarize ideas with bullet points where appropriate, like after a paragraph of text explaining a concept for example.  Also make use of comparisons and/or analogies where appropriate.  I remember these are suggestions, do not over use the suggested ideas in the last few sentences, only where it would make sense to do so.  Finally, your responses shouldn't come off as patronizing or condescending."}
]

# update_win function for sending prompt and clearing the prompt box
def update_win(event):
    global content
    global gpt_html
    gpt_html = "<h2>welcome to chatGPT baughtnet edition</h2><br>"
    content = txt_prompt.get(1.0, "end-1c")
    gpt_html = gpt_html + content
    # txt_gpt.insert("end", "You say:  " + content + "\n" + "---------------------------------------------------------------" + "\n")
    # txt_prompt.delete(1.0, 'end')
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"
    # parse with markdown to format into HTML document
    html_response = markdown.markdown(chat_response)

    html_response = html_response.replace('<pre><code>', '<pre><code class="code-block">')
    html_response = html_response.replace('<pre><code class="code-block">', '<pre class="code-block-wrapper"><code class="code-block">')
    html_response = html_response.replace('</code></pre>', '</code></pre><button class="copy-button">Copy</button>')
    gpt_html = gpt_html + html_response
    html_gpt = HTMLText(main_frame, html=gpt_html)
    html_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
    # txt_gpt.insert("end", html_response)
    # txt_gpt.see('end')
    print(chat_response)
    print(gpt_html)

# Set up app appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Create the app
app = customtkinter.CTk()
app.geometry("720x720")
app.title("Custom OpenAI")

# Create the tab view
tab_view = customtkinter.CTkTabview(master=app)
tab_view.pack(fill='both', expand=True, padx=5, pady=5)

# Create the tabs
normal_tab = customtkinter.CTkFrame(tab_view)
code_tab = customtkinter.CTkFrame(tab_view)
document_tab = customtkinter.CTkFrame(tab_view)

tab_view.add("Normal")
tab_view.add("Code")
tab_view.add("Document")

# btn_frame = customtkinter.CTkFrame(app)
# btn_frame.grid(padx=5, pady=5, sticky='se')

main_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# configure rows and columns of the main_frame
main_frame.columnconfigure(0)
main_frame.columnconfigure(1, weight=8)
main_frame.columnconfigure(2)
main_frame.rowconfigure(0, weight=8)
main_frame.rowconfigure(1)

# text boxes for input and response
# txt_gpt = customtkinter.CTkTextbox(master=main_frame)
# txt_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
# html_gpt = HTMLText(main_frame, html=gpt_html)
# html_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
txt_prompt = customtkinter.CTkTextbox(master=main_frame)
txt_prompt.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

# labels for prompt and chat says
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says:")
lbl_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='ne')
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:")
lbl_prompt.grid(row=1, column=0, padx=5, pady=5, sticky='ne')

# buttons
btn_chat = customtkinter.CTkButton(master=main_frame, width=20, text="Send", command=lambda: update_win(""))
btn_chat.grid(row=1, column=2, padx=5, pady=15, sticky='ns')

btn_close = customtkinter.CTkButton(app, text="Exit", command=app.destroy)
btn_close.pack(padx=5, pady=5, side='right')

app.bind("<Shift-Return>", lambda event: update_win(""))

# run the app
app.mainloop()
