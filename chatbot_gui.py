import tkinter as tk
from tkinter import ttk
from evaluation import chatbot_response


class ChatbotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IPO Chatbot")
        self.geometry("400x500")
        self.resizable(width=False, height=False)
        self.create_widgets()

    def create_widgets(self):
        self.chatlog = tk.Text(self, bd=0, bg="white", height="8", width="50", font="Arial", )
        self.chatlog.config(state=tk.DISABLED)
        self.scrollbar = tk.Scrollbar(self, command=self.chatlog.yview, cursor="heart")
        self.chatlog['yscrollcommand'] = self.scrollbar.set
        self.send_button = tk.Button(self, font=("Verdana",12,"bold"), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b", fg="#ffffff", command=self.send)
        self.entry_box = tk.Text(self, bd=0, bg="white", width="29", height="5", font="Arial")
        self.scrollbar.place(x=376, y=6, height=386)
        self.chatlog.place(x=6, y=6, height=386, width=370)
        self.entry_box.place(x=128, y=401, height=90, width=265)
        self.send_button.place(x=6, y=401, height=90)

    def send(self):
        msg = self.entry_box.get("1.0", "end-1c").strip()
        self.entry_box.delete("0.0", tk.END)
        if msg != '':
            self.chatlog.config(state=tk.NORMAL)
            self.chatlog.insert(tk.END, "You: " + msg + '\n\n')
            self.chatlog.config(foreground="#442265", font=("verdana", 12))
            res = chatbot_response(msg)
            self.chatlog.insert(tk.END, "IPO: " + res + '\n\n')
            self.chatlog.config(state=tk.DISABLED)
            self.chatlog.yview(tk.END)


if __name__ == "__main__":
    app = ChatbotGUI()
    app.mainloop()