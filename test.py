
from __future__ import print_function

import io
import logging
import os
import subprocess
import sys
import cv2 
import numpy as np
from PIL import Image

import gphoto2 as gp


def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    # required configuration will depend on camera type!
    print('Checking camera config')
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera))
    # find the image format config item
    OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
    if OK >= gp.GP_OK:
        # get current setting
        value = gp.check_result(gp.gp_widget_get_value(image_format))
        # make sure it's not ra
    # find the capture size class config item
    # need to set this on my Canon 350d to get preview to work at all
    OK, capture_size_class = gp.gp_widget_get_child_by_name(
        config, 'capturesizeclass')
    if OK >= gp.GP_OK:
        # set value
        value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
        gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
        # set config
        gp.check_result(gp.gp_camera_set_config(camera, config))
    # capture preview image (not saved to camera memory card)
    print('Capturing preview image')
    while True:
        camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        # display image

        ds = io.BytesIO(file_data)
        file_bytes = np.asarray(bytearray(ds.read()), dtype=np.uint8)
        print(file_bytes)
        print(np.shape(file_bytes))
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        print(img)
        res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('test', res)
        k = cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
        #image = Image.open(io.BytesIO(file_data))
        #image.show(command="fim")
        gp.check_result(gp.gp_camera_exit(camera))
    

if __name__ == "__main__":
    sys.exit(main())