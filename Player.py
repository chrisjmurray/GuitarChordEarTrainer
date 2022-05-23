import rtmidi
import time

CHORDDURATION = 1.25
ARPDURATION = .5

inst_dict = {'Acoustic Grand Piano': 1, 
             'Acoustic Guitar (nylon)': 25,
             'Electric Guitar (jazz)': 27,
             'Overdriven Guitar': 30,
             'Distortion Guitar': 31 }

class Player:
    def __init__(self):
        self.midiout = None
        self.setport()

    def setport(self):
        self.midiout = rtmidi.MidiOut()
        try:
            self.midiout.open_port(0)
        except:
            print("unable to open port")
    
    def changeinstrument(self, instname):
        instnum=inst_dict[instname]
        self.midiout.send_message([0xC0, instnum, 0])
        
    def makeonoffmessages(self, notes):
        """returns list of tuples of on/off messages for a given
        note or set of notes"""
        velocity = 112
        on = 0x90
        off = 0x80
        if isinstance(notes, int):
            note_on = [on, notes, velocity]
            note_off = [off , notes, 0]
            return[(note_on, note_off)]
        if isinstance(notes, list):
            result = []
            for note in notes:
                note_on = [on, note, velocity]
                note_off = [off , note, 0]
                result.append((note_on, note_off))
            return result

    def playchord(self, notes):
        events = self.makeonoffmessages(notes)
        for tup in events:
            note_on, note_off = tup
            self.midiout.send_message(note_on)
        time.sleep(CHORDDURATION)
        for tup in events:
            note_on, note_off = tup
            self.midiout.send_message(note_off)

    def playarpeggio(self, notes):
        events = self.makeonoffmessages(notes)
        for tup in events:
            note_on, note_off = tup
            self.midiout.send_message(note_on)
            time.sleep(ARPDURATION)
            self.midiout.send_message(note_off)
            

    def __del__(self):
        del self.midiout

