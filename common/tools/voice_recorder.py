import logging
from pvrecorder import PvRecorder

logger = logging.getLogger(__name__)


def show_audio_devices():
    for i, device in enumerate(PvRecorder.get_available_devices()):
        logger.info("Device %d: %s" % (i, device))


def listen(deviceIndex):
    recorder = PvRecorder(device_index=deviceIndex,frame_length=256)
    return recorder
