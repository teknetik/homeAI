import asyncio
import websockets
import json
import base64
import shutil
import os
import subprocess
from openai import AsyncOpenAI

# Define API keys and voice ID
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "dhyOxsTWJRMmlB8yowNT"

# Set OpenAI API key
aclient = AsyncOpenAI(api_key=OPENAI_API_KEY)


def is_installed(lib_name):
    return shutil.which(lib_name) is not None


async def stream(audio_stream):
    """Stream audio data using mpv player."""
    if not is_installed("mpv"):
        raise ValueError(
            "mpv not found, necessary to stream audio. Install instructions: https://mpv.io/installation/"
        )

    mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Started streaming audio")
    async for chunk in audio_stream:
        if chunk:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()


async def text_to_speech_input_streaming(voice_id, text_iterator):
    """Send text to ElevenLabs API and stream the returned audio."""
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_turbo_v2"

    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps(
                {
                    "text": " ",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
                    "xi_api_key": ELEVENLABS_API_KEY,
                }
            )
        )

        async def listen():
            """Listen to the websocket for audio data and stream it."""
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("audio"):
                        yield base64.b64decode(data["audio"])
                    elif data.get("isFinal"):
                        break
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break

        listen_task = asyncio.create_task(stream(listen()))

        await websocket.send(
            json.dumps({"text": text_iterator, "try_trigger_generation": True})
        )

        await websocket.send(json.dumps({"text": ""}))

        await listen_task


async def chat_completion(query):
    """Process the chat completion and handle streaming text to TTS,
    and also handle and store data within <data>...</data> tags."""
    response = await aclient.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
            {
                "role": "system",
                "content": 'You are a helpful assistant that responds to questions from the user. You always respond in JSON format which has two keys. "Speech" and "Data". A detailed response to the question should be stored in the "Data" key of the JSON object and wrappered in <data></data> opening/closing tags.. A short conversational version that\'s not too lengthy and can be easily spoken in a few seconds should be stored in "Speech" and the value should be wrapped in opening <speech> and closing </speech> tagh.\nExamples:\n{\n  "Speech": "<speech>Yes, dogs can look up, though their range of motion might be more limited compared to humans.</speech>",\n  "Data": "<data>Dogs are capable of looking up but their neck and skull structure allows a more restricted range of upward vision compared to humans. This means while dogs can definitely look upwards, they won\'t have the same vertical range as humans do, and how high they can look can also depend on the breed and the individual dog’s anatomy.</data>"\n}\n{\n  "Speech": "<speech>Yes, ducks can look up. They have flexible necks that allow them to move their heads in various directions.</speech>",\n  "Data": "<data>Ducks have a good range of motion in their necks, enabling them to look up and around easily. This flexibility helps them stay alert to their surroundings and look for predators or other threats from different angles, including above.</data>"\n}',
            },
            {"role": "user", "content": query},
        ],
        temperature=1,
        stream=True,
    )

    speech_buffer = ""  # Buffer for speech sections
    data_buffer = ""  # Buffer for data sections
    data_storage = []  # List to store data extracted from <data>...</data> tags
    speech_storage = []  # List to store speech extracted from <speech>...</speech> tags
    full_response = {}
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            # Append each chunk to the buffers
            speech_buffer += delta.content
            data_buffer += delta.content

            # Handle <speech> tags
            while "<speech>" in speech_buffer and "</speech>" in speech_buffer:
                start = speech_buffer.index("<speech>") + len("<speech>")
                end = speech_buffer.index("</speech>", start)
                speech_content = speech_buffer[start:end]

                await text_to_speech_input_streaming(VOICE_ID, speech_content.strip())
                speech_storage.append(speech_content.strip())
                speech_buffer = speech_buffer[
                    end + len("</speech>") :
                ].strip()  # Remove processed speech section
                # print(speech_storage)

            # Handle <data> tags
            while "<data>" in data_buffer and "</data>" in data_buffer:
                start = data_buffer.index("<data>") + len("<data>")
                end = data_buffer.index("</data>", start)
                data_content = data_buffer[start:end]

                # Process or store the data content as needed
                data_storage.append(data_content.strip())
                data_buffer = data_buffer[
                    end + len("</data>") :
                ].strip()  # Remove processed data section
                # print(data_storage)

            # For debugging: print buffer content if it's getting too large
            if len(speech_buffer) > 1000 or len(data_buffer) > 1000:
                print("Warning: Buffer is large, might be missing a closing tag.")
                print(f"Speech Buffer: {speech_buffer[:500]}...")
                print(f"Data Buffer: {data_buffer[:500]}...")
    full_response["Speech"] = speech_storage
    full_response["Data"] = data_storage
    # print(json.dumps(full_response, indent=2 ))
    return full_response


# Main execution
if __name__ == "__main__":
    user_query = "Why is the sky blue?"
    asyncio.run(chat_completion(user_query))
