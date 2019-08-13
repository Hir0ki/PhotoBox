import gphoto2 as gp
import time

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
