Summary: A way to setup PlexAMP headless on a Raspi and control your raspi using a IR remote control.  The remote control allows volume changes, play pause, skip next/previous, and the nunbers of the remote control can start playlists.  Uses PlexAPI to make this all happen.  Also includes voice feedback via text to speech algo. 

This set of scripts does a few things:
1. plexamp.service can be used to automatically run PlexAmp on 
2. remote.conf is used by lircd.service for config of the remote control
3. plexIRloop.py is the main python script used to read the remote control and send controls to plexamp service
4. plexir.service is used to turn the plexIRloop service on automatically

Hardware required:
1. Raspi 4 4GB (other versions should work)
2. IR sensor*
3. IR Remote control*
* I got both these from here: https://www.amazon.com/gp/product/B01D8KOZF4/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1

Detailed Instructions:
1. Install Rasbian OS 64bit Lite from this website.  You just need a small SD card, 4GB is all.
2. Connect to Wifi, make a user. Here I made user = pi.  Use 'sudo raspi-config' for any details.  Ensure alsamixer works for volume control.
3. Follow PlexAMP instructions to install Install Node JS.
4. Download PlexAmp headless here: https://forums.plex.tv/t/plexamp-on-the-raspberry-pi/791500
5. Run PlexAmp!  Open the URL of your player and signin and make sure everything works.  (ie visiting 'http://IPADDRESS:32500')
6. Create your PlexAmp service....I supplied plexamp.service for this purpose.
7. Enable the service:
$ sudo systemctl daemon-reload
$ sudo systemctl enable plexamp
$ sudo systemctl start plexamp
8. Next stepup the IR remote following these instructions:
https://www.instructables.com/Setup-IR-Remote-Control-Using-LIRC-for-the-Raspber/
9. Im using a egloo remote using the config file in the attached repo orginally found here:
https://github.com/greenring/ElegooRemote/blob/master/elegoo.lircd.conf
10. Now install some dependencies:
 sudo apt update && sudo apt upgrade -y
 sudo apt install python3-pip
 pip install pyttsx
 sudo apt install libespeak1
 pip install PlexAPI
 pip install python-weather
11. Now finally run your plexIRloop.py via python3 to test
12. And turn it into a service 
 sudo cp plexir.service /lib/systemd/system/
 sudo systemctl enable plexir

13. Enable all services above including plexir and check to ensure everything is happy (sudo systemctl status plexamp lircd plexir)

