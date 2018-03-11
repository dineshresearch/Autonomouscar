import RPi.GPIO as GPIO
from time import sleep


# Pins for Motor Driver Inputs
Motor1A = 24
Motor1B = 23
Motor2A = 2
Motor2B = 3
Motor1E = 25

def setup():
        GPIO.setmode(GPIO.BCM)                          # GPIO Numbering
        GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(Motor1B,GPIO.OUT)
        GPIO.setup(Motor2A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(Motor2B,GPIO.OUT)
        GPIO.setup(Motor1E,GPIO.OUT)

#def picam():
#        sudo python raspberryPiRemote.py 

def loop(direction):
        	# Going forwards
        if direction == 1:
        	GPIO.output(Motor1A,GPIO.HIGH)
        	GPIO.output(Motor1B,GPIO.LOW)
        	GPIO.output(Motor2A,GPIO.HIGH)
        	GPIO.output(Motor2B,GPIO.LOW)
        	GPIO.output(Motor1E,GPIO.HIGH)
        	#sleep(3)
	elif direction == 2:
        	# Going backwards
        	GPIO.output(Motor1A,GPIO.LOW)
        	GPIO.output(Motor1B,GPIO.HIGH)
        	GPIO.output(Motor2A,GPIO.LOW)
        	GPIO.output(Motor2B,GPIO.HIGH)
        	GPIO.output(Motor1E,GPIO.HIGH)
        	#sleep(5)
	elif direction == 3:
        	# Going left
        	GPIO.output(Motor1A,GPIO.HIGH)
        	GPIO.output(Motor1B,GPIO.LOW)
       		GPIO.output(Motor2A,GPIO.LOW)
        	GPIO.output(Motor2B,GPIO.HIGH)
        	GPIO.output(Motor1E,GPIO.HIGH)
        	#sleep(3)
	elif direction == 4:
        	# Going right
        	GPIO.output(Motor1A,GPIO.LOW)
        	GPIO.output(Motor1B,GPIO.HIGH)
        	GPIO.output(Motor2A,GPIO.HIGH)
        	GPIO.output(Motor2B,GPIO.LOW)
        	GPIO.output(Motor1E,GPIO.HIGH)
        	#sleep(3)
	else:
		print('please enter a valid number')

def stop():
        # Stop
        GPIO.output(Motor1E,GPIO.LOW)

def destroy():
        GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
        setup()
#        picam()
        try:
	    while True:
            	direction = input('Enter the direction: ')
            	loop(direction)
	    	#stop()
	    	#destroy()
        except KeyboardInterrupt:
		GPIO.output(Motor1E,GPIO.LOW)
                destroy()


