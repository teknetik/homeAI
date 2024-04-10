import logging
import asyncio
import os

from common.tools import whisperTools
from common.tools import mp3Player

if os.getenv("LLM_MODEL") == "groq":
    from stream_groq import chat_completion
else:
    from stream import chat_completion

logger = logging.getLogger(__name__)


def agent(recorder, memory):

    recorder.stop()
    mp3Player.play_mp3("./common/agents/mp3/listen.mp3")
    recorder.start()
    logger.info("Waiting for speech")
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
                    full_response = asyncio.run(chat_completion(transcription.text))
                    logger.info(full_response)
                except Exception as e:
                    logger.info(e)
                    pass
                # Restart the recorder after audio has been played
                recorder.start()
        else:
            # If no speech was detected
            pass
            # logger.info("No speech detected, skipping this cycle.")
