import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox
import clipboard

class App:
    def __init__(self, master):
        self.master = master
        self.text = scrolledtext.ScrolledText(master, wrap="word")
        self.text.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.copy_button = tk.Button(master, text="Copy", command=self.copy_text)
        self.copy_button.pack(pady=10)
        
        # Create a tag for code blocks
        self.text.tag_configure("code", font="Courier 10", background="#f1f1f1")
        
        # Example response from the openai API
        response = """# Hello, world

This is some **bold** text and some `code`.

```
for i in range(10):
    print(i)
```
"""
        # Insert the response with the code block tag
        self.text.insert(tk.END, response)
        self.text.tag_add("code", "5.5", "10.14")
        self.text.tag_add("code", "12.1", "15.1")
        
    def copy_text(self):
        # Get the selected text
        selection = self.text.get("sel.first", "sel.last")
        
        # Copy the selected text to the clipboard
        clipboard.copy(selection)
        
        # Show a message box to confirm the copy
        messagebox.showinfo("Copied", "Text copied to clipboard")

root = tk.Tk()
app = App(root)
root.mainloop()
