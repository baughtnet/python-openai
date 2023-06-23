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
tab.pack(fill='both', expand=True, padx=10, pady=10)

normal_tab = customtkinter.CTkFrame(tab)
code_tab = customtkinter.CTkFrame(tab)
document_tab = customtkinter.CTkFrame(tab)

tab.add("Normal")
tab.add("Code")
tab.add("Document")

lbl_gpt = customtkinter.CTkLabel(app, text="Chat says...").pack()
txt_gpt = customtkinter.CTkTextbox(app, wrap='word')
txt_gpt.pack(padx=10, pady=10, expand=True, fill='both')

lbl_prompt = customtkinter.CTkLabel(app, text="Prompt: ").pack()
txt_prompt = customtkinter.CTkTextbox(app, height = 4.5, wrap='word')
txt_prompt.pack(fill='x', padx=10, pady=10)

btn_close = customtkinter.CTkButton(app, text="Close", command=app.destroy)
btn_close.pack(side='right', padx=5, pady=5)

btn_chat = customtkinter.CTkButton(app, text="Send", command=lambda: update_win(""))
btn_chat.pack(side='right', padx=5, pady=5)

app.mainloop()