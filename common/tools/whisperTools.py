import webrtcvad
import numpy as np
import time
import wave
import struct
import os
import logging

from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)


def voice_detected(
    audio_data, sample_rate=16000, aggressiveness=3, volume_threshold=600
):
    """
    Detects voice in the given audio data using WebRTC VAD and volume thresholding.

    Parameters:
    - audio_data: The audio data in PCM format.
    - sample_rate: The sample rate of the audio data. Default is 16kHz.
    - aggressiveness: VAD aggressiveness mode, which is an integer between 0 and 3.
                      0 is the least aggressive about filtering out non-speech,
                      3 is the most aggressive.
    - volume_threshold: The RMS energy threshold below which audio is considered silent.

    Returns:
    - True if voice is detected, False otherwise.
    """
    vad = webrtcvad.Vad(aggressiveness)
    frame_length = int(sample_rate * 0.01)
    audio_frame = audio_data[:frame_length]
    audio = np.int16(audio_frame).tobytes()

    rms = np.sqrt(np.mean(np.square(audio_frame)))

    if vad.is_speech(audio, sample_rate) and rms > volume_threshold:
        logger.info("Voice Speech detected")
        return True
    else:
        return False


def is_silence(audio_data, threshold=200, window_duration=0.5, sample_rate=16000):
    """
    Detect if the audio data represents silence based on volume standard deviation over a window.

    Parameters:
    - audio_data: Audio data to check for silence.
    - threshold: Standard deviation threshold below which audio is considered silent.
    - window_duration: Duration of the window in seconds over which to calculate the standard deviation.
    - sample_rate: Sample rate of the audio data.

    Returns:
    - True if the audio is considered silent, False otherwise.
    """
    audio_np = np.array(audio_data)
    window_size = int(window_duration * sample_rate)
    std_dev = np.std(audio_np[-window_size:])
    return std_dev < threshold


def is_silence(pcm_chunk, threshold=1000):
    """Check if the given PCM chunk is silent. You might need to adjust the threshold based on your microphone sensitivity."""
    avg_amplitude = sum([abs(sample) for sample in pcm_chunk]) / len(pcm_chunk)
    return avg_amplitude < threshold


def record_until_silence(recorder, max_duration_seconds=10, silence_duration=1):
    """Record audio until silence is detected, with terminal feedback."""
    audio_data = []
    silence_start_time = None
    end_time = time.time() + max_duration_seconds
    logger.info("Listening...")

    while time.time() < end_time:
        pcm = (
            recorder.read()
        )  # This should return a chunk of audio data as a list of integers.
        audio_data.extend(pcm)

        # Only check the recent chunk for silence to improve efficiency
        if is_silence(pcm):
            if silence_start_time is None:
                silence_start_time = time.time()
                logger.info("\rSilence detected, waiting...")
            elif time.time() - silence_start_time > silence_duration:
                logger.info("\rSilence duration met. Recording stopped.")
                break
        else:
            if silence_start_time is not None:
                logger.info(
                    "\rListening..."
                )  # Reset the message when noise is detected
            silence_start_time = None

    if not silence_start_time:
        logger.info("\rMax duration reached. Recording stopped.")
    return audio_data


def transcribe_with_whisper(audio_data):
    """
    Transcribe the given audio data with Whisper ASR.
    Note: For frequent transcriptions, consider an in-memory solution to avoid file I/O.
    """
    with wave.open("temp_audio.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # Assuming 16-bit audio
        wf.setframerate(16000)  # Common sample rate for ASR
        wf.writeframes(struct.pack("h" * len(audio_data), *audio_data))

    with open("temp_audio.wav", "rb") as f:
        # Ideally, you'd handle exceptions here for potential API errors
        # response = {}  # Dummy response since I can't call external APIs. Replace with actual API call.
        # response = client.audio.transcribe("whisper-1", f)
        response = client.audio.transcriptions.create(model="whisper-1", file=f)
    logger.info(response)
    try:
        os.remove("temp_audio.wav")
    except Exception as e:
        logger.info(f"Error deleting file: {e}")
    return response
