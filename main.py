import json
import time
import webbrowser
from dataclasses import dataclass
from threading import Thread
from tkinter import messagebox

import customtkinter as ctk
import pyperclip
from PIL import Image

import connector


@dataclass
class Theme:
    fg_color: str
    bg_color: str
    hover_color: str
    chat_bg_color: str
    chat_fg_color: str


# Global
runner = True
running = False
connection = connector.Network()
username = ''
chat = ''
translate_server_code = {
    "accepted": "Duyệt",
    "rejected": "Từ chối",
    "toolong": "Username quá dài",
    "tooshort": "Username phải có ít nhất 3 kí tự",
    "baduni": "Username không được chứa kí tự đặc biệt (chỉ được a-zA-Z và 0-9)",
    "alruser": "Username đã tồn tại",
    "roomnotfound": "Không tìm thấy phòng",
    "infonotreachable": "Không đủ thông tin",
    "boardcast": "Thông báo",
    "message": "Tin nhắn",
    "unknown": "Không rõ"
}


def load_server() -> None:
    connection.set_host("")
    connection.set_port()


load_server()

dark_theme = Theme(fg_color="grey14", bg_color="grey21", hover_color="grey35", chat_bg_color="grey25",
                   chat_fg_color="#1F6AA5")
_current_theme = dark_theme
ctk.set_appearance_mode("dark")


def profile_link():
    webbrowser.open("https://www.facebook.com/notchapple1703")
    webbrowser.open("https://www.facebook.com/py.hacker.hieu")


class Home(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Da lô giả cầy")
        self.geometry("550x350")
        self.resizable(False, False)
        self.iconbitmap("assets/chat_icon.ico")

        self.bind("<1>", lambda event: event.widget.focus_set())
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, width=400, height=100, text="Da lô giả cầy", font=("Arial", 30, "bold"),
                                  image=ctk.CTkImage(Image.open("assets/chat_icon.png"), size=(100, 100)),
                                  compound="left")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, width=400, height=50, placeholder_text="Username", font=("Arial", 15, "bold"))
        self.entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.host_button = ctk.CTkButton(self, width=150, height=50, text="Host", font=("Arial", 15, "bold"),
                                         command=self.host)
        self.host_button.grid(row=2, column=0, padx=30, pady=20, sticky="e")

        self.join_button = ctk.CTkButton(self, width=150, height=50, text="Join", font=("Arial", 15, "bold"),
                                         command=self.id_inp)
        self.join_button.grid(row=2, column=1, padx=30, pady=20, sticky="w")

        self.credit = ctk.CTkButton(self, height=25, text="Notch Apple   -   MHP", font=("Arial", 12),
                                    fg_color=_current_theme.fg_color, hover_color=_current_theme.hover_color,
                                    command=profile_link)
        self.credit.grid(row=3, column=0, columnspan=2, padx=10, pady=35, sticky="se")

    def id_inp(self):
        id = ctk.CTkInputDialog(text="ID:", title="Join")
        self.join(id.get_input())
        id.destroy()

    def host(self):
        global chat, username
        connection.flush()
        connection.connect()
        _usn = self.entry.get()
        rest = connection.send(json.dumps({"username": _usn, "icr": 1}).encode('utf-8'))
        if rest:
            try:
                roomid = rest['roomid']
            except:
                try:
                    errorcode = rest['status']
                    if not errorcode:
                        errorcode = 'unknown'
                except:
                    errorcode = "unknown"
                messagebox.showerror("Error", "Không thể tạo phòng, mã lỗi: " + translate_server_code[errorcode])
                connection.flush()
                return
            self.destroy()
            chat = ChatRoom(roomid)
            username = _usn
            chat.add_bcs(str(username) + " created the group.")
            chat.mainloop()
        else:
            try:
                errorcode = rest['status']
                if not errorcode:
                    errorcode = 'unknown'
            except:
                errorcode = "unknown"
            messagebox.showerror("Error", "Không thể tạo phòng, mã lỗi: " + translate_server_code[errorcode])
            connection.flush()
            return

    def join(self, _roomid):
        global chat, username
        connection.flush()
        connection.connect()
        _usn = self.entry.get()
        rest = connection.send(json.dumps({"username": _usn, "icr": 0, "roomid": _roomid}).encode('utf-8'))
        if rest:
            try:
                roomid = rest['roomid']
            except:
                try:
                    errorcode = rest['status']
                    if not errorcode:
                        errorcode = 'unknown'
                except:
                    errorcode = "unknown"
                messagebox.showerror("Error", "Không tìm thấy phòng, mã lỗi: " + translate_server_code[errorcode])
                connection.flush()
                return
            self.destroy()
            chat = ChatRoom(roomid)
            username = _usn
            chat.add_bcs(str(username) + " joined the group.")
            chat.mainloop()
        else:
            try:
                errorcode = rest['status']
                if not errorcode:
                    errorcode = 'unknown'
            except:
                errorcode = "unknown"
            messagebox.showerror("Error", "Không tìm thấy phòng, mã lỗi: " + translate_server_code[errorcode])
            connection.flush()
            return


