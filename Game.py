import tkinter as tk
from tkinter import BOTTOM, END, LEFT, TOP, Menu, Toplevel, ttk, messagebox 
from ctypes import windll

from fingerings import ChordManager
from Player import Player
from Player import inst_dict
import DBOperations
import confighandler
import string
import Settings

reserved_names = ['all three note voicings', 'major and minor triads', 'all triads', 'dyads']

class HelpWindow:
    def __init__(self, master):
        helpstring = "Press Continue to start/finish a turn. \nRepeat and Arpeggiate will replay the current voicing.\nShortcut keys: Enter - Continue, a - arpeggiate, r - repeat"

        win = Toplevel(master)

        window_width = 400
        window_height = 200
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        win.title("Help")
        ttk.Label(win, text=helpstring).pack()

class TagsWindow:
    def __init__(self, master, chordmanager, settingsholder):
        self.cm = chordmanager
        self.settingsholder = settingsholder
        self.win = Toplevel(master)        

        window_width = 575
        window_height = 300
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self.center_x = int(screen_width/2 - window_width/2)
        self.center_y = int(screen_height/2 - window_height/2)
        self.win.geometry(f'{window_width}x{window_height}+{self.center_x}+{self.center_y}')
        self.win.title("Manage Tags")

        frame_alltags = ttk.Frame(master=self.win)
        frame_activetags = ttk.Frame(master=self.win)

        lbl_alltags = ttk.Label(master = self.win, text='All Tags')
        lbl_activetags = ttk.Label(master = self.win, text='Active Tags')             

        sv = DBOperations.get_all_tags()
        sv.sort()
        sv = tk.StringVar(master=frame_alltags, value = sv)
        settingsforlistbox = {'height': 8, 'selectmode': 'single'}
        self.lstbx_alltags = tk.Listbox(master=frame_alltags, listvariable = sv, **settingsforlistbox)
        self.lstbx_activetags = tk.Listbox(master=frame_activetags, **settingsforlistbox)
        for tag in self.cm.tags:
            self.lstbx_activetags.insert(END, tag)

        scrllbr_alltags = tk.Scrollbar(frame_alltags, orient="vertical", command=self.lstbx_alltags.yview)
        scrllbr_activetags = tk.Scrollbar(frame_activetags, orient="vertical",command=self.lstbx_activetags.yview)

        frame_taggroups = ttk.Frame(master=self.win)
        lbl_taggroups = ttk.Label(master = self.win, text='Tag Groups')
        self.cmbbx_taggroups = ttk.Combobox(master = frame_taggroups, values = confighandler.gettaggroupnames())
        self.cmbbx_taggroups['state'] = 'readonly'
        self.cmbbx_taggroups.pack(side=TOP)
        self.cmbbx_taggroups.bind('<<ComboboxSelected>>', self.cmbbx_tagchanged)
        self.refresh_cmbbx_taggroups()

        self.btn_done = ttk.Button(text='Done', master=self.win, command=self.win.destroy)  

        btn_addtag = ttk.Button(text='Add', master=self.win, command=self.btn_addtag_action)
        btn_removetag = ttk.Button(text='Remove', master=self.win, command=self.btn_removetag_action)
        lbl_savegroup = ttk.Label(master=self.win, text='Save active tags as group')
        btn_savegroup = ttk.Button(text='Save Group', master =self.win, command=self.btn_savetaggroup_action)

        self.lstbx_alltags.pack(side='left', fill='y')
        scrllbr_alltags.pack(side='right', fill='y')
        self.lstbx_activetags.pack(side='left', fill='y')
        scrllbr_activetags.pack(side='right', fill='y')

        self.lstbx_alltags.config(yscrollcommand = scrllbr_alltags.set)
        self.lstbx_activetags.config(yscrollcommand=scrllbr_activetags.set)

        lbl_alltags.grid(row=0, column=0)
        frame_alltags.grid(row=1, column=0)
        btn_addtag.grid(row=2, column=0)

        lbl_activetags.grid(row=0, column=1)
        frame_activetags.grid(row=1, column=1)
        btn_removetag.grid(row=2, column=1)
        lbl_savegroup.grid(row=3, column=1)
        btn_savegroup.grid(row=4, column=1)

        lbl_taggroups.grid(row=0, column=2)
        frame_taggroups.grid(row=1, column=2)
        self.btn_done.grid(row=4, column=2)

    def refresh_cmbbx_taggroups(self):
        self.cmbbx_taggroups['values'] = confighandler.gettaggroupnames().sort()
        self.cmbbx_taggroups.set(self.settingsholder._active_taggroup)
        
    def btn_addtag_action(self):
        item = self.lstbx_alltags.selection_get()

        if item not in self.cm.tags:
            self.cm.tags.append(item)
            self.lstbx_activetags.insert(END, item)
            self.cmbbx_taggroups.set('<custom>')
            confighandler.addtaggroup('<custom>', confighandler.listtostring(self.cm.tags))
            confighandler.setsetting('tag_group', '<custom>')
    
    def btn_removetag_action(self):
        item = self.lstbx_activetags.selection_get()
        if (len(self.cm.tags) > 0):
            self.cm.tags.remove(item)
            self.cm.tags.sort()
            i = self.lstbx_activetags.get(0, END).index(item)
            self.lstbx_activetags.delete(i)
            self.cmbbx_taggroups.set('<custom>')
            confighandler.addtaggroup('<custom>', confighandler.listtostring(self.cm.tags))
            confighandler.setsetting('tag_group', '<custom>')

    def btn_cleartags_action(self):
        self.lstbx_activetags.delete(0, END)
        self.cm.tags = []

    def btn_savetaggroup_action(self):
        win2 = Toplevel(self.win)
        window_width = 400
        window_height = 150
        win2.geometry(f'{window_width}x{window_height}+{self.center_x}+{self.center_y}')
        win2.title("Save active tags as group")
        
        def groupnameisvalid(name):
            '''returns an empty string if the name is valid. returns a description of the error if the name is invalid'''
            
            result = ''
            if len(name) > 20:
                result = 'Max length of name is 20 characters'
                return result
            if set(name) == set(' '):
                result = "Name must include characters other than spaces"
                return result
            allowed = set(string.ascii_lowercase + string.digits + '-' + '_' + ' ')
            if not set(name).issubset(allowed):
                result = "Allowed characters: lowercase letters, numbers, -, _, spaces"
                return result
            if name in reserved_names:
                result = "Name reserved for default group"
                return result
            return result

        def btn_save_action():
            name = entry_nameprompt.get()
            isvalidresult = groupnameisvalid(name)
            if isvalidresult == '':
                confighandler.addtaggroup(name, confighandler.listtostring(self.cm.tags))
                self.settingsholder._active_taggroup = name
                confighandler.setsetting('tag_group', self.settingsholder._active_taggroup)
                self.refresh_cmbbx_taggroups()
                win2.destroy()
            else:
                messagebox.showinfo("Invalid name", isvalidresult)
                win2.focus()
        
        def btn_cancel_action():
            win2.destroy()

        lbl_nameprompt = ttk.Label(master=win2, text="Group Name")
        entrytext = tk.StringVar()
        entry_nameprompt = ttk.Entry(master=win2, textvariable=entrytext)
        frame_btns = ttk.Frame(master=win2)
        btn_save = ttk.Button(master=frame_btns, text='Save', command=btn_save_action)
        btn_cancel = ttk.Button(master=frame_btns, text='Cancel', command=btn_cancel_action)
        
        btn_save.grid(row=0, column=0)
        btn_cancel.grid(row=0, column=1)

        lbl_nameprompt.pack()
        entry_nameprompt.pack()
        frame_btns.pack()        
    
    def cmbbx_tagchanged(self, event):
        selected_tag = self.cmbbx_taggroups.get()
        self.btn_cleartags_action()
        tags = confighandler.gettagsfromtaggroup(selected_tag)
        for tag in tags:
            self.cm.tags.append(tag)
            self.lstbx_activetags.insert(END, tag)
        confighandler.setsetting('tag_group', selected_tag)

