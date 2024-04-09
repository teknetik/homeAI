import common.tools.wake_word as wake_word
import common.tools.voice_recorder as voice_recorder
import common.agents.stella as stella
import os
import logging


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Global variables
# Porcupine
keyword_paths = ["./common/agents/stella_en_linux_v3_0_0.ppn"]



def main():
    # Set up the wake word and listen
    sleeping = True
    recorder = voice_recorder.listen()
    while sleeping:
        sleeping = wake_word.listen(keyword_paths, recorder)
        if not sleeping:
            logger.info("Waking up")
    return None


if __name__ == "__main__":
    main()
