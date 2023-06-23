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

# "Chat says..." label
lbl_gpt = customtkinter.CTkLabel(master=main_frame, text="Chat says...")
lbl_gpt.pack(fill='x', padx=5, pady=5)

# Create a frame for the textboxes
text_frame = customtkinter.CTkFrame(master=main_frame)
text_frame.pack(fill='both', expand=True, padx=5, pady=5)

# Large textbox for txt_gpt
txt_gpt = customtkinter.CTkTextbox(master=text_frame, wrap='word')
txt_gpt.pack(fill='both', expand=True, pady=(0,5))

# "Prompt:" label
lbl_prompt = customtkinter.CTkLabel(master=main_frame, text="Prompt:")
lbl_prompt.pack(side='left', padx=5, pady=(5,2))

# Smaller textbox for txt_prompt
txt_prompt = customtkinter.CTkTextbox(master=main_frame, height=6, wrap='word')
txt_prompt.pack(fill='both', expand=True, pady=5)

# Send button
btn_chat = customtkinter.CTkButton(main_frame, text="Send", command=lambda: update_win(""))
btn_chat.pack(side='right', padx=5, pady=5, ipady=20)

# "Chat says..." label on the left, "Prompt:" label on the right
lbl_gpt.pack(side='left', padx=5)

btn_close = customtkinter.CTkButton(app, text="Close", command=app.destroy)
btn_close.pack(side='right', padx=5, pady=5)

app.mainloop()
