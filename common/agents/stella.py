import logging
import asyncio

from common.tools import whisperTools
from common.tools import mp3Player
from stream import chat_completion

logger = logging.getLogger(__name__)


def agent(recorder, memory):

    recorder.stop()
    mp3Player.play_mp3("./common/agents/mp3/listen.mp3")
    recorder.start()

    in_conversation = True

    while in_conversation:
        # While speech is detected, record audio
        talking = whisperTools.voice_detected(recorder.read())
        if talking:
            audio_data = whisperTools.record_until_silence(recorder)
            logger.info("Sending recorded audio to Whisper")
            transcription = whisperTools.transcribe_with_whisper(audio_data)
            # Implement som break words to exit the chat
            if (
                "thank you for watching" in transcription.text.lower()
                or "stop" in transcription.text.lower()
                or "terminate" in transcription.text.lower()
                or "pause" in transcription.text.lower()
            ):
                in_conversation = False
                logger.info("Ending Conversation")
                mp3Player.play_mp3("./common/agents/mp3/sleep.mp3")
                recorder.stop()
            else:
                recorder.stop()
                try:
                    # Generate audio stream from Elevenlabs from the response
                    asyncio.run(chat_completion(transcription.text))
                except Exception as e:
                    logger.info(e)
                    pass
                # Restart the recorder after audio has been played
                recorder.start()
        else:
            # If no speech was detected
            pass
            # logger.info("No speech detected, skipping this cycle.")
