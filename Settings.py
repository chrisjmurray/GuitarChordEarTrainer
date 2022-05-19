import confighandler

class SettingsHolder:
    def __init__(self):
        self._active_taggroup = self.getconfigtaggroup()
        self._active_instrument = self.getconfiginstrument()

    def getconfigtaggroup(self):
        return confighandler.getsetting('tag_group')
    
    def getconfiginstrument(self):
        return confighandler.getsetting('playback_instrument')
    
    def settaggroup(self, taggroupname):
        '''sets the active taggroup as well, as writes it to the config file 
        so it remains the active taggroup on the next startup. taggroup = <custom> signifies
        that the user has edited the active tags without saving as a taggroup name'''
        self._active_taggroup = taggroupname
        confighandler.setsetting('tag_group', taggroupname)