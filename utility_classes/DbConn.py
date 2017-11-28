'''
Created on Nov 25, 2017

@author: zacha
'''
import sqlite3
import requests
import json

db_name = "../database/sqlitedb.db"


class AgreBotDbConnection(object):
    '''
    classdocs
    '''
    con = None
    ppm = 1

    def __init__(self, points_per_minute):
        '''
        Constructor
        '''
        self.conn = sqlite3.connect(db_name)
        self.ppm = points_per_minute
        
    def run_query(self, query):
        c = self.conn.cursor()
        c.execute(query);
        self.conn.commit()
        
        #c.execute('SELECT * FROM USER_POINTS')
        #rows = c.fetchall()
        #print rows
        
    
    def create_user_table(self):
        self.run_query('''CREATE TABLE IF NOT EXISTS stocks
             (id integer primary key autoincrement, username text, timeinchat integer, points integer, active integer, role text)''')
        #'''create table entries (id integer primary key autoincrement, username text, timeinchat integer, points integer, active integer, role text)'''
    
    def close_connection(self):
        self.conn.close()
        
    def save_results(self):
        return
        
    def increase_viewer_points(self, channel_name):
        #API call to get current viewers
        response = requests.get("https://tmi.twitch.tv/group/user/" + channel_name + "/chatters")
        print response.json()
        
        #pull each type of user from json
        userdata = response.json()
        modList = userdata['chatters']['moderators']
        viewerList = userdata['chatters']['viewers']
        staffList = userdata['chatters']['staff']
        adminList = userdata['chatters']['admins']
        globalModList = userdata['chatters']['global_mods']
        
        #get 1 user list
        totalViewerList = modList + viewerList + staffList + adminList + globalModList
        
        userListString = "";
        #update table set points = points + <MOD>, timeInChat = timeInChat + 5 where username in ("list of users")
        for user in totalViewerList: 
            userListString = userListString + user + ","
            
        updatePoints = '''UPDATE USER_POINTS SET POINTS = POINTS + ''' + self.ppm + ''', CHAT_TIME = CHAT_TIME + 5 where username in (''' + userListString + ''')'''
        
        self.run_query(updatePoints)
            
            
        
        