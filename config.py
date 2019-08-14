import json
import log
from os import path 


class Config():

    def __init__(self):
        with open('./config.json', 'r') as file:
            self._config_dict = json.load(file)

    def get_output_path(self):
        try:
            return self._config_dict['output_path']
        except KeyError as ex:
            log.log_msg_with_error("couldn't load output path", ex)