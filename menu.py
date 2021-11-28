import tkinter as tk
import tkinter.messagebox as messagebox
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from threading import Thread


CREDITS = """Designers
Lead Designer - Martin

Programmers
Lead Programmer - Martin

Artists
Lead Artist - @suspicious_brix
Other Artists: Martin

Please like the Repl
Thanks!
"""


CONTROLS = """Start/stop level:
E
Restart level:
Double tap E
Switch character:
Q

Jump:
W
Left:
A
Right:
D
Groundpound:
S

Add time to timer:
+
Remove time from timer:
-"""



retry_strategy = Retry(
    total=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


class Menu(tk.Tk):
  def __init__(self, play):
    super().__init__()
    self.play = play
    self.title('Make the Jump 2!')

    self.main = tk.Frame(self)
    self.main.grid(row=0, column=0, sticky='news')
    self.create = tk.Frame(self)
    self.create.grid(row=0, column=0, sticky='news')
    self.load = tk.Frame(self)
    self.load.grid(row=0, column=0, sticky='news')
    self.credits = tk.Frame(self)
    self.credits.grid(row=0, column=0, sticky='news')
    self.controls = tk.Frame(self)
    self.controls.grid(row=0, column=0, sticky='news')
    self.main.tkraise()

    self.upload_level_button = tk.Button(self.main, text='Upload Level', command=self.upload_mode)
    self.upload_level_button.pack()

    self.download_level_button = tk.Button(self.main, text='Download Level', command=self.load_mode)
    self.download_level_button.pack()

    self.credits_button = tk.Button(self.main, text='Credits', command=self.credits_mode)
    self.credits_button.pack()

    self.controls_button = tk.Button(self.main, text='Controls', command=self.controls_mode)
    self.controls_button.pack()

    self.back_button0 = tk.Button(self.main, text='Back to Game', command=self.destroy)
    self.back_button0.pack()

    self.name_entry_label = tk.Label(self.create, text="Level Title")
    self.name_entry_label.pack()

    self.name_entry = tk.Entry(self.create)
    self.name_entry.pack()

    self.descrition_entry_label = tk.Label(self.create, text="Level Description")
    self.descrition_entry_label.pack()

    self.descrition_entry = tk.Text(self.create, height = 3, width = 20)
    self.descrition_entry.pack()

    self.done_button1 = tk.Button(self.create, text='Done', command=self.upload_level)
    self.done_button1.pack()

    self.back_button1 = tk.Button(self.create, text='Back', command=self.back)
    self.back_button1.pack()

    self.level_id_entry_label = tk.Label(self.load, text="Level ID")
    self.level_id_entry_label.pack()

    self.level_id_entry = tk.Entry(self.load)
    self.level_id_entry.pack()

    self.done_button2 = tk.Button(self.load, text='Done', command=self.load_level)
    self.done_button2.pack()

    self.back_button2 = tk.Button(self.load, text='Back', command=self.back)
    self.back_button2.pack()

    # self.credits_text = tk.Text(self.credits, height=10, width=20)
    # self.credits_text.insert(tk.END, CREDITS)
    # self.credits_text.config(state=tk.DISABLED)
    # self.credits_text.pack()

    self.credit_scrollbar_y = tk.Scrollbar(self.credits)
    self.credit_scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)

    self.credit_scrollbar_x = tk.Scrollbar(self.credits, orient='horizontal')
    self.credit_scrollbar_x.pack(side = tk.BOTTOM, fill = tk.X)

    self.credits_text = tk.Listbox(self.credits, yscrollcommand=self.credit_scrollbar_y.set, xscrollcommand=self.credit_scrollbar_x.set, height=5)
    for line in CREDITS.split("\n"):
      self.credits_text.insert(tk.END, line)
    self.credits_text.pack()

    self.credit_scrollbar_y.config(command=self.credits_text.yview)
    self.credit_scrollbar_x.config(command=self.credits_text.xview)

    self.back_button2 = tk.Button(self.credits, text='Back', command=self.back)
    self.back_button2.pack()

    self.controls_scrollbar_y = tk.Scrollbar(self.controls)
    self.controls_scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)

    self.controls_scrollbar_x = tk.Scrollbar(self.controls, orient='horizontal')
    self.controls_scrollbar_x.pack(side = tk.BOTTOM, fill = tk.X)

    self.controls_text = tk.Listbox(self.controls, yscrollcommand=self.controls_scrollbar_y.set, xscrollcommand=self.controls_scrollbar_x.set, height=5)
    for line in CONTROLS.split("\n"):
      self.controls_text.insert(tk.END, line)
    self.controls_text.pack()

    self.controls_scrollbar_y.config(command=self.controls_text.yview)
    self.controls_scrollbar_x.config(command=self.controls_text.xview)

    self.back_button3 = tk.Button(self.controls, text='Back', command=self.back)
    self.back_button3.pack()
  """
  def on_show_frame(self, evt):
    print(c, self.c)
    if c != self.c:
      raise Exception()
  """
  
  def upload_mode(self):
    self.name_entry.delete(0, tk.END)
    self.descrition_entry.delete("1.0", tk.END)
    self.create.tkraise()
  
  def upload_level(self):
    try:
      http.get("https://make-the-jump-2-levels.martinstaab.repl.co/")
      data = requests.post("https://make-the-jump-2-levels.martinstaab.repl.co/upload", {"title": self.name_entry.get().strip(), "description": self.descrition_entry.get("1.0", tk.END).strip(), "level": self.play.to_json()}).text
      
      messagebox.showinfo("Share Level", "Level uploaded! Level ID is: " + str(json.loads(data)["level_id"]) + ".")
      self.back()
    except requests.exceptions.RetryError:
      messagebox.showinfo("Share Level", "Please open up Make the Jump 2 Levels in a new tab (link is in description), then try to share your level again.")
  
  def load_mode(self):
    self.level_id_entry.delete(0, tk.END)
    self.load.tkraise()
  
  def load_level(self):
    try:
      level_id = int(self.level_id_entry.get().strip())
    except ValueError:
      messagebox.showinfo("Share Level", "Please enter a valid Level ID")
      return
    try:
      http.get("https://make-the-jump-2-levels.martinstaab.repl.co/")
      data = requests.get("https://make-the-jump-2-levels.martinstaab.repl.co/level/" + str(level_id)).text
      self.play.from_json(data)
      self.back()
    except requests.exceptions.RetryError:
      messagebox.showinfo("Share Level", "Please open up Make the Jump 2 Levels in a new tab (link is in description), then try to load the level again.")
  
  def credits_mode(self):
    self.credits.tkraise()
  
  def controls_mode(self):
    self.controls.tkraise()
  
  def back(self):
    self.main.tkraise()


def go(play):
  menu = Menu(play)
  menu.mainloop()
