from pydub import AudioSegment
from pydub.playback import play as mp3Play


def play_mp3(filename):
    audio = AudioSegment.from_mp3(filename)
    mp3Play(audio)