class AddFingeringsWindow:
    def __init__(self, master):
        lbl_1string_text = "e: "
        lbl_2string_text = "B: "
        lbl_3string_text = "G: "
        lbl_4string_text = "D: "
        lbl_5string_text = "A: "
        lbl_6string_text = "E: "

        self.win = Toplevel(master)        

        window_width = 400
        window_height = 325
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self.center_x = int(screen_width/2 - window_width/2)
        self.center_y = int(screen_height/2 - window_height/2)
        self.win.geometry(f'{window_width}x{window_height}+{self.center_x}+{self.center_y}')
        self.win.title("Add Fingerings to Database")


        frame_fretinputs = ttk.Frame(master=self.win)

        fretentrystyle = {'master': frame_fretinputs, 'width': 2}
        fretlabelstyle = {'master': frame_fretinputs}
        lbl_1string = ttk.Label(**fretlabelstyle, text=lbl_1string_text)
        self.entry_1string = ttk.Entry(**fretentrystyle)
        lbl_2string = ttk.Label(**fretlabelstyle, text=lbl_2string_text)
        self.entry_2string = ttk.Entry(**fretentrystyle)
        lbl_3string = ttk.Label(**fretlabelstyle, text=lbl_3string_text)
        self.entry_3string = ttk.Entry(**fretentrystyle)
        lbl_4string = ttk.Label(**fretlabelstyle, text=lbl_4string_text)
        self.entry_4string = ttk.Entry(**fretentrystyle)
        lbl_5string = ttk.Label(**fretlabelstyle, text=lbl_5string_text)
        self.entry_5string = ttk.Entry(**fretentrystyle)
        lbl_6string = ttk.Label(**fretlabelstyle, text=lbl_6string_text)
        self.entry_6string = ttk.Entry(**fretentrystyle)

        self.entry_1string.focus()

        lbl_1string.grid(row=0, column=0)
        self.entry_1string.grid(row=0, column=1)
        lbl_2string.grid(row=1, column=0)
        self.entry_2string.grid(row=1, column=1)
        lbl_3string.grid(row=2, column=0)
        self.entry_3string.grid(row=2, column=1)
        lbl_4string.grid(row=3, column=0)
        self.entry_4string.grid(row=3, column=1)
        lbl_5string.grid(row=4, column=0)
        self.entry_5string.grid(row=4, column=1)
        lbl_6string.grid(row=5, column=0)
        self.entry_6string.grid(row=5, column=1)

        frame_tagentry = ttk.Frame(master=self.win)
        lbl_tagentry = ttk.Label(master=frame_tagentry, text="Enter comma separated tags")
        self.entry_tagentry = ttk.Entry(master=frame_tagentry)
        lbl_tagentry.pack()
        self.entry_tagentry.pack()

        frame_btns = ttk.Frame(master=self.win)
        btn_enter = ttk.Button(text="Enter", master=frame_btns, command=self.btn_enter_action)
        self.win.bind('<Return>', self.btn_enter_action)
        btn_finish = ttk.Button(text="Finish", master=frame_btns, command=self.btn_finish_action)

        btn_enter.pack()
        btn_finish.pack()

        lbl_fretinput1 = ttk.Label(master=self.win, text="Enter fret numbers in the appropriate text box")
        lbl_fretinput2 = ttk.Label(master=self.win, text="Leave blank if string is not played")
        lbl_fretinput1.pack()
        lbl_fretinput2.pack()
        frame_fretinputs.pack()
        frame_tagentry.pack(side=LEFT)
        frame_btns.pack(side=BOTTOM)

    def btn_enter_action(self, *args):
        fretlist = []
        fretlist.append(self.entry_1string.get())
        fretlist.append(self.entry_2string.get())
        fretlist.append(self.entry_3string.get())
        fretlist.append(self.entry_4string.get())
        fretlist.append(self.entry_5string.get())
        fretlist.append(self.entry_6string.get())
        for i, fret in enumerate(fretlist):
            if fret == '':
                fretlist[i] = '-1'
        if not self.isvalidfrets(fretlist):
            return
        tagentrystring = self.entry_tagentry.get()
        taglist = self.entrystringtotaglist(tagentrystring)
        taglist.append('user defined')
        if not self.isvalidtags(taglist):
            return
        
        fingering = self.fretlisttofingering(fretlist)
        conn = DBOperations.create_connection()
        DBOperations.insert_fingering(conn, fingering, taglist)
        self.entry_1string.delete(0, END)
        self.entry_2string.delete(0, END)
        self.entry_3string.delete(0, END)
        self.entry_4string.delete(0, END)
        self.entry_5string.delete(0, END)
        self.entry_6string.delete(0, END)
        self.entry_1string.focus()


        
    def btn_finish_action(self, *args):
        self.win.destroy()
    
    def fretlisttofingering(self, fretlist):
        fretlist = [int(i) for i in fretlist]
        fretset = set(fretlist) - set([-1])
        fretmin = min(fretset)
        for i, fret in enumerate(fretlist):
            if fret != -1:
                fretlist[i] -= fretmin
        fretlist = [str(i) for i in fretlist]
        fretlist.reverse()
        return ','.join(fretlist)

    def entrystringtotaglist(self, entrystring):
        taglist = entrystring.split(',')
        taglist = [tag.lstrip().rstrip() for tag in taglist]
        return taglist

    def isvalidfrets(self, fretlist):
        for fret in fretlist:
            if not (fret.isnumeric() or fret == '-1'):
                messagebox.showinfo("Invalid frets", "only numbers allowed")
                return False
        fretlist = [int(i) for i in fretlist]
        fretset = set(fretlist) - set([-1])
        fretmin = min(fretset)
        fretmax = max(fretset)
        if fretmin < 0 or fretmax < 0:
            messagebox.showinfo("Invalid frets", "use positive fret numbers")
            return False
        if (fretmax-fretmin) > 4:
            messagebox.showinfo("Invalid frets","max fret span is 5 frets")
            return False
        return True
    def isvalidtags(self, taglist):
        for tag in taglist:
            if len(tag) > 20:
                result = 'Max length of a tag is 20 characters'
                messagebox.showinfo("Invalid tag: "+tag, "Invalid tag: "+result)
                return False
            if set(tag) == set(' '):
                result = "tags must include characters other than spaces"
                messagebox.showinfo("Invalid tag: "+tag, "Invalid tag: "+result)
                return False
            allowed = set(string.ascii_lowercase + string.digits + '-' + '_' + ' ')
            if not set(tag).issubset(allowed):
                result = "Allowed characters: lowercase letters, numbers, -, _, spaces"
                messagebox.showinfo("Invalid tag: "+tag,"Invalid tag: "+result)
                return False
        return True

