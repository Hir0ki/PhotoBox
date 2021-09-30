import logging
import qrcode
from PIL import ImageQt

class QRCodeService():
    
    
    def __init__(self) -> None:
        pass



    def generade_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=25,
            border=4,
        )

        qr.add_data(data)
        img = qr.make_image()
        logging.info(f"Generate qr code for link: {data}") 
        return ImageQt.ImageQt(img)