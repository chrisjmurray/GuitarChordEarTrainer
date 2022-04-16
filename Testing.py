from fingerings import ChordManager
import Player
"""
p = Player.Player()
cm = ChordManager()

p.playchord(cm.midinotes)
p.playarpeggio(cm.midinotes)"""

running = True
while(running):
    x =input("> ")
    match x:
        case '':
            print("supdog")
            continue
        case 'x':
            running=False
    print("end of while")