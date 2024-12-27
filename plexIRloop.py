

baseurl = 'http://192.168.0.113:32400' #TODO: this is the location of your Plex server 
token = 'INSERT_TOKEN_HERE'#TODO: this is the Token for your Plex server
clientNameForThisScript = "KitchenOrginal" #TODO: this is the name of the PlexAMP this is meant to control

from lirc import RawConnection #this is required to communicate to  IR
import signal
import pyttsx3 #this is for the next to speech module
from subprocess import call
from plexapi.server import PlexServer
import time
from time import sleep, gmtime, strftime 

plex = PlexServer(baseurl, token)
print(plex)
print(plex.clients())
plexRandom = False #to turn on random shuffle

for client in plex.clients():
    print(client.title)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

#************HANDLER OF IR ACTION START************************************

def takePlexAction(action):
    cars = plex.library.section('Music').playlist('Kitchen Tunes')
    motownPlaylist = plex.library.section('Music').playlist('Motown')
    sixtiesPlaylist = plex.library.section('Music').playlist('Best 60s')
    recentPlaylist = plex.library.section('Music').playlist('Recently Added')
    allPlaylist = plex.library.section('Music').playlist('All Music')

    #print(cars.title)
    client = plex.client(clientNameForThisScript)

    if (action=="KEY_VOLUMEUP"):
          print("You pressed volume up!")
          #use client.setVolume(volume=100) #pass a value from 0 too 100 
          #amixer -c 0 set Headphone 2dB+
          call(['amixer', '-q', '-c', '0', 'set', 'PCM', '2dB+'], shell=False) #used to be Headphone not PCM
    elif action=="KEY_PLAY" or action=="KEY_POWER":
          print("You pressed the Play button!")
          if client.isPlayingMedia(includePaused = False) == True: #do not count paused as playing
             #print("client is playing music, so I will pause")
             client.pause()
          else:
             #client.playMedia(cars)
             #print("client is NOT playing music, so I will play")
             #add another line here, 
             if client.isPlayingMedia(includePaused = True) == False:
                   #print("nothing to resume so play new list")
                   client.playMedia(cars)
                   #client.playMedia(boysPlaylist)
                   #client.play()
             else:
                   #print("resuming playlist....")
                   client.play()
    elif (action=="KEY_VOLUMEDOWN"):
          print("You pressed the volume down button!")
          #use client.setVolume(volume=90) #pass a value from 0 to 100
          #amixer -c 0 set Headphone 2dB-
          #call(['shutdown', '-h', 'now'], shell=False)
          call(['amixer', '-q', '-c', '0', 'set', 'PCM', '2dB-'], shell=False)
    elif (action=="KEY_NEXT"):
          print("You pressed the next button!")
          client.skipNext()
    elif (action=="KEY_PREVIOUS"):
          print("You pressed the previous button!")
          client.skipPrevious()
    elif (action=="KEY_EQUAL"):  
          global plexRandom 
          plexRandom = not plexRandom
          print("Setting Random to :")
          print(int(plexRandom))  
          client.setShuffle(int(plexRandom))
    elif (action=="KEY_9"):
          sayThis("You pressed 9")
    elif (action=="KEY_8"):
          sayThis("You pressed 8")
    elif (action=="KEY_7"):
          sayThis("You pressed 7")
    elif (action=="KEY_6"):
          sayThis("You pressed 6")
    elif (action=="KEY_5"):
          sayThis("You pressed 5")
    elif (action=="KEY_4"):
          sayThis("Here is the all motown playlist")
          client.playMedia(motownPlaylist)
          client.play()
    elif (action=="KEY_3"):
          sayThis("Here is the 60s playlist")
          client.playMedia(sixtiesPlaylist)
          client.play()
    elif (action=="KEY_2"):
          sayThis("Here is the all music playlist")
          client.playMedia(allPlaylist)
          client.play()
    elif (action=="KEY_1"):
          sayThis("Here is the recent playlist.")
          client.playMedia(recentPlaylist)
          client.play()
    elif (action=="KEY_0"):
          sayThis("Here is the all music playlist")
          client.playMedia(allPlaylist)
          client.play()
    else:
          sayThis("Hello")
          print("No action defined yet for..")
          print(action)


#****************HANDLER OF IR ACTION END****************************************

#****************WEATHER START*****************

import asyncio
import python_weather
from python_weather.forecast import CurrentForecast, DailyForecast

F = python_weather.IMPERIAL

def render_current(x: CurrentForecast) -> str:
    #return f"{x.temperature}°{F}, {x.description}."
    return f"It is {x.temperature} outside and {x.description}."

async def print_weather():
    async with python_weather.Client(format=F) as client:
        weather = await client.get("Chicago")
        print(render_current(weather.current))
        sayThis(render_current(weather.current))
        
#if __name__ == '__main__':
#    asyncio.run(print_weather())


#*************WEATHER END**************************


#*************SPEAKING START***********************

def sayThis(sayThisText):
  engine = pyttsx3.init()
  engine.setProperty('rate', 120)
  engine.setProperty('volume',1.0)
  #sayThisText = "It is " + str(weather.current.temperature) + " degrees outside in Chicago right now."
  #sayThisText = "Hello world!"
  engine.say(sayThisText)
  engine.runAndWait()
  return True

#**************SPEAKING END***********************

#*************PLAY/PAUSE LOGIC START**************

def playPauseButtonPress():
    if client.isPlayingMedia(includePaused = False) == True: #do not count paused as playing
         print("client is playing music, so I will pause")
         client.pause()
    else:
         #client.playMedia(cars)
         print("client is NOT playing music, so I will play")
         #add another line here, 
         if client.isPlayingMedia(includePaused = True) == False:
               print("nothing to resume so play new list")
               client.playMedia(cars)
         else: 
               print("resuming playlist....")
               client.play()

#*************PLAY/PAUSE LOGIC END****************


#************MAIN IR LOOP START*******************

def ProcessIRRemote():
       
    #get IR command
    #keypress format = (hexcode, repeat_num, command_key, remote_id)
    try:
        keypress = conn.readline(.0001)
    except:
        keypress=""
              
    if (keypress != "" and keypress != None):
                
        data = keypress.split()
        sequence = data[1]
        command = data[2]
        
        #ignore command repeats
        if (sequence != "00"):
           return

        #print(command)
        takePlexAction(command)

#**********MAIN IR LOOP END************************

#*********MAIN LOOP START**************************
        
            
#define Global
conn = RawConnection()
print("Starting Up...\n")
interrupted = False

while True:         
      ProcessIRRemote()
      time.sleep(0.01)
      if interrupted:
        print("Gotta go.....\n")
        break

#*********MAIN LOOP END******************************

