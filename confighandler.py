import configparser


def listtostring(listofstrings):
    '''converts a list of tag strings to a single string suitable for
    writing in the config file'''
    return ','.join(listofstrings)

def stringtolist(string):
    '''converts a string of tags, as formatted in the config file, to a list
    of individual tags'''
    return string.split(',')

def buildconfig():
    parser = configparser.ConfigParser()
    parser.add_section('tag_groups')

    threenotevoicings = '0-1-2,0-2-4,0-3-6,0-4-8,0-2-7,0-1-3,0-2-3,0-1-4,0-3-4,0-1-5,0-4-5,0-1-6,0-5-6,0-2-5,0-3-5,0-2-6,0-4-6,0-3-7,0-4-7'
    parser.set('tag_groups', 'All three note voicings', threenotevoicings)

    majorminorvoicings = '0-4-7,0-3-7'
    parser.set('tag_groups', 'Major and Minor Triads', majorminorvoicings)

    triadvoicings = '0-3-6,0-3-7,0-4-7,0-4-8'
    parser.set('tag_groups', 'All Triads', triadvoicings)

    parser.set('tag_groups', 'Dyads', 'dyad')

    parser.add_section('settings')
    parser.set('settings', 'tag_group', 'all three note voicings')
    parser.set('settings', 'playback_instrument', 'Acoustic Guitar (nylon)')

    configfile = open('config.ini', 'w+')
    parser.write(configfile)
    configfile.close()

def addtaggroup(name, tags):
    '''Adds a tag group to the config file. name is a string and tags is a list of strings. This method does not validate strings'''
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    parser.set('tag_groups', name, tags)
    configfile = open('config.ini', 'w+')
    parser.write(configfile)
    configfile.close()

def removetaggroup(name):
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    if parser.has_option('tag_groups', name):
        parser.remove_option('tag_groups', name)
    
    configfile = open('config.ini', 'w+')
    parser.write(configfile)
    configfile.close()

def gettaggroupnames():
    '''returns a list of the tag group names as strings'''
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    return parser.options('tag_groups')

def gettagsfromtaggroup(taggroupname):
    '''returns a list of tags as strings that belong to a tag group'''
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    tags = parser.get('tag_groups', taggroupname)
    return stringtolist(tags)

def getsetting(settingname):
    '''returns the string associated with the given setting. tag_group, playback_instrument'''
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    return parser.get('settings', settingname)

def setsetting(settingname, option):
    '''writes the setting to the config file. example, settingname='tag_group', option='Dyads' '''
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    parser.set('settings', settingname, option)
    configfile = open('config.ini', 'w+')
    parser.write(configfile)
    configfile.close()
