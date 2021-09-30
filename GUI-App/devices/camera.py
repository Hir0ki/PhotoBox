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
                self.context = gp.Context()
                self.camera: gp.gphoto2.camera = gp.Camera()
                self.camera.init(self.context)
                self._set_config_value_checked('iso', 800)
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



    def _set_config_value_checked(self, name, value):
        value = str(value)
        ret = False
        for t in range(0, 20):
            try:
            	config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
            	OK, widget = gp.gp_widget_get_child_by_name(config, name)

            	if OK >= gp.GP_OK:
            		num = None
            		choice_count = gp.check_result(gp.gp_widget_count_choices(widget))
            		logging.info("count %d", choice_count)
            		for i in range(choice_count):
            			vi = gp.check_result(gp.gp_widget_get_choice(widget, i))
            			if vi.lower() == value.lower():
            				num = i
            				value = vi
            				break
            			try:
            				if abs(float(vi) - float(value)) < 0.000001:
            					value = vi
            					num = i
            					break
            			except ValueError:
            				pass
            			try:
            				if '/' in vi:
            					fr = vi.split('/')
            					fr = float(fr[0]) / float(fr[1])
            					if abs(fr - float(value)) < abs(fr * 0.001):
            						value = vi
            						num = i
            						break
            			except:
            				pass
                        
            		if num is not None:
            			logging.info("set %s => %s (choice %d)" % (name, value, num))
            			# set value
            			gp.check_result(gp.gp_widget_set_value(widget, value))
            			ret = True
            		else:
            			logging.info("cant't set %s => %s" % (name, value))
            	# set config
            	gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))
            	break
            except gp.GPhoto2Error as ex:
            	logging.exception('failed')
            	time.sleep(0.1)
            	ret = False
            	continue
            return ret

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
            self._set_config_value_checked('output', 'Off')
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
