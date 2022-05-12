import tkinter as tk
from tkinter import BOTTOM, LEFT, TOP, ttk 
from ctypes import windll
from fingerings import ChordManager
from Player import Player

class Game:
    def __init__(self, master):
        lbl_1string_text = "e: "
        lbl_2string_text = "B: "
        lbl_3string_text = "G: "
        lbl_4string_text = "D: "
        lbl_5string_text = "A: "
        lbl_6string_text = "E: "
        self.isDuringTurn=False

        self.master = master
        master.title('Guitar Chord Ear Trainer') 
        title = master.title()    
        window_width = 400
        window_height = 400

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        #Labels for string numbers and fret numbers
        frame_output = ttk.Frame(master=master)
        self.lbl_1string = ttk.Label(text=lbl_1string_text, master=frame_output)
        self.lbl_1string.grid(row=0, column=0)
        self.lbl_1fret = ttk.Label(text='x', master = frame_output)
        self.lbl_1fret.grid(row=0, column=1)
        self.lbl_2string = ttk.Label(text=lbl_2string_text, master=frame_output)
        self.lbl_2string.grid(row=1, column=0)
        self.lbl_2fret = ttk.Label(text='x', master=frame_output)
        self.lbl_2fret.grid(row=1, column=1)
        self.lbl_3string = ttk.Label(text=lbl_3string_text, master=frame_output)
        self.lbl_3string.grid(row=2, column=0)
        self.lbl_3fret = ttk.Label(text='x', master=frame_output)
        self.lbl_3fret.grid(row=2, column=1)
        self.lbl_4string = ttk.Label(text=lbl_4string_text, master=frame_output)
        self.lbl_4string.grid(row=3, column=0)
        self.lbl_4fret = ttk.Label(text='x', master=frame_output)
        self.lbl_4fret.grid(row=3, column=1)
        self.lbl_5string = ttk.Label(text=lbl_5string_text, master=frame_output)
        self.lbl_5string.grid(row=4, column=0)
        self.lbl_5fret = ttk.Label(text='x', master=frame_output)
        self.lbl_5fret.grid(row=4, column=1)
        self.lbl_6string = ttk.Label(text=lbl_6string_text, master=frame_output)
        self.lbl_6string.grid(row=5, column=0)
        self.lbl_6fret = ttk.Label(text='x', master=frame_output)
        self.lbl_6fret.grid(row=5, column=1)
        frame_output.pack(expand=True)

        #buttons Next, arppegiate, repeat
        frame_control = ttk.Frame(master=master)
        btn_continue = ttk.Button(text="Continue", master=frame_control, command=self.btn_continue_action)
        btn_continue.pack(side=LEFT)
        btn_repeat = ttk.Button(text="Repeat", master=frame_control, command=self.btn_repeat_action)
        btn_repeat.pack(side=LEFT)
        btn_arpeggiate = ttk.Button(text="Arpeggiate", master=frame_control, command=self.btn_arpeggiate_action)
        btn_arpeggiate.pack(side=LEFT)
        frame_control.pack(side=BOTTOM)

        #behavior objects
        self.cm = ChordManager()
        self.player = Player()
    
    def update_fret_labels(self, labelList):
        self.lbl_1fret['text'] = labelList[0]
        self.lbl_2fret['text'] = labelList[1]
        self.lbl_3fret['text'] = labelList[2]
        self.lbl_4fret['text'] = labelList[3]
        self.lbl_5fret['text'] = labelList[4]
        self.lbl_6fret['text'] = labelList[5]

    def btn_continue_action(self):
        if self.isDuringTurn:
            self.isDuringTurn = False
            labelList = self.cm.getfretlabels()
            self.update_fret_labels(labelList)
        
        elif not self.isDuringTurn:
            self.isDuringTurn = True
            self.update_fret_labels(['x']*6)
            self.cm.setnew()
            self.player.playchord(self.cm.midinotes)

    def btn_repeat_action(self):
        self.player.playchord(self.cm.midinotes)

    def btn_arpeggiate_action(self):
        self.player.playarpeggio(self.cm.midinotes)


if __name__ == "__main__":
    try: # this block is for fixing the UI blur specific to windows
        # put it in a try/finally block to keep program compatible 
        # with macOS, Linux
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
    #keep the window displaying
        root = tk.Tk()
        Game(root)
        root.mainloop()