class ChatRoom(ctk.CTk):
    def __init__(self, roomid):
        global running
        super().__init__()
        self.roomid = roomid
        self.title("Da lô giả cầy")
        self.geometry("700x500")
        self.resizable(False, False)
        self.iconbitmap("assets/chat_icon.ico")
        self.protocol("WM_DELETE_WINDOW", lambda: self.close())
        self.bind("<1>", lambda event: event.widget.focus_set())
        self.grid_columnconfigure(0, weight=1)

        ##################################################

        self.room_id = ctk.CTkButton(self, width=100, height=40, text="Room ID: " + roomid, font=("Arial", 15, "bold"),
                                     fg_color=_current_theme.fg_color, bg_color=_current_theme.fg_color, hover_color=_current_theme.hover_color,
                                     command=self.copyroomid)
        self.room_id.grid(row=0, column=0, padx=40, sticky="w")

        self.credit = ctk.CTkButton(self, height=25, text="Notch Apple   -   MHP", font=("Arial", 12), fg_color=_current_theme.fg_color, hover_color=_current_theme.hover_color, command=profile_link)
        self.credit.grid(row=0, column=0, padx=40, pady=10, sticky="se")

        ##################################################

        self.chat_frame = ctk.CTkScrollableFrame(self, width=600, height=350, bg_color=_current_theme.fg_color)
        self.chat_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.msg_entry = ctk.CTkTextbox(self, width=625, height=50, border_width=2, border_color=None,
                                        fg_color=_current_theme.bg_color,
                                        bg_color=_current_theme.fg_color,
                                        font=("Arial", 15, "bold"))
        self.msg_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.msg_entry.bind("<Shift-Return>", self.send_msg)

        self.send_button = ctk.CTkButton(self, width=30, height=30, text="", font=("Arial", 15, "bold"),
                                         image=ctk.CTkImage(Image.open("assets/send-message.png"), size=(30, 30)),
                                         fg_color=_current_theme.bg_color, bg_color=_current_theme.bg_color,
                                         hover_color=_current_theme.hover_color,
                                         command=self.send_msg)
        self.send_button.grid(row=2, column=0, columnspan=2, padx=45, pady=10, sticky="e")
        running = True
    def close(self, event=None):
        global running, chat, username
        # Refresh all the thing
        running = False
        username = ''
        chat = ''
        connection.flush()
        self.destroy()
        Home().mainloop()

    def copyroomid(self):
        pyperclip.copy(self.roomid)
        return True

    def send_msg(self, event=None):
        connection.client.send(
            json.dumps({"status": "send", "message": self.msg_entry.get('0.0', 'end')}).encode('utf-8'))
        self.msg_entry.delete('0.0', "end")

    def add_msg(self, msg, lorr):
        if not lorr:
            _temp = ctk.CTkLabel(self.chat_frame, text=msg, font=("Arial", 15, "bold"),
                                 fg_color=_current_theme.chat_bg_color, corner_radius=10, wraplength=250,
                                 justify="left")
            _temp.pack(padx=10, pady=5, ipady=5, anchor="w")
        else:
            _temp = ctk.CTkLabel(self.chat_frame, text=msg, font=("Arial", 15, "bold"),
                                 fg_color=_current_theme.chat_fg_color,
                                 corner_radius=10, wraplength=250, justify="left")
            _temp.pack(padx=10, pady=5, ipady=5, anchor="e")
        self.chat_frame._parent_canvas.yview_moveto(2)

    def add_bcs(self, msg):
        _temp = ctk.CTkLabel(self.chat_frame, text=msg,
                             font=("Arial", 12, "bold"), wraplength=250)
        _temp.pack(padx=10, pady=5, ipady=5, anchor="center")
        self.chat_frame._parent_canvas.yview_moveto(2)


def Keep_alive() -> None:
    global running, runner
    while runner:
        while running:
            try:
                resp = json.loads(connection.client.recv(1024))
                if resp:
                    if resp['status'] == 'message':
                        rest = chat.add_msg(resp['from'] + ": " + resp['message'], resp['from'] == username)
                    elif resp['status'] == 'boardcast':
                        rest = chat.add_bcs(resp['message'])

            except:
                pass
        time.sleep(0.1)


home = Home()
if __name__ == "__main__":
    keepalive = Thread(target=Keep_alive, daemon=True)
    keepalive.start()
    home.mainloop()
