__author__ = 'zhengwang'

import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os
import RPi.GPIO as GPIO
from time import sleep


class CollectTrainingData(object):
    
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # connect to a seral port
       # self.ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
        self.send_inst = True

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):
        
	Motor1A = 24
	Motor1B = 23
	Motor2A = 2
	Motor2B = 3
	Motor1E = 25
        GPIO.setmode(GPIO.BCM)                          # GPIO Numbering
        GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(Motor1B,GPIO.OUT)
        GPIO.setup(Motor2A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(Motor2B,GPIO.OUT)
        GPIO.setup(Motor1E,GPIO.OUT)

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
	    direction=1
	    while frame <= 90 :
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    #print("came 1") 
                    # select lower half of the image
                    roi = image[120:240, :]
                    
                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                    
                    #cv2.imshow('roi_image', roi)
                    cv2.imshow('image', image)
                    
                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    
                    frame += 1
                    total_frame += 1
		    print(frame)
                    # simple orders
                    if direction == 1:
                           	        print("Forward")
					GPIO.output(Motor1A,GPIO.HIGH)
			                GPIO.output(Motor1B,GPIO.LOW)
                			GPIO.output(Motor2A,GPIO.HIGH)
                			GPIO.output(Motor2B,GPIO.LOW)
                			GPIO.output(Motor1E,GPIO.HIGH)
                               	        saved_frame += 1
                              	        image_array = np.vstack((image_array, temp_array))
                                        label_array = np.vstack((label_array, self.k[2]))
                                        #self.ser.write(chr(1))

                    elif direction == 2:
                                	print("Reverse")
					GPIO.output(Motor1A,GPIO.LOW)
                			GPIO.output(Motor1B,GPIO.HIGH)
                			GPIO.output(Motor2A,GPIO.LOW)
                			GPIO.output(Motor2B,GPIO.HIGH)
                			GPIO.output(Motor1E,GPIO.HIGH)
                                	saved_frame += 1
                                	image_array = np.vstack((image_array, temp_array))
                               	 	label_array = np.vstack((label_array, self.k[3]))
                                	#self.ser.write(chr(2))
                            
                    elif direction == 3:
                                	print("Left")
					GPIO.output(Motor1A,GPIO.HIGH)
                			GPIO.output(Motor1B,GPIO.LOW)
                			GPIO.output(Motor2A,GPIO.LOW)
                			GPIO.output(Motor2B,GPIO.HIGH)
                			GPIO.output(Motor1E,GPIO.HIGH)
                                	image_array = np.vstack((image_array, temp_array))
                                	label_array = np.vstack((label_array, self.k[0]))
                                	saved_frame += 1
                               		 #self.ser.write(chr(3))

                    elif direction == 4:
                                	print("Right")
					GPIO.output(Motor1A,GPIO.LOW)
                			GPIO.output(Motor1B,GPIO.HIGH)
                			GPIO.output(Motor2A,GPIO.HIGH)
                			GPIO.output(Motor2B,GPIO.LOW)
                			GPIO.output(Motor1E,GPIO.HIGH)
                               	 	image_array = np.vstack((image_array, temp_array))
                                	label_array = np.vstack((label_array, self.k[1]))
                                	saved_frame += 1
                                	#self.ser.write(chr(4))
	       	    else:
					print("invalid input Usage:1-Forward 2-Reverse 3-Left 4-Right")


            # save training images and labels
	    print 'training started'
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
	    print(directory)
	    print(file_name)
            #if not os.path.exists(directory):
            #    os.makedirs(directory)
            try:    
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame

        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
	
	try:
    		CollectTrainingData()
        except KeyboardInterrupt:
                GPIO.output(Motor1E,GPIO.LOW)
                GPIO.cleanup()

    
