# RemotePicamera
Initial simple client/server Raspberry Pi Camera 

To Install
=========
  * Make sure that Raspberry Pi camaera is attached and enabled. Use raspistill to capture
  * Make sure that python is installed 
  `python -v`
  should return something like
  `Python 2.7.9 (default, Mar  8 2015, 00:52:26)`
  *Install picamera: sudo apt-get install python-picamera

To Run
======

The order is important here. The client software exits if it can't find the server - so launch the server first.

On Server:
`python imageListener.py`

On Raspberry Pi:
  * Get the IP address of the server
  * Enter the server IP address in raspberryPiRemote.py
  * `python raspberryPiRemote.py`

