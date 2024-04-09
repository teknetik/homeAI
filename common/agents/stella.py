import os
import time
import requests
import logging

from common.tools import whisperTools
from common.tools import mp3Player

from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.tools import tool
from langchain.agents import Tool
from langchain.agents import initialize_agent

from datetime import datetime
from elevenlabs import stream

logger = logging.getLogger(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
logger.info("OpenAI API Key: " + openai_api_key)


def agent(recorder, memory):
    role = """
    You are an AI assistant called stella.
    Your role is to provide short conversational answers to questions or tasks given by the user.
    Provide responses that dont provide a large amount of detail and could be spoken out loud in a few seconds.
    """
    model = "gpt-4-turbo"
    recorder.stop()
    mp3Player.play_mp3("./common/agents/mp3/how_can_i_help.mp3")
    recorder.start()
    time.sleep(0.1)

    in_conversation = True
    while in_conversation:
        talking = whisperTools.voice_detected(recorder.read())
        if talking:
            audio_data = whisperTools.record_until_silence(recorder)
            logger.info("Sending recorded audio to Elevenlabs")
            transcription = whisperTools.transcribe_with_whisper(audio_data)
            logger.info(transcription.text.lower())
            if "thank you for watching" in transcription.text.lower() or "stop" in transcription.text.lower() or "terminate" in transcription.text.lower() or "pause" in transcription.text.lower():
                in_conversation = False
                logger.info("Ending Conversation")
                mp3Player.play_mp3("./common/agents/mp3/end_convo.mp3")
            else:
                recorder.stop()

                # Send the user message to the LLM
                llm = ChatOpenAI(temperature=0.5, model=model)
                message = [
                    SystemMessage(
                        content="""
                        You are an AI assistant called stella.
                        Your role is to provide short conversational answers to questions or tasks given by the user.
                        Provide responses that dont provide a large amount of detail and could be spoken out loud in a few seconds.
                        """
                    ),
                    HumanMessage(
                        content=transcription.text
                    )
                ]
                gpt_response = llm.invoke(message)
                now = str(datetime.now())
                logger.info(now + " Full response:")
                logger.info(gpt_response.content)
                print(type(gpt_response.content))

                # Generate audio from Elevenlabs from the response
                now = str(datetime.now())
                logger.info(now + " Generating response")
                from elevenlabs import play
                from elevenlabs.client import ElevenLabs

                client = ElevenLabs(
                    api_key=elevenlabs_api_key
                )

                audio = client.generate(
                    text=gpt_response.content,
                    voice="Rachel",
                    model="eleven_turbo_v2",
                    stream=True
                )
                try:
                    now = str(datetime.now())
                    logger.info(now + "Streaming response")
                    stream(audio)
                except Exception as e:
                    logger.info(e)
                    pass
                # Restart the recorder after audio has been played
                recorder.start()
        else:
            # If no speech was detected
            logger.info("No speech detected, skipping this cycle.")