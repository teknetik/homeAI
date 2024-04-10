#!/usr/bin/env -S poetry run python

import asyncio
import os
from openai import OpenAI, AsyncOpenAI
import openai_tts_stream
# This script assumes you have the OPENAI_API_KEY environment variable set to a valid OpenAI API key.
#
# You can run this script from the root directory like so:
# `python examples/streaming.py`

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
def sync_main() -> None:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="1,2,3,",
        max_tokens=5,
        temperature=0,
        stream=True,
    )

    # You can manually control iteration over the response
    first = next(response)
    print(f"got response data: {first.model_dump_json(indent=2)}")

    # Or you could automatically iterate through all of data.
    # Note that the for loop will not exit until *all* of the data has been processed.
    for data in response:
        print(data.model_dump_json())


async def async_main() -> None:
    client = AsyncOpenAI()
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that responds to questions from the user. You always respond in JSON format which has two keys. \"Speech\" and \"Data\". A detailed response to the question should be stored in the \"Data\" key of the JSON object. A short conversational version that's not too lengthy and can be easily spoken in a few seconds should be stored in \"Speech\" and the value should be wrapped in opening <speech> and closing </speech> tagh.\nExamples:\n{\n  \"Speech\": \"<speech>Yes, dogs can look up, though their range of motion might be more limited compared to humans.</speech>\",\n  \"Data\": \"Dogs are capable of looking up but their neck and skull structure allows a more restricted range of upward vision compared to humans. This means while dogs can definitely look upwards, they won't have the same vertical range as humans do, and how high they can look can also depend on the breed and the individual dog’s anatomy.\"\n}\n{\n  \"Speech\": \"<speech>Yes, ducks can look up. They have flexible necks that allow them to move their heads in various directions.</speech>\",\n  \"Data\": \"Ducks have a good range of motion in their necks, enabling them to look up and around easily. This flexibility helps them stay alert to their surroundings and look for predators or other threats from different angles, including above.\"\n}"
        },
        {
            "role": "user",
            "content": "can hedgehogs roll over?"
        },
    ]
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=True,
    )

    # You can manually control iteration over the response.
    # In Python 3.10+ you can also use the `await anext(response)` builtin instead
    first = await response.__anext__()
    print(f"got response data: {first.model_dump_json(indent=2)}")

    # Or you could automatically iterate through all of data.
    # Note that the for loop will not exit until *all* of the data has been processed.
    async for data in response:
        print(data.choices[0].delta.content)
        await process_tagged_stream_chunked([data.choices[0].delta.content])

async def process_tagged_stream_chunked(stream):
    in_speech_tag = False
    speech_buffer = ""

    async for chunk in stream:
        # Handle partial opening/closing tags split across chunks
        buffer = speech_buffer + chunk
        speech_buffer = ""  # Reset buffer

        while buffer:
            if in_speech_tag:
                # Look for the closing tag in the current buffer
                end_idx = buffer.find("</speech>")
                if end_idx != -1:
                    # Send the chunk before the closing tag to TTS
                    await text_to_speech_input_streaming_chunked(buffer[:end_idx])
                    buffer = buffer[end_idx + len("</speech>"):]  # Skip past closing tag
                    in_speech_tag = False
                else:
                    # Entire buffer is speech content; send to TTS and exit loop to wait for more data
                    await text_to_speech_input_streaming_chunked(buffer)
                    buffer = ""
            else:
                # Look for the next opening tag
                start_idx = buffer.find("<speech>")
                if start_idx != -1:
                    # Found an opening tag; start streaming to TTS from here
                    in_speech_tag = True
                    buffer = buffer[start_idx + len("<speech>"):]  # Skip past opening tag
                else:
                    # No opening tag found in the current buffer; move to next chunk
                    buffer = ""

async def text_to_speech_input_streaming_chunked(text_chunk):
    # This is a placeholder for sending the text chunk to your TTS system.
    # You might need to adjust it to fit your actual TTS streaming interface.
    print("Sending to TTS:", text_chunk)

#sync_main()

asyncio.run(async_main())