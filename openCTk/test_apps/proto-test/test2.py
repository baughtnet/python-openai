# import libraries
import customtkinter

# set up app appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# app app
app = customtkinter.CTk()
app.geometry("720x720")
app.title("Custom OpenAI")

tab = customtkinter.CTkTabview(master=app)
tab.pack(fill='both', expand=True, padx=5, pady=5)

normal_tab = customtkinter.CTkFrame(tab)
code_tab = customtkinter.CTkFrame(tab)
document_tab = customtkinter.CTkFrame(tab)

tab.add("Normal")
tab.add("Code")
tab.add("Document")

# Create a main frame for the Normal tab
main_frame = customtkinter.CTkFrame(tab.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# Configure rows and columns of the main frame
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.rowconfigure(0, weight=8)
main_frame.rowconfigure(1, weight=2)

# Create a frame for the textboxes
text_frame = customtkinter.CTkFrame(master=main_frame)
text_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=8)
text_frame.rowconfigure(1, weight=2)  # Updated row weight for txt_prompt

# Large textbox for txt_gpt
txt_gpt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_gpt.grid(row=0, column=0, padx=5, pady=(0,5), sticky='nsew')

# "Prompt:" label
lbl_prompt = customtkinter.CTkLabel(master=text_frame, text="Prompt:", height=1)
lbl_prompt.grid(row=1, column=0, padx=5, pady=(5,2), sticky='w')

# Smaller textbox for txt_prompt
txt_prompt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_prompt.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# "Chat says..." label
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says...", height=1)
lbl_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Send button
btn_chat = customtkinter.CTkButton(main_frame, text="Send", command=lambda: update_win(""))
btn_chat.grid(row=1, column=1, padx=5, pady=5, sticky='se')

btn_close = customtkinter.CTkButton(app, text="Close", command=app.destroy)
btn_close.pack(side='right', padx=5, pady=5)

app.mainloop()