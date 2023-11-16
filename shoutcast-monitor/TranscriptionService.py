from openai import OpenAI
from os import path
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class TranscriptionService:

  def __init__(self, openai_api_key):
    self.__client = OpenAI(api_key=openai_api_key)

  # strip the first 3 characters from the transcript
  def __postprocess(self, text):
    return text[3:]


  def transcribe(self, filename):
    afpath = path.join(path.dirname(path.realpath(__file__)), "recordings", filename)
    audio_file= open(afpath, "rb")
    transcript = self.__client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file,
      language="en",
      prompt=config["transcription_service"]["prompt"],
    )
    return self.__postprocess(transcript.text)
