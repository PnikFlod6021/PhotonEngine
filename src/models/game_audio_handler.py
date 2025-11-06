from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import random

from src.constants import GameAudioConstants

class GameAudioHandler():
    def __init__(self):
        self.audio_paths = [
            GameAudioConstants.AUDIO_1,
            GameAudioConstants.AUDIO_2,
            GameAudioConstants.AUDIO_3,
            GameAudioConstants.AUDIO_4,
            GameAudioConstants.AUDIO_5,
            GameAudioConstants.AUDIO_6,
            GameAudioConstants.AUDIO_7,
            GameAudioConstants.AUDIO_8
        ]

        self.random_audio_path = random.choice(self.audio_paths)

    def cut_audio(self,b_seconds=0, b_minutes=0,e_seconds=0, e_minutes=0): #begin and end times to splice
        beginning_minutes = b_minutes * (60 * 1000)
        beginning_seconds = b_seconds * 1000
        end_minutes = e_minutes * (60 * 1000)
        end_seconds = e_seconds * 1000

        beginning_time_to_trim = beginning_minutes + beginning_seconds
        end_time_to_trim = end_minutes + end_seconds

        audio = AudioSegment.from_mp3(self.random_audio_path) 

        trimmed_audio = audio[beginning_time_to_trim:end_time_to_trim]

        return trimmed_audio

    def play_random_audio(self):
        trimmed_audio = (self.cut_audio(
                        b_seconds=(GameAudioConstants.COUNTDOWN_GAME_AUDIO_LENGTH), 
                        e_minutes=GameAudioConstants.GAME_AUDIO_LENGTH,
                        e_seconds=GameAudioConstants.COUNTDOWN_GAME_AUDIO_LENGTH))

        _play_with_simpleaudio(trimmed_audio)
    
    def play_countdown_audio(self):
        trimmed_audio = (self.cut_audio(
                        e_seconds=GameAudioConstants.COUNTDOWN_GAME_AUDIO_LENGTH))

        _play_with_simpleaudio(trimmed_audio)

        
