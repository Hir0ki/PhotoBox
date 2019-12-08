import gphoto2 as gp
import time
import io
import numpy as np
#from PhotoBox.devices.log import log
import os 
import cv2 
from pathlib import Path

class Camera:
    def __init__(self):
        self._pipe_path = "test"
        self._connect_to_camera()
        
    def _connect_to_camera(self):
        #try:
        pass
        #    os.mkfifo(self._pipe_path)
        #except OSError as oe: 
        #    if oe.errno != errno.EEXIST:
        #        raise

    def capture_next_preview_as_np_array(self):
        """Returns a numpy array with the image in RGB with no transparent channels"""
        return cv2.imread('/home/hir0ki/Projects/PhotoBox/devices/Test_image.png')


    def capture_image(self):
        """Captures image and write it to a file that returns it"""
        return Path('/home/hir0ki/Projects/PhotoBox/devices/test_capture.png')


    def save_image(self, target_path, camera_file_path):
        pass



    def disconnect_camera(self):
        self.camera.exit()
        #log.log_msg("exits camera")

