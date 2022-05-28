from PIL import Image, ImageDraw, ImageTk
import os

blankdiagrampath = os.path.dirname(os.path.abspath(__file__))
blankdiagrampath = os.path.join(blankdiagrampath, 'Data', 'blankfretboard.png')
interfretdist = 71
interstringdist = 52
basestringpos = 35
basefretpos = 70
dotdiam = 32

class FretDiagramCanvas:
    def __init__(self, chordmanager, canvas):
        self.cm = chordmanager
        self.canvas = canvas
        img = Image.open(blankdiagrampath)
        aspectratio = img.height/img.width
        self.height = self.canvas.winfo_height()
        self.width = int(self.height/aspectratio)
        self.image = self.fingeringtodiagram()
        self.image_container = self.canvas.create_image(int(self.canvas.winfo_width()/2), int(self.canvas.winfo_height()/2))
        self.showblank()

    
    def coordsfromcenter(self, center, diameter=30):
        """helper function for ImageDraw.Draw.ellipse. center is given as a tuple (xcoord, ycoord)"""
        cx, cy = center
        d = diameter
        return [cx-d/2,cy-d/2, cx+d/2, cy+d/2]
    
    def frettocentercoord(self, string, fret):
        xcoord = string*interstringdist+basestringpos
        ycoord = fret*interfretdist+basefretpos
        return(xcoord, ycoord)
    
    def fingeringtodiagram(self, showfrets=True):
        if not showfrets:
            zeroedfingering = [-1,-1,-1,-1,-1,-1]
        else:
            zeroedfingering = self.cm.zeroedfingering
        fretcoords = []
        for string, fret in enumerate(zeroedfingering):
            if fret != -1:
                fretcoords.append(self.frettocentercoord(string, fret))
        im = Image.open(blankdiagrampath)
        draw = ImageDraw.Draw(im)
        for coord in fretcoords:
            draw.ellipse(self.coordsfromcenter(coord, 32), fill='black', outline='black')
        im = im.resize((int(self.width), int(self.height)), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(im)
        return im
    
    def showfrets(self):
        self.image = self.fingeringtodiagram(showfrets=True)
        self.canvas.itemconfig(self.image_container, image = self.image)
        self.canvas.update()
    def showblank(self):
        self.image = self.fingeringtodiagram(showfrets=False)
        self.canvas.itemconfig(self.image_container, image = self.image)
        self.canvas.update()