import common.tools.wake_word as wake_word
import common.tools.voice_recorder as voice_recorder
import common.agents.stella as stella
from langchain.memory import ConversationBufferMemory
import logging


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Global variables
# Porcupine
keyword_paths = ["./common/agents/stella_en_linux_v3_0_0.ppn"]


def main():
    # Set up the wake word and listen
    sleeping = True
    recorder = voice_recorder.listen()
    # instantiate langchain memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    while sleeping:
        sleeping = wake_word.listen(keyword_paths, recorder)
        if not sleeping:
            logger.info("Waking up")
            recorder.start()
            stella.agent(recorder, memory)
            sleeping = True
    return None


if __name__ == "__main__":
    main()
