'''
Created on Nov 24, 2017

@author: zachary.a.ob@gmail.com
'''
import socket, string
import aiml
import os, time, random, hashlib
import json, pickle
import SessionManager
import datetime
import sqlite3
import CommandDetector
import DbConn

# Set all the variables necessary run
session_data = "../sessions/data.p"
session_dict = "../sessions/sessions.p"
HOST = "irc.twitch.tv"
NICK = "AgreBot"
PORT = 6667
PASS = "oauth:0lko75l2pedu2pfgjnesruf3k3bfgt"
readbuffer = ""
MODT = False
channel_name = "#agreadda"
should_save_at = datetime.datetime.now() + datetime.timedelta(minutes = 1)

# Method for creating a random session id
def generateRandomSessionKey():
    rawdata = private_secret + str(time.time()) + string.join(map(chr, [random.randint(0,255) for x in range(100)]),"")
    session_key = hashlib.sha256(rawdata).hexdigest()
    del(rawdata)
    return session_key

def Db_save():
    print "Saving DB"
    db_conn.save_results()
    db_conn.increase_viewer_points(channel_name)

# Method for sending a message
def Send_message(message):
    s.send("PRIVMSG "+ channel_name +" :" + message + "\r\n")

def Save_sessions(kernel_to_save, chat_mates_to_save):
    try:
        print('writing session data')
        outfile = open(session_data, 'wb')
        pickle.dump(kernel_to_save._sessions, outfile)
        outfile.close()
    except IOError as e:
        print(e.errno)
    
    try:
        print('writing session dict')
        outfile = open(session_dict, 'wb')
        pickle.dump(chat_mates_to_save._sessionDict, outfile)
        outfile.close()
    except IOError as e:
        print(e.errno)
        
def Open_sessions(kernel_to_populate, chat_mates_to_save):
    try:
        print('pulling session data')
        infile = open(session_data, 'rb')
        kernel_to_populate._sessions=pickle.load(infile) 
        print("done pulling session data")
    except IOError as e:
        print(e.errno)            

    try:
        print('pulling session dict')
        infile = open(session_dict, 'rb')
        chat_mates_to_save._sessionDict = pickle.load(infile)
        print('done pulling dict')
    except IOError as e:
        print(e.errno)
        
        
#**********************************
#START PROGRAM RUN
#**********************************

# My Secret Key
private_secret = os.urandom(64)

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

chat_users = SessionManager.Session()
agre_bot_commands = CommandDetector.AgreBotCommands()
db_conn = DbConn.AgreBotDbConnection(1)

Open_sessions(kernel, chat_users)
print('after session load')
print(chat_users._sessionDict)
print(kernel._sessions)
print('entering program')

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN "+ channel_name +" \r\n")
#creating DB Connection

while True:
    #if you haven't saved all entries, points, etc in the last 5min then save
    if(should_save_at.time() < datetime.datetime.now().time()):
        
        Db_save()
        should_save_at = should_save_at + datetime.timedelta(minutes = 5)
        
    #fetch the message from the stream
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    #looping through all messages
    for line in temp:
        #print(line)
        #print(chat_users._sessionDict)
        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        else:
            # Splits the given string so we can work with it better
            parts = string.split(line, ":")
            #check for specifit twitch messages to ignore
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                #parse the message
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]
                
                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                if MODT:
                    print(chat_users._sessionDict)
                    #kernel.respond("hi")
                    if not username in chat_users._sessionDict.keys():
                        chat_users._sessionDict[username] = generateRandomSessionKey()
                    wasCommand = agre_bot_commands.isCommand(message, username)
                    print wasCommand
                    if('No Command Found' not in wasCommand):
                        print "executing command"
                        for key in wasCommand:
                            Send_message(key)
                    else:
                        Send_message(kernel.respond(message, chat_users._sessionDict[username]))
                    print(username + ": " + message)
                    #print(kernel._sessions)
                    Save_sessions(kernel, chat_users)
                    
                    # You can add all your plain commands here
                    #if message == "Hey":
                    #    Send_message("Welcome to my stream, " + username)

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True