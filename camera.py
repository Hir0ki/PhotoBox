import gphoto2 as gp
import time
import io
import numpy as np 
import log

class Camera():

    def __init__(self):
        self._connect_to_camera()

    def _connect_to_camera(self):
        is_first_loop_done = False
        while True:
            try: 
                context = gp.Context()
                self.camera = gp.Camera()
                self.camera.init(context)
            except gp.GPhoto2Error as ex:
                if ex == gp.GP_ERROR_MODEL_NOT_FOUND:
                    print("didn't find camera")
                    time.sleep(3)
                    continue
                print(ex)
                continue
            if is_first_loop_done == False:
                print("camera found")
                break
            
            is_first_loop_done = True

    def capture_next_preview_as_np_array(self):
        try:
            preview_file = self.camera.capture_preview()
            preview_path =  gp.check_result(gp.gp_file_get_data_and_size(preview_file))
            return self._convert_camera_to_np_array(preview_path)
        except Exception as error_gp:
            log.log_msg_with_error("Error while capturing the preview", error_gp)
        

    def capture_image(self):
        try:
            return self.camera.capture(gp.GP_CAPTURE_IMAGE)
            
        except Exception as ex:
            log.log_msg_with_error("error while takeing a picture", ex)

    def save_image(self, target_path, camera_file_path):
        try:
            camera_file = self.camera.file_get( camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL)
            target = f'{target_path}/{camera_file_path.name}'
            camera_file.save(target)
            return target            
        except Exception as ex:
            log.log_msg_with_error("error while saving a file", ex)

    def _convert_camera_to_np_array(self, camera_file ):
        try:
            ds = io.BytesIO(camera_file)
            return np.asarray(bytearray(ds.read()), dtype=np.uint8)
        except Exception as error_io:
            log.log_msg_with_error("error while reading picture from camera", error_io)


    def disconnect_camera(self):
        self.camera.exit()
        log.log_msg("exits camera")