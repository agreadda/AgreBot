'''
Created on Nov 27, 2017

@author: zacha
'''
import re

class AgreBotCommands(object):
    '''
    classdocs
    '''
    __listOfAdmins__ = ['agreadda']
    __listOfAdminCommands__ = {'agrebot.*?  ban.*?': '<INSERT COMMAND>',
                               'agrebot.*? timeout.*?': '/timeout ranger_rolin 15',
                               'agrebot.*? shut down the stream': '<INSERT COMMAND>' 
    }
    __listOfCommands__ = {'agrebot.*?please': '<INSERT COMMAND>', 'agrebot.*?how many points do I have.*?': '<INSERT COMMAND>', 
                               'agrebot.*? who are the mods.*?': '/mods'}
    __listOfCommandsResponses__ = {'agrebot.*?please': 'I guess I can help you out.', 'agrebot.*?how many points do I have.*?': 'A lot. Why?', 
                               'agrebot.*? ban.*?': 'right away',
                               'agrebot.*? timeout.*?': 'Right away.',
                               'agrebot.*? who are the mods.*?': '/mods',
                               'agrebot.*? shut down the stream': 'If I have to....' }
    
    def executeCommand(self, incomingCommand):
        print  incomingCommand
        return incomingCommand
    
    def __init__(self):
        '''
        Constructor
        '''
    
    #first check if we should even process
    def startsWithAgre(self, message):
        if(message.lower().startswith( 'agrebot' ) or message.lower().startswith( 'hey agrebot' )):
            return True
        return False
    
    #match against all regex commands that we find
    def isCommand(self, message, user):
        if(self.startsWithAgre(message)):
            for regex in self.__listOfCommands__.keys():
                print regex
                p = re.compile(regex)
                if(p.match(message)):
                    self.executeCommand(self.__listOfCommands__[regex])
                    return {self.executeCommand(self.__listOfCommands__[regex]), self.executeCommand(self.__listOfCommandsResponses__[regex])} 
            if user.lower() in self.__listOfAdmins__:
                for regex in self.__listOfAdminCommands__.keys():
                    print regex
                    p = re.compile(regex)
                    if(p.match(message)):
                        self.executeCommand(self.__listOfAdminCommands__[regex])
                        return { self.executeCommand(self.__listOfAdminCommands__[regex]), self.executeCommand(self.__listOfCommandsResponses__[regex]) } 
        return 'No Command Found'
                