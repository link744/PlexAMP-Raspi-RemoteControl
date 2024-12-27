
Hardware required:
1. Raspi 4 4GB (other versions should work)
2. IR sensor
3. IR Remote control

This set of scripts does a few things:
1. plexamp.service can be used to automatically run PlexAmp on 
2. remote.conf is used by lircd.service for config of the remote control
3. plexIRloop.py is the main python script used to read the remote control and send controls to plexamp service
4. plexir.service is used to turn the plexIRloop service on automatically

Pre-reqs:
1. Setup your Raspi with Ubuntu Linux Server (no GUI required). 64bit was tested.
2. Setup your Raspi initially using 'sudo raspi-config' for wifi ec
3. Ensure alsamixer works because that is how the remote controls the volume of the raspi
4. Install PlexAMP according to their instructions including configuration of at 'http://plexampip:32500'
5. Setup the lircd service and ensure it automatically starts upon boot (sudo systemctl enable lircd service)
6. Enable all services above including plexir and check to ensure everything is happy (sudo systemctl status plexamp lircd plexir)

