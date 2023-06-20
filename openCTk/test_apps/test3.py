import customtkinter

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

# Create a main frame for the Normal tab
main_frame = customtkinter.CTkFrame(tab_view.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# Configure rows and columns of the main frame
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=6)
main_frame.rowconfigure(0, weight=4)
main_frame.rowconfigure(1, weight=1)


# Create a frame for the textboxes
text_frame = customtkinter.CTkFrame(master=main_frame)
text_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
text_frame.columnconfigure(0, weight=1)
text_frame.rowconfigure(0, weight=8)
text_frame.rowconfigure(1, weight=2)

# Create the large textbox for txt_gpt
txt_gpt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Create the smaller textbox for txt_prompt
txt_prompt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_prompt.grid(row=1, column=0, padx=5, pady=(0,5), sticky='nsew')

# Create the "Chat says..." label
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says...", height=1)
lbl_gpt.grid(row=0, column=0, padx=10, pady=30, sticky='ne')

# Create the "Prompt:" label
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:", height=1)
lbl_prompt.grid(row=1, column=0, padx=10, pady=(5,2), sticky='ne')

# Create the send button
btn_chat = customtkinter.CTkButton(text_frame, text="Send", command=lambda: update_win(""))
btn_chat.grid(row=1, column=0, padx=5, pady=5, sticky='se')

# Create the close button
btn_close = customtkinter.CTkButton(app, text="Close", command=app.destroy)
btn_close.pack(side='right', padx=5, pady=5)

# Calculate the 80/20 split for the textboxes
total_height = app.winfo_screenheight()
txt_gpt_height = int(total_height * 0.8)
txt_prompt_height = int(total_height * 0.2)

# Set the height of the textboxes
txt_gpt.configure(height=txt_gpt_height)
txt_prompt.configure(height=txt_prompt_height)

# Run the app
app.mainloop()