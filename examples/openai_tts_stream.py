import time
from pathlib import Path
import os
from openai import OpenAI

# Define API keys and voice ID
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Set OpenAI API key
openai = OpenAI(api_key=OPENAI_API_KEY)


def stream_to_speakers(input) -> None:
    import pyaudio

    player_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16, channels=1, rate=24000, output=True
    )

    start_time = time.time()

    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        response_format="pcm",  # similar to WAV, but without a header chunk at the start.
        input=input,
    ) as response:
        print(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms")
        for chunk in response.iter_bytes(chunk_size=1024):
            player_stream.write(chunk)

    print(f"Done in {int((time.time() - start_time) * 1000)}ms.")


if __name__ == "__main__":
    input = """I see skies of blue and clouds of white
                    The bright blessed days, the dark sacred nights
                    And I think to myself
                    What a wonderful world"""
    stream_to_speakers(input)
