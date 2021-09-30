import json
import logging
import sys


class Config:
    def __init__(self):
        with open("./config.json", "r") as file:
            self._config_dict = json.load(file)

    def get_output_path(self):
        try:
            return self._config_dict["output_path"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load output path", ex)

    def get_debug(self):
        try:
            return self._config_dict["debug"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load debug", ex)

    def get_image_show_time_in_s(self):
        try:
            return self._config_dict["image_show_time_in_s"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load image_show_time_in_s", ex)

    def get_serial_port(self):
        try:
            return self._config_dict["serial_port"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load serial_port", ex)
    
    def get_button_height(self):
        try:
            return self._config_dict["button_height"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load button_height", ex)

    def get_base_url(self):
        try:
            return self._config_dict["base_url"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load base_url", ex)
    def get_start_page_png_path(self):
        try:
            return self._config_dict["start_page_png_path"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load start_page_png_path", ex)

    def get_qr_code_png_path(self):
        try:
            return self._config_dict["qr_code_png_path"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load qr_code_png_path", ex)

    def get_asset_path(self):
        try:
            return self._config_dict["asset_path"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load asset_path", ex)

    def get_count_down_time_in_s(self):
        try:
            return self._config_dict["count_down_time_in_s"]
        except KeyError as ex:
            log.log_msg_with_error("couldn't load count_down_time_in_s", ex)

    def setup_logger(self):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root.addHandler(handler)


def get_config():
    return Config()
