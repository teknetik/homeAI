import os
import time
import requests
import logging

#from common.tools import whisperTools
#from common.tools import mp3Player

from langchain_community.chat_models import ChatOpenAI

from datetime import datetime


logger = logging.getLogger(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")
logger.info("OpenAI API Key: " + openai_api_key)


def agent(recorder, memory):
    role = """
    You are an AI assistant called stella.
    Your role is to provide short conversational answers to questions or tasks given by the user.
    Provide responses that dont provide a large amount of detail and could be spoken out loud in a few seconds.
    """
    model = "gpt-4"
    recorder.stop()
    mp3Player.play_mp3("./common/agents/Grace/how_can_i_help.mp3")
    recorder.start()
    time.sleep(0.1)

    waiting_voice = [
        "processing",
        "calculating",
        "analyzing",
        "working on it",
        "evaluating",
        "fetching data",
        "give me a moment",
        "looking into that",
        "let me think",
        "retrieving answer",
        "hold on",
        "just a second",
        "querying that",
        "bringing up the info",
    ]
    # Updates the HTML frontend
    def api(endpoint, event):
        url = "http://localhost:5000/" + endpoint
        headers = {"Content-Type": "application/json"}
        data = {"event": event}
        requests.post(url, json=data, headers=headers)
        return None

    api("mic", "on")

    in_conversation = True
    while in_conversation:
        talking = whisperTools.voice_detected(recorder.read())
        if talking:
            audio_data = whisperTools.record_until_silence(recorder)
            now = str(datetime.now())
            print(now + " Sending recorded audio to Elevenlabs")
            transcription = whisperTools.transcribe_with_whisper(audio_data)
            now = str(datetime.now())
            print(now + " Transcription:", transcription)
            if "thank you for watching" in transcription:
                in_conversation = False
                print("Ending Conversation")
                api("mic", "off")
            if (
                "stop" in transcription
                or "terminate" in transcription
                or "pause" in transcription
            ):
                in_conversation = False
                print("Ending Conversation")
                api("mic", "off")
                mp3Player.play_mp3("./common/agents/Grace/end_convo.mp3")
            else:
                # Pick a random phrase from the list
                #selected_phrase = random.choice(waiting_voice)
                api("spinner", "on")
                # If there are spaces in the phrase, replace them with underscores
                #if " " in selected_phrase:
                    #selected_phrase = selected_phrase.replace(" ", "_")
                #print("Selected Phrase: " + selected_phrase)
                # Stop the recorder while playing the audio
                recorder.stop()
                #mp3Player.play_mp3("./agents/Grace/" + selected_phrase + ".mp3")

                # Send the user message to the LLM
                gpt_response = stella_chain(transcription, role, model, memory)
                now = str(datetime.now())
                print(now + " Full response:")
                print(gpt_response)
                print("\n\n")
                api("spinner", "off")
                # Send the response to the server
                url = "http://localhost:5000/send-text"
                headers = {"Content-Type": "application/json"}
                data = {"text": gpt_response}

                try:
                    response = requests.post(url, json=data, headers=headers)
                    print(response.json())
                except Exception as e:
                    print(e)
                    pass

                # Generate audio from Elevenlabs from the response
                now = str(datetime.now())
                print(now + " Generating response")
                audio = generate(
                    text=gpt_response,
                    voice="Grace",
                    model="eleven_turbo_v2",
                    stream=True,
                )
                try:
                    now = str(datetime.now())
                    print(now + "Streaming response")
                    stream(audio)
                except Exception as e:
                    print(e)
                    pass
                # Restart the recorder after audio has been played
                recorder.start()