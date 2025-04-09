
import cv2
from pprint import pprint

from acq_const import CODECS, FRAME_WIDTH, FRAME_HEIGHT, FRAME_RATE


def is_fourcc_available(codec):
    try:
        fourcc = cv2.VideoWriter_fourcc(*codec)
        temp_video = cv2.VideoWriter(
            'temp.mkv', fourcc, FRAME_RATE, 
            (FRAME_WIDTH, FRAME_HEIGHT), isColor=True
            )
        return temp_video.isOpened()
    except:
        return False

def enumerate_fourcc_codecs():
    codecs_to_test = CODECS
    available_codecs = []
    for codec in codecs_to_test:
        available_codecs.append((codec, is_fourcc_available(codec)))
    return available_codecs


if __name__ == '__main__':
    codecs = enumerate_fourcc_codecs()
    print('Available FourCC codecs:')
    print(codecs)