class ChangeInstrumentWindow:
    def __init__(self, master, player):
        win = Toplevel(master)
        self.player = player

        window_width = 300
        window_height = 100
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        win.title("Change Instrument")
        ttk.Label(win, text='Choose the Instrument').grid(row=1, column=1)
        self.cmbbx_insts = ttk.Combobox(master = win, values = list(inst_dict.keys()))
        self.cmbbx_insts['state'] = 'readonly'
        self.cmbbx_insts.bind('<<ComboboxSelected>>', self.cmbbx_instchanged)
        self.cmbbx_insts.set(confighandler.getsetting('playback_instrument'))
        self.cmbbx_insts.grid(row=2, column=1)

        ttk.Button(master=win, text='Done', command=win.destroy).grid(row=3, column=2)
    
    def cmbbx_instchanged(self, *args):
        newinst = self.cmbbx_insts.get()
        self.player.changeinstrument(newinst)
        confighandler.setsetting('playback_instrument', newinst)

class Game:
    def __init__(self, master):
        #behavior objects
        self.cm = ChordManager()
        self.player = Player()
        self.settings = Settings.SettingsHolder()
        self.cm.settagsfromtaggroup(self.settings.getconfigtaggroup())
        self.player.changeinstrument(confighandler.getsetting('playback_instrument'))
        lbl_1string_text = "e: "
        lbl_2string_text = "B: "
        lbl_3string_text = "G: "
        lbl_4string_text = "D: "
        lbl_5string_text = "A: "
        lbl_6string_text = "E: "
        self.isDuringTurn=False

        self.master = master
        master.title('Guitar Chord Ear Trainer') 
        window_width = 400
        window_height = 400

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        menubar = Menu(master)
        optionsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Help", command=self.btn_help_action)
        optionsmenu.add_command(label="Manage Tags", command=self.open_tags_window)
        optionsmenu.add_command(label="Add Fingerings to Database", command=self.open_addfingerings_window)
        optionsmenu.add_command(label="Change Playback Instrument", command=self.open_changeinst_window)
        menubar.add_cascade(label="Options", menu=optionsmenu)
        master.config(menu=menubar)

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
        master.bind('<Return>', self.btn_continue_action)

        btn_repeat = ttk.Button(text="Repeat", master=frame_control, command=self.btn_repeat_action)
        btn_repeat.pack(side=LEFT)
        master.bind('r', self.btn_repeat_action)

        btn_arpeggiate = ttk.Button(text="Arpeggiate", master=frame_control, command=self.btn_arpeggiate_action)
        btn_arpeggiate.pack(side=LEFT)
        master.bind('a', self.btn_arpeggiate_action)

        #btn_help = ttk.Button(text="Help", master=frame_control, command=self.btn_help_action)
        #btn_help.pack(side=LEFT)
        frame_control.pack(side=BOTTOM)
    
    def update_fret_labels(self, labelList):
        self.lbl_1fret['text'] = labelList[0]
        self.lbl_2fret['text'] = labelList[1]
        self.lbl_3fret['text'] = labelList[2]
        self.lbl_4fret['text'] = labelList[3]
        self.lbl_5fret['text'] = labelList[4]
        self.lbl_6fret['text'] = labelList[5]

    def btn_continue_action(self, *args):
        if self.isDuringTurn:
            self.isDuringTurn = False
            labelList = self.cm.getfretlabels()
            self.update_fret_labels(labelList)
        
        elif not self.isDuringTurn:
            self.isDuringTurn = True
            self.update_fret_labels(['x']*6)
            self.cm.setnew()
            self.player.playchord(self.cm.midinotes)

    def btn_repeat_action(self, *args):
        self.player.playchord(self.cm.midinotes)

    def btn_arpeggiate_action(self, *args):
        self.player.playarpeggio(self.cm.midinotes)

    def btn_help_action(self):
        HelpWindow(self.master)
    
    def open_tags_window(self):
        TagsWindow(self.master, self.cm, self.settings)
    def open_addfingerings_window(self):
        AddFingeringsWindow(self.master)
    def open_changeinst_window(self):
        ChangeInstrumentWindow(self.master, self.player)

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