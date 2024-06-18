#!/usr/bin/env python
"""
BlueRov video capture class
"""

import cv2
import gi
import numpy as np
import sys
import os
import io
from pymavlink import mavutil
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst

#  https://machinelearningknowledge.ai/learn-object-tracking-in-opencv-python-with-code-examples/

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
print('version:{}'.format(cv2.__version__))

# Create the connection
master = mavutil.mavlink_connection('udpin:192.168.2.1:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Arm
# master.arducopter_arm() or:
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)

# wait until arming confirmed (can manually check with master.motors_armed())
print("Waiting for the vehicle to arm")
master.motors_armed_wait()
print('Armed!')

buttons = None

ROVControl = (
    master.target_system,
    0,
    0,
    500,
    0,
    buttons)

class track_object():    
    def __init__(self):
        # Set up tracker.
        # Instead of MIL, you can also use
 
        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        tracker_type = tracker_types[7]
     
        if int(minor_ver) < 3:        
            tracker = cv2.Tracker_create(tracker_type)        
        else:
            print('Tracker_create2')
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            if tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            if tracker_type == "CSRT":
                tracker = cv2.TrackerCSRT_create()

        self.tracker = tracker #cv2.TrackerCSRT_create()
        self.first_frame = True
        self.tracker_type = tracker_type

        # Define an initial bounding box
        self.bbox = (287, 23, 86, 320)

    # capture from camera
    def track_frame(self, frame):
        
        #frame = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY)
        is_success, buffer = cv2.imencode(".jpg", frame)
        io_buf = io.BytesIO(buffer)

        # decode
        frame = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
        '''cv2.imwrite('test.jpg', frame)
        frame = cv2.imread('/home/sscrov/Downloads/test.jpg')
        os.remove('/home/sscrov/Downloads/test.jpg')'''
        width = np.size(frame, 1) #get width of image
        height = np.size(frame, 0) #get height of image
        #print('frame:',len(frame),str(frame),'size:',width,' ', height)
        #print(frame.flags['C_CONTIGUOUS'])
        #cv2.imshow("Tracking", frame)  
        #return
        #print('frame,',frame)
        if self.first_frame:            
            #print("line 59")
            # Uncomment the line below to select a different bounding box
            self.bbox = cv2.selectROI(frame, False)
            #print("line 62")
            # Initialize tracker with first frame and bounding box
            ok = self.tracker.init(frame, self.bbox)
            #print('init:', ok)

            #if ok:
            self.first_frame = False
            #print('ok:',ok)
        else:

            # Start timer
            timer = cv2.getTickCount()
     
            # Update tracker
            ok, self.bbox = self.tracker.update(frame)
            #print("line 77")
            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
     
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                cv2.rectangle(frame, p1, p2, (0,0,255), 2, 3)
                print(frame.shape[:2])
                p1x, p1y = p1
                p2x, p2y = p2
                center = ((p1x+p2x)/2,(p1y+p2y)/2)
                #print("p1:", p1)
                #print("p2:", p2)
            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
     
            # Display tracker type on frame
            cv2.putText(frame, self.tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
         
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
     
            # Display result
            cv2.imshow("Tracking", frame)         



class RovVideo():
    """BlueRov video capture class constructor

    Attributes:
        port (int): Video UDP port
        video_codec (string): Source h264 parser
        video_decode (string): Transform YUV (12bits) to BGR (24bits)
        video_pipe (object): GStreamer top-level pipeline
        video_sink (object): Gstreamer sink element
        video_sink_conf (string): Sink configuration
        video_source (string): Udp source ip and port
        latest_frame (np.ndarray): Latest retrieved video frame
    """

    def __init__(self, port=5600):
        """Summary

        Args:
            port (int, optional): UDP port
        """

        Gst.init(None)

        self.port = port
        self.latest_frame = self._new_frame = None

        # [Software component diagram](https://www.ardusub.com/software/components.html)
        # UDP video stream (:5600)
        self.video_source = 'udpsrc port={}'.format(self.port)
        # [Rasp raw image](http://picamera.readthedocs.io/en/release-0.7/recipes2.html#raw-image-capture-yuv-format)
        # Cam -> CSI-2 -> H264 Raw (YUV 4-4-4 (12bits) I420)
        self.video_codec = '! application/x-rtp, payload=96 ! rtph264depay ! h264parse ! avdec_h264'
        # Python don't have nibble, convert YUV nibbles (4-4-4) to OpenCV standard BGR bytes (8-8-8)
        self.video_decode = \
            '! decodebin ! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert'
        # Create a sink to get data
        self.video_sink_conf = \
            '! appsink emit-signals=true sync=false max-buffers=2 drop=true'

        self.video_pipe = None
        self.video_sink = None

        self.run()

    def start_gst(self, config=None):
        """ Start gstreamer pipeline and sink
        Pipeline description list e.g:
            [
                'videotestsrc ! decodebin', \
                '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                '! appsink'
            ]

        Args:
            config (list, optional): Gstreamer pileline description list
        """

        if not config:
            config = \
                [
                    'videotestsrc ! decodebin',
                    '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                    '! appsink'
                ]

        command = ' '.join(config)
        self.video_pipe = Gst.parse_launch(command)
        self.video_pipe.set_state(Gst.State.PLAYING)
        self.video_sink = self.video_pipe.get_by_name('appsink0')

    @staticmethod
    def gst_to_opencv(sample):
        """Transform byte array into np array

        Args:
            sample (TYPE): Description

        Returns:
            TYPE: Description
        """
        buf = sample.get_buffer()
        caps_structure = sample.get_caps().get_structure(0)
        array = np.ndarray(
            (
                caps_structure.get_value('height'),
                caps_structure.get_value('width'),
                3
            ),
            buffer=buf.extract_dup(0, buf.get_size()), dtype=np.uint8)
        return array

    def frame(self):
        """ Get Frame

        Returns:
            np.ndarray: latest retrieved image frame
        """
        if self.frame_available:
            self.latest_frame = self._new_frame
            # reset to indicate latest frame has been 'consumed'
            self._new_frame = None
        return self.latest_frame

    def frame_available(self):
        """Check if a new frame is available

        Returns:
            bool: true if a new frame is available
        """
        return self._new_frame is not None

    def run(self):
        """ Get frame to update _new_frame
        """

        self.start_gst(
            [
                self.video_source,
                self.video_codec,
                self.video_decode,
                self.video_sink_conf
            ])

        self.video_sink.connect('new-sample', self.callback)

    def callback(self, sink):
        sample = sink.emit('pull-sample')
        self._new_frame = self.gst_to_opencv(sample)

        return Gst.FlowReturn.OK

def rov_main():
    # Create the video object
    # Add port= if is necessary to use a different one
    video = RovVideo()

    print('Initialising stream...')
    waited = 0
    while not video.frame_available():
        waited += 1
        print('\r  Frame not available (x{})'.format(waited), end='')
        cv2.waitKey(30)
    print('\nSuccess!\nStarting streaming - press "q" to quit.')

    track = track_object()
    frame_num=0
    while True:
        
        # Wait for the next frame to become available
        if video.frame_available():
            # Only retrieve and display a frame if it's new
            frame = video.frame()
            #print(frame,"_frame")
            if frame_num > 30:
                track.track_frame(frame)
            else:
                frame_num += 1
            #print('succeed track')
            #cv2.imshow('frame', frame)
        # Allow frame to display, and check if user wants to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
def rov_main_test():
    # Create the video object
    # Add port= if is necessary to use a different one
    video = RovVideo()#cv2.VideoCapture(r"/home/sscrov/Downloads/2024-04-20_10.43.04.mkv")

    print('Initialising stream...')
    waited = 0
    while not video.frame_available():
        waited += 1
        print('\r  Frame not available (x{})'.format(waited), end='')
        cv2.waitKey(30)
    print('\nSuccess!\nStarting streaming - press "q" to quit.')

    track = track_object()
    frame_num=0
    while True:
        
        # Wait for the next frame to become available
        if video.frame_available():
            # Only retrieve and display a frame if it's new
        
            frame = video.frame()
                #print(frame,"_frame")
            if frame_num > 30:
                track.track_frame(frame)
            else:
                frame_num += 1
                print(frame_num)
            #print('succeed track')
                #cv2.imshow('frame', frame)
            # Allow frame to display, and check if user wants to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
def test():
    track = track_object()
    
    video = cv2.VideoCapture(r"/home/sscrov/Downloads/2024-04-20_10.43.04.mkv")

    ok,frame=video.read()
    #bbox = cv2.selectROI(frame)
    #ok = tracker.init(frame,bbox)
    print("what is this")
    print(video.read())
    while True:
        ok,frame=video.read()
        
        '''
        if not ok:
            break
        ok,bbox=tracker.update(frame)
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
        else:
            cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow('Tracking',frame)
        '''

        track.track_frame(frame)
        if cv2.waitKey(1) & 0XFF==27:
            break
        
        
        #time.sleep(500)

if __name__ == '__main__':
    #test()
    rov_main_test()
    cv2.destroyAllWindows()
