import gphoto2 as gp
import time
import io
import logging
import numpy as np
import cv2


class Camera:
    def __init__(self):
        self._connect_to_camera()
        self._init_logging()

    def _init_logging(self):
        self.callback_obj = gp.check_result(
            gp.use_python_logging(
                mapping={
                    gp.GP_LOG_ERROR: logging.INFO,
                    gp.GP_LOG_DEBUG: logging.DEBUG,
                    gp.GP_LOG_VERBOSE: logging.DEBUG - 3,
                    gp.GP_LOG_DATA: logging.DEBUG - 6,
                }
            )
        )

    def _connect_to_camera(self):
        is_first_loop_done = False
        while True:
            try:
                context = gp.Context()
                self.camera = gp.Camera()
                self.camera.init(context)
            except gp.GPhoto2Error as ex:
                if ex == gp.GP_ERROR_MODEL_NOT_FOUND:
                    time.sleep(3)
                    continue
                logging.error("didn't find camera", exc_info=ex)
                continue
            if is_first_loop_done == False:
                logging.info("camera found")
                break

            is_first_loop_done = True

    def capture_next_preview_as_np_array(self):
        try:
            preview_file = self.camera.capture_preview()
            preview_path = gp.check_result(gp.gp_file_get_data_and_size(preview_file))
            img = self._convert_camera_to_np_array(preview_path)
            logging.debug(f"camera preview data: {img} ")
            return cv2.imdecode(img, cv2.IMREAD_COLOR)
        except Exception as ex:
            logging.error(
                f"Error while capturing the preview: {type(ex).__name__}", exc_info=ex
            )

    def capture_image(self, dir_path):
        try:
            logging.info("Capture image")
            cap_img_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            img_path = self.save_image(str(dir_path), cap_img_path)
            return cv2.imread(img_path)

        except Exception as ex:
            logging.error(
                f"error while takeing a picture name: {type(ex).__name__}", exc_info=ex
            )

    def save_image(self, target_path, camera_file_path):
        try:
            logging.info("Save image to disk")
            camera_file = self.camera.file_get(
                camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL
            )
            target = f"{target_path}/{camera_file_path.name}"
            camera_file.save(target)
            logging.info("Saved image to disk")
            return target
        except Exception as ex:
            logging.error(
                f"error while saving a file name: {type(ex).__name__}", exc_info=ex
            )

    def _convert_camera_to_np_array(self, camera_file):
        try:
            ds = io.BytesIO(camera_file)
            return np.asarray(bytearray(ds.read()), dtype=np.uint8)
        except Exception as error_io:
            logging.error("error while reading picture from camera", exc_info=error_io)

    def disconnect_camera(self):
        self.camera.exit()
        logging.info("exits camera")
