import os
import logging
import asyncio

from common.tools import whisperTools
from common.tools import mp3Player
from stream import chat_completion

from elevenlabs.client import AsyncElevenLabs as ElevenLabs
from elevenlabs import stream

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


logger = logging.getLogger(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
logger.info("OpenAI API Key: " + openai_api_key)
model = "gpt-4-turbo"

# Initialize clients
llm = ChatOpenAI(temperature=0.5, model=model)
client = ElevenLabs(
    api_key=elevenlabs_api_key
)



def agent(recorder, memory):

    recorder.stop()
    mp3Player.play_mp3("./common/agents/mp3/how_can_i_help.mp3")
    recorder.start()
    #time.sleep(0.1)

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
                recorder.stop()
            else:
                recorder.stop()

                # Create LLM prompt and send
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
                logger.info(f"Full response: %s", gpt_response.content)

                # Generate audio from Elevenlabs from the response
                logger.info("Generating response")
                # audio = client.generate(
                #     text=gpt_response.content,
                #     voice="Rachel",
                #     model="eleven_turbo_v2",
                #     stream=True
                # )
                asyncio.run(chat_completion(gpt_response.content))
                try:
                    logger.info("Streaming response")
                    #stream(audio)
                except Exception as e:
                    logger.info(e)
                    pass
                # Restart the recorder after audio has been played
                recorder.start()
        else:
            # If no speech was detected
            pass
            #logger.info("No speech detected, skipping this cycle.")