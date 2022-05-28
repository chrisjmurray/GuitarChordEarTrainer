from random import randint
import DBOperations
import confighandler

class ChordManager:
    def __init__(self, tags = None):
        self.tuning = [40, 45, 50, 55, 59, 64] #holds midi note values of the open guitar strings, indexed same as fingerings
        self.fingering = [] #low E string at index 0, high E at index 5
        self.zeroedfingering = []
        self.midinotes = [] #holds the midi note value
        self.maxposition = 15
        if tags == None:
            self.tags = DBOperations.get_all_tags()
        else:
            self.tags = tags
        self.setnew()

    def parsefing(self, newfromdb):
        fingstring = newfromdb[0]
        self.zeroedfingering = list(map(int, fingstring.split(',')))
        self.fingering = list(map(int, fingstring.split(',')))

    def parsetags(self, newfromdb):
        pass

    def setmidinotes(self):
        self.midinotes = []
        for i, fret in enumerate(self.fingering):
            if (fret != -1):
                self.midinotes.append(fret+self.tuning[i])
    
    def setrandposition(self):
        randpos = randint(0, self.maxposition)
        for i, x in enumerate(self.fingering):
            if (x != -1):
                self.fingering[i] = randpos + x
    
    def printfingering(self):
        printstring = ''
        for fret in self.fingering:
            if fret == -1:
                printstring += 'x'
            else:
                printstring += str(fret)
            printstring += ' '
        print(printstring)
    
    def getfretlabels(self):
        '''returns a list of strings for the fret labels. high e at index 0
        and low E at index 5'''
        labelList = []
        for fret in self.fingering:
            if fret == -1:
                labelList.append('x')
            else:
                labelList.append(str(fret))
        labelList.reverse()
        return labelList
    def gettagsfordbsearch(self):
        '''returns active tag list in string format suitable for database search. e.g. (tag1, tag2, tag3) '''
        return "('"+"', '".join(self.tags)+"')"

    def gettagsforstringvar(self):
        '''returns active tags in string format suitable for tkinter's listbox's stringvar'''
        return ' '.join(self.tags)
    
    def settagsfromtaggroup(self, taggroupname):
        self.tags = confighandler.gettagsfromtaggroup(taggroupname)

    def setnew(self):
        if len(self.tags) == 0:
            newfromdb = DBOperations.fetchrandfing()
        else:
            newfromdb = DBOperations.fetch_rand_fingering_from_tags(self.tags)
        self.parsefing(newfromdb)
        self.parsetags(newfromdb)
        self.setrandposition()
        self.setmidinotes()

