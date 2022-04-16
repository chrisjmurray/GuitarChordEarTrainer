import rtmidi
import time

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
        time.sleep(1.25)
        for tup in events:
            note_on, note_off = tup
            self.midiout.send_message(note_off)
            
    
    def playarpeggio(self, notes):
        events = self.makeonoffmessages(notes)
        for tup in events:
            note_on, note_off = tup
            self.midiout.send_message(note_on)
            time.sleep(0.5)
            self.midiout.send_message(note_off)
            

    def __del__(self):
        del self.midiout

