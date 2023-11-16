import requests
from pydub import AudioSegment
from io import BytesIO
from datetime import datetime
from TranscriptionService import TranscriptionService
import os
import threading
import logging
import signal
import sys
from dotenv import load_dotenv
import configparser
from TranscriptionStorageService import TranscriptionStorageService

config = configparser.ConfigParser()
config.read("config.ini")
load_dotenv()
logging.basicConfig(level=logging.ERROR)

ts = TranscriptionService(os.getenv("OPENAI_API_KEY"))
tss = TranscriptionStorageService()

# Delete files upon exit
def signal_handler(sig, frame):
  print("\rCleaning up...")
  for filename in os.listdir("recordings"):
    os.remove("recordings/" + filename)
  print("Done!")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Define a new function to handle transcription
def handle_transcription(filename):
  text = ts.transcribe(filename)
  tss.add_entry({
    'timestamp': datetime.now(),
    'transcription': text
  })
  timestamped_transcription = datetime.now().strftime("%H:%M:%S: ") + text
  print("\rNew DB entry\t" + timestamped_transcription)
  os.remove("recordings/" + filename)

def check_audio_level(segment):
  return segment.dBFS

def main():
  stream_url = config["shoutcast"]["stream_url"]
  response = requests.get(stream_url, stream=True)

  logging.debug("Connected to stream...")

  buffer = BytesIO()
  record_buffer = BytesIO()
  recording = False

  start_threshold = -40 # dBFS
  stop_threshold = -40 # dBFS

  # Continuously read data from the stream
  for block in response.iter_content(1024):
    buffer.write(block)
    
    # Check audio level every few seconds
    if buffer.tell() > 3500 * 4: # 28 kbps = 3500 B/s
      logging.debug("Checking audio level...")
      buffer.seek(0)

      # current_fname = datetime.now().strftime("%H-%M-%S") + '.mp3'
      
      segment = AudioSegment.from_file(buffer, format='mp3')
      # segment.export(current_fname, format='mp3')
      
      level = check_audio_level(segment)
      # print("Current level: " + str(level))
      if level > start_threshold:
        if not recording:
          print("Recording...", end="")
          sys.stdout.flush()
          # Start recording
          recording = True
          record_buffer = BytesIO()
        
        record_buffer.write(buffer.getbuffer())
      elif level < stop_threshold and recording:
        logging.debug("Saving recording...")
        filename = datetime.now().strftime("%H-%M-%S.mp3")

        # Stop recording
        recording = False
        record_buffer.seek(0)
        record = AudioSegment.from_file(record_buffer, format='mp3')

        record.export("recordings/" + filename, format='mp3')
        threading.Thread(target=handle_transcription, args=(filename,)).start()
      
      # Clear buffer
      buffer = BytesIO()

if __name__ == "__main__":
  main()
