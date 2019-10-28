################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
import numpy as np
import pandas as pd
from datetime import datetime



current = datetime.now().strftime('%Y%m%d%H%M%S')
label = 1
Thumb_fin_meta_direction_x = []
Thumb_fin_meta_direction_y = []
Thumb_fin_meta_direction_z = []
Thumb_fin_prox_direction_x = []
Thumb_fin_prox_direction_y = []
Thumb_fin_prox_direction_z = []
Thumb_fin_inter_direction_x = []
Thumb_fin_inter_direction_y = []
Thumb_fin_inter_direction_z = []
Thumb_fin_dist_direction_x = []
Thumb_fin_dist_direction_y = []
Thumb_fin_dist_direction_z = []
label_list = []

def getch():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)  

class SampleListener(Leap.Listener):
    finger_names = ['Thumb'] #thumb only
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        
        
        frame = controller.frame()
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        
        
        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)


            # Get fingers

            for finger in hand.fingers:

                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                        self.bone_names[bone.type],
                        bone.prev_joint,
                        bone.next_joint,
                        bone.direction)

                    if self.finger_names[finger.type] == 'Thumb':
                        if self.bone_names[bone.type] == 'Metacarpal':
                            Thumb_fin_meta_direction_x.append(bone.speed.x)
                            Thumb_fin_meta_direction_y.append(bone.speed.y)
                            Thumb_fin_meta_direction_z.append(bone.speed.z)
                        if self.bone_names[bone.type] == 'Proximal':
                            Thumb_fin_prox_direction_x.append(bone.direction.x)
                            Thumb_fin_prox_direction_y.append(bone.direction.y)
                            Thumb_fin_prox_direction_z.append(bone.direction.z)
                        if self.bone_names[bone.type] == 'Intermediate':
                            Thumb_fin_inter_direction_x.append(bone.direction.x)
                            Thumb_fin_inter_direction_y.append(bone.direction.y)
                            Thumb_fin_inter_direction_z.append(bone.direction.z)
                        if self.bone_names[bone.type] == 'Distal':
                            Thumb_fin_dist_direction_x.append(bone.direction.x)
                            Thumb_fin_dist_direction_y.append(bone.direction.y)
                            Thumb_fin_dist_direction_z.append(bone.direction.z)
            label_list.append(label)
        if not frame.hands.is_empty:
            print ""
        

def data_save_pandas():
    df = pd.DataFrame({
        "Thumb_fin_meta_direction_x" : Thumb_fin_meta_direction_x,
        "Thumb_fin_meta_direction_y" : Thumb_fin_meta_direction_y,
        "Thumb_fin_meta_direction_z" : Thumb_fin_meta_direction_z,
        "Thumb_fin_prox_direction_x" : Thumb_fin_prox_direction_x,
        "Thumb_fin_prox_direction_y" : Thumb_fin_prox_direction_y,
        "Thumb_fin_prox_direction_z" : Thumb_fin_prox_direction_z,
        "Thumb_fin_inter_direction_x" : Thumb_fin_inter_direction_x,
        "Thumb_fin_inter_direction_y" : Thumb_fin_inter_direction_y,
        "Thumb_fin_inter_direction_z" : Thumb_fin_inter_direction_z,
        "Thumb_fin_dist_direction_x" : Thumb_fin_dist_direction_x,
        "Thumb_fin_dist_direction_y" : Thumb_fin_dist_direction_y,
        "Thumb_fin_dist_direction_z" : Thumb_fin_dist_direction_z,
        "label" : label_list,
    })
    df.to_csv("./{0}_{1}.csv".format(current, str(label)))

def main():
    # Create a sample listener and controller
    key = ord(getch())
    if key == 27:#esc
        print "m"
    elif key == 13:#enter
        print "m"
    elif key == 224: 
        key = ord(getch())
        if key == 80: #up
            print "m"
        elif key == 72: #down
            print "m"
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
        data_save_pandas()
    
    
    

            

if __name__ == "__main__":
    main()
