import tkinter as tk
import asyncio
from evaluation import chatbot_response


class ChatbotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IPO Chatbot")
        self.geometry("400x500")
        self.resizable(width=False, height=False)
        self.iconbitmap("ipo-small-logo.ico")
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.chatlog = tk.Text(self, width=40, bd=0, bg="white", font="Arial")
        self.chatlog.config(state=tk.DISABLED)
        self.scrollbar = tk.Scrollbar(self, width=20, command=self.chatlog.yview)
        self.chatlog['yscrollcommand'] = self.scrollbar.set
        self.send_button = tk.Button(self, font=("Verdana",12,"bold"), text="Send", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b", fg="#ffffff", command=self.send)
        self.entry_box = tk.Text(self, bd=0, bg="white", font="Arial", height=5, width=30)
        self.chatlog.grid(row=1, column=1, columnspan=2, sticky="EW")
        self.scrollbar.grid(row=1, column=3, sticky="NSW")
        self.entry_box.grid(row=2, column=1, sticky="EW")
        self.send_button.grid(row=2, column=2, sticky="EW", columnspan=2)
        self.bind('<Return>', self.send)

    def send(self, event=None):
        msg = self.entry_box.get("1.0", "end-1c").strip()
        self.entry_box.delete("0.0", tk.END)
        if msg != '':
            self.chatlog.config(state=tk.NORMAL)
            self.chatlog.insert(tk.END, "You: " + msg + '\n\n')
            self.chatlog.config(foreground="#442265", font=("verdana", 12))
            asyncio.run(self.get_response(msg))

    async def get_response(self, msg):
        self.update_idletasks()
        res = await chatbot_response(msg)
        self.chatlog.insert(tk.END, "IPO: " + res + '\n\n')
        self.chatlog.config(state=tk.DISABLED)
        self.chatlog.yview(tk.END)


if __name__ == "__main__":
    app = ChatbotGUI()
    app.mainloop()