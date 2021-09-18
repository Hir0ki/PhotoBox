import shortuuid
import logging 
from utils.config import Config
from pathlib import Path



class SessionService:

    def __init__(self) -> None:
        self.config = Config()
        self.base_dir: Path = Path(self.config.get_output_path())
        # set alphabet for random uuid's
        shortuuid.set_alphabet("1234567890qwertzuiopasdfghjklyxcvbnm")


    def start_new_session(self): 
        tmp_uuid = shortuuid.ShortUUID().random(length=6)
        while self._check_if_id_is_unique(tmp_uuid) == False:
            tmp_uuid = shortuuid.ShortUUID().random(length=6)
        else:
            self.session_uuid = tmp_uuid
        logging.info(f"Create new session with uuid: {self.session_uuid}")
        self.session_path: Path = self.base_dir.joinpath(self.session_uuid)
        self.session_path.mkdir()
        
        

    def _check_if_id_is_unique(self, uuid: str) -> bool:
        session_uuids = [ x.name for x in self.base_dir.glob("*") if x.is_dir() ]
        for session_uuid in session_uuids:
            if uuid == session_uuid:
                return False
        return True
    
