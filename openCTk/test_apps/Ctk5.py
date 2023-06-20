# import libraries
import customtkinter
import openai
import os

# Set OpenAI API key
openai.api_key = os.environ.get('OPENAI_API')

# Initialize messages list
messages = [{"role": "user", "content": "You are a polite and helpful assistant"}]

# Define the function to update the window
def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt.delete(1.0, 'end')
    chat()

# Define the function to perform the chat with OpenAI
def chat():
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" + "\n" + "---------------------------------------------------------------" + "\n"
    txt_gpt.insert("end", chat_response)
    txt_gpt.see('end')
    print(chat_response)

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

btn_frame = customtkinter.CTkFrame(app)
btn_frame.place(relx=1, rely=1, anchor='se', relwidth=1.0, relheight=0.05)

# Create a main frame for the Normal tab
main_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# Configure rows and columns of the main frame
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=8)
main_frame.rowconfigure(0, weight=4)
main_frame.rowconfigure(1, weight=1)

# Create the frame for the textboxes
text_frame = customtkinter.CTkFrame(master=main_frame)
text_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=1)
text_frame.rowconfigure(1, weight=1)

# Create the large textbox for txt_gpt
txt_gpt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_gpt.grid(row=0, column=0, sticky='nsew')

# Create the smaller frame for prompt and chat button
prompt_frame = customtkinter.CTkFrame(master=text_frame)
prompt_frame.grid(row=1, column=0, sticky='nsew')
prompt_frame.columnconfigure(0, weight=1)
prompt_frame.columnconfigure(1, weight=0)

# Create the smaller textbox for prompt
txt_prompt = customtkinter.CTkTextbox(master=prompt_frame, wrap='word')
txt_prompt.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Create the send button
btn_chat = customtkinter.CTkButton(prompt_frame, text="Send", command=lambda: update_win(""))
btn_chat.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

# Create the "Chat says..." label
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says...", height=1)
lbl_gpt.grid(row=0, column=0, padx=10, pady=30, sticky='ne')

# Create the "Prompt:" label
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:", height=1)
lbl_prompt.grid(row=1, column=0, padx=10, pady=(5, 2), sticky='ne')

# Create the close button
btn_close = customtkinter.CTkButton(btn_frame, text="Close", command=app.destroy)
btn_close.pack(padx=5, pady=5)

# Bind the Shift+Return keystroke to the update_win function
app.bind("<Shift-Return>", lambda event: update_win(""))

# Run the app
app.mainloop()
