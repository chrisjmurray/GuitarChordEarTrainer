from fingerings import ChordManager
from Player import Player

welcome_string = """Welcome. Press enter to play chords and also to display the answer.\nEnter h for help, x for exit"""
help_string = """You're on your own, bucko"""
class GameConsole:
    def __init__(self):
        self.cm = ChordManager()
        self.player = Player()
        self.loadoptions()
        self.playgame()

    def playgame(self):
        running = True
        isDuringTurn = False
        print(welcome_string)
        print("Enter to start")
        while(running):
            userin = input("> ")
            match userin:
                case '':
                    if isDuringTurn:
                        isDuringTurn = False
                        self.cm.printfingering()
                    elif not isDuringTurn:
                        isDuringTurn = True
                        self.cm.setnew()
                        self.player.playchord(self.cm.midinotes)
                case 'a':
                    self.player.playarpeggio(self.cm.midinotes)
                case 'r':
                    self.player.playchord(self.cm.midinotes)
                case 'h':
                    self.help()
                case 'o':
                    self.options()
                case 'q':
                    break
                case default:
                    print("Invalid input")
    
    def help(self):
        print(help_string)
    def options(self):   
        print("no options yet")         

    def loadoptions(self):
        pass
    
if __name__ == "__main__":
   GameConsole()