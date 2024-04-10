import os
import pvporcupine
import logging
from datetime import datetime


# Set up logging
logger = logging.getLogger(__name__)
porcupine_access_key = os.getenv("PORCUPINE_ACCESS_KEY")

def listen(keyword_paths, recorder):
    try:
        porcupine = pvporcupine.create(
            access_key=porcupine_access_key,
            keyword_paths=keyword_paths,
        )
    except pvporcupine.PorcupineActivationError as e:
        logger.info("AccessKey activation error")
        raise e
    except pvporcupine.PorcupineActivationLimitError as e:
        logger.info("AccessKey has reached it's temporary device limit")
        raise e
    except pvporcupine.PorcupineActivationRefusedError as e:
        logger.info("AccessKey refused")
        raise e
    except pvporcupine.PorcupineActivationThrottledError as e:
        logger.info("AccessKey has been throttled")
        raise e
    except pvporcupine.PorcupineError as e:
        logger.info("Failed to initialize Porcupine")
        raise e

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace(".ppn", "").split("_")
        if len(keyword_phrase_part) > 6:
            keywords.append(" ".join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])

    logger.info("Porcupine version: %s" % porcupine.version)
    logger.info("Listening ... (press Ctrl+C to exit)")
    recorder.start()

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                logger.info(
                    "[%s] Detected %s" % (str(datetime.now()), keywords[result])
                )
                return True
    except KeyboardInterrupt:
        logger.info("Stopping ...")

    finally:
        recorder.stop()
        porcupine.delete()
        return False


