from fingerings import ChordManager
import Player

p = Player.Player()
cm = ChordManager()

p.playchord(cm.midinotes)
p.playarpeggio(cm.midinotes)