'''
Created on Nov 24, 2017

@author: zacha
'''

import socket, string
import aiml
import os, time, random, hashlib
import json, pickle
import SessionManager

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
 
# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")


# Method for sending a message
def Send_message(message):
    s.send("PRIVMSG "+ channel_name +" :" + message + "\r\n")


if __name__ == '__main__':
    # Connecting to Twitch IRC by passing credentials and joining a certain channel
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS " + PASS + "\r\n")
    s.send("NICK " + NICK + "\r\n")
    s.send("JOIN "+ channel_name +" \r\n")
    
    while True:
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()
    
        for line in temp:
            if (line[0] == "PING"):
                s.send("PONG %s\r\n" % line[1])
            else:
                # Splits the given string so we can work with it better
                parts = string.split(line, ":")
                if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
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
                        myMessage = kernel.respond(message)
                        print(username + ": " + message)
                        print("My Response: " + myMessage)
                        myMessage = kernel.respond(message)
                        Send_message(myMessage)
    
                    for l in parts:
                        if "End of /NAMES list" in l:
                            MODT = True