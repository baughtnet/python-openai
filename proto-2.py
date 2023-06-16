# import libraries
import customtkinter

# set up app appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# create the app 
app = customtkinter.CTk()
app.geometry("720x720")
app.title("Custom OpenAI")

# create the tab view
tab = customtkinter.CTkTabview(master=app)
tab.pack(fill='both', expand=True, padx=5, pady=5)

# create the Normal, Code, and Document tabs
normal_tab = customtkinter.CTkFrame(tab)
code_tab = customtkinter.CTkFrame(tab)
document_tab = customtkinter.CTkFrame(tab)

tab.add("Normal")
tab.add("Code")
tab.add("Document")

# create a main frame for the Normal tab
main_frame = customtkinter.CTkFrame(tab.tab("Normal"))
main_frame.pack(fill='both', expand=True, padx=5, pady=5)

# create a grid layout for the main frame
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=4)
main_frame.rowconfigure(1, weight=1)

# "Chat says..." label
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says...")
lbl_gpt.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

# Large textbox for txt_gpt
txt_gpt = customtkinter.CTkTextbox(master=main_frame, wrap='word')
txt_gpt.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

# "Prompt:" label
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:")
lbl_prompt.grid(row=1, column=0, padx=5, pady=(5,2), sticky='nw')

# Smaller textbox for txt_prompt
txt_prompt = customtkinter.CTkTextbox(master=main_frame, height=20, wrap='word')
txt_prompt.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')

# Send button
btn_chat = customtkinter.CTkButton(main_frame, text="Send", command=lambda: update_win(""))
btn_chat.grid(row=1, column=2, padx=5, pady=5, sticky='ne')

# "Chat says..." label on the left, "Prompt:" label on the right
# Set the remaining column width to half of the first two columns
main_frame.columnconfigure(3, weight=1)
lbl_gpt.grid(sticky='nw', row=0, column=0, padx=5, pady=5)
lbl_prompt.grid(sticky='nw', row=1, column=0, padx=5, pady=(5,2))

# Close button
btn_close = customtkinter.CTkButton(app, text="Close", command=app.destroy)
btn_close.pack(side='right', padx=5, pady=5)

app.mainloop()
