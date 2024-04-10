from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import time
import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "dhyOxsTWJRMmlB8yowNT"
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def stream_to_speakers(text) -> None:

    audio_stream = client.generate(
          text=text,
          stream=True
        )
    stream(audio_stream)


if __name__ == "__main__":
    text = """I see skies of blue and clouds of white
                    The bright blessed days, the dark sacred nights
                    And I think to myself
                    What a wonderful world"""
    stream_to_speakers(text)
