# import libraries
from time import sleep
import customtkinter
from customtkinter.windows.widgets import appearance_mode
import openai
import os

# import openAI API key
# openai.api_key = os.environ.get('OPENAI_API')
openai.api_key = "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"
# messages = [
    # {"role": "user", "content": "You are a polite and helpful assistant"}
#]

messages = [
        {'role': "user",
         "content": "You are a polite and helpful assistant.  Please summarize ideas with bullet points where appropriate, like after a paragraph of text explaining a concept for example.  Also make use of comparisons and/or analogies where appropriate.  Your responses shouldn't come off as patronizing or condescending."}
]

# update_win function for sending prompt and clearing the prompt box
def update_win(event):
    global content
    content = txt_prompt.get(1.0, "end-1c")
    txt_gpt.insert("end", "You say:  " + content + "\n" + "---------------------------------------------------------------" + "\n")
    txt_prompt.delete(1.0, 'end')
    chat()

# chat function for adding AI response to txt_gpt text box
def chat():
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages
    )
    chat_response = "AI says: " + completion.choices[0].message.content + "\n" "\n" + "---------------------------------------------------------------" + "\n"
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
txt_gpt = customtkinter.CTkTextbox(master=main_frame)
txt_gpt.grid(columnspan=2, row=0, column=1, padx=5, pady=5, sticky='nsew')
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
