import cv2
import os
import time
import platform
import threading
import datetime

class TelloAlexa:
    """Wrapper class to enable the GUI."""

    def __init__(self,tello,outputpath):
        """
        Initial all the element of the GUI,support by Tkinter

        :param tello: class interacts with the Tello drone.

        Raises:
            RuntimeError: If the Tello rejects the attempt to enter command mode.
        """        

        self.tello = tello # videostream device
        self.outputPath = outputpath # the path that save pictures created by clicking the takeSnapshot button 
        self.frame = None  # frame read from h264decoder and used for pose recognition 
        self.thread = None # thread of the Tkinter mainloop
        self.stopEvent = None  
        
        # control variables
        self.distance = 0.1  # default distance for 'move' cmd
        self.degree = 30  # default degree for 'cw' or 'ccw' cmd
        
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = False
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.isBusy = False

        # the sending_command will send command to tello every 5 seconds
        self.sending_command_thread = threading.Thread(target = self._sendingCommand)


    def checkForFaces(self):
        if self.isBusy :
            return
        else:
            self.isBusy = True
            self.tello.takeoff()
            time.sleep(10)
            for x in range(4):
                #rotate 90 degree and take a snap shot
                res = self.tello.rotate_cw(self.degree)
                print("tello sent :",res)
                time.sleep(2)
                #self.takeSnapshot()

            self.tello.land()
            self.isBusy = False

    def takeSnapshot(self):
        """
        save the current frame of the video as a jpg file and put it into outputpath
        """
        # grab the current timestamp and use it to construct the filename
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        print("[INFO] saved {}".format(filename))

    def videoLoop(self):
        """
        The mainloop thread of Tkinter 
        Raises:
            RuntimeError: To get around a RunTime error that Tkinter throws due to threading.
        """

        print("In video loop")
        try:
            faceCascade = cv2.CascadeClassifier('C:\\Users\\aksha\\opencvmodels/haarcascade_frontalface_default.xml')
            # start the thread that get GUI image and drwa skeleton 
            time.sleep(0.5)
            self.sending_command_thread.start()
            while not self.stopEvent:                
                #system = platform.system()

            # read the frame for GUI show
                self.frame = self.tello.read()
                if self.frame is None or self.frame.size == 0:
                    continue 
                #img = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,     
                    scaleFactor=1.2,
                    minNeighbors=5,     
                    minSize=(20, 20)
                )
                print("found %s faces" %len(faces))
                for (x,y,w,h) in faces:
                    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
                    # roi_gray = gray[y:y+h, x:x+w]
                    # roi_color = img[y:y+h, x:x+w] 
            
            # transfer the format from frame to image    
                cv2.imshow('tello stream', gray)
                #cv2.imshow('Face', roi_color)
                key = cv2.waitKey(25) &0xFF
                if key == ord('q'):
                    self.stopEvent = True

            cv2.destroyAllWindows()

                                                         
        except RuntimeError, e:
            self.stopEvent = True
            print("[INFO] caught a RuntimeError")

           

            
    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """    

        while not self.stopEvent:
            self.tello.send_command('command')        
            time.sleep(5)

   
   
    def takeSnapshot(self):
        """
        save the current frame of the video as a jpg file and put it into outputpath
        """

        # grab the current timestamp and use it to construct the filename
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        print("[INFO] saved {}".format(filename))


    def telloTakeOff(self):
        return self.tello.takeoff()                

    def telloLanding(self):
        return self.tello.land()

    def telloFlip_l(self):
        return self.tello.flip('l')

    def telloFlip_r(self):
        return self.tello.flip('r')

    def telloFlip_f(self):
        return self.tello.flip('f')

    def telloFlip_b(self):
        return self.tello.flip('b')

    def telloCW(self, degree):
        return self.tello.rotate_cw(degree)

    def telloCCW(self, degree):
        return self.tello.rotate_ccw(degree)

    def telloMoveForward(self, distance):
        return self.tello.move_forward(distance)

    def telloMoveBackward(self, distance):
        return self.tello.move_backward(distance)

    def telloMoveLeft(self, distance):
        return self.tello.move_left(distance)

    def telloMoveRight(self, distance):
        return self.tello.move_right(distance)

    def telloUp(self, dist):
        return self.tello.move_up(dist)

    def telloDown(self, dist):
        return self.tello.move_down(dist)

