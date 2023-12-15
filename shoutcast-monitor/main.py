import sys
from datetime import datetime
from TranscriptionService import TranscriptionService
import os
import logging
import signal
from dotenv import load_dotenv
import configparser
from TranscriptionStorageService import TranscriptionStorageService
from ShoutcastMonitor import ShoutcastMonitor
# from shared.MQService import MQService

config = configparser.ConfigParser()
config.read("config.ini")
load_dotenv()
logging.basicConfig(level=logging.ERROR)

monitor = ShoutcastMonitor("recordings/")

ts = TranscriptionService(os.getenv("OPENAI_API_KEY"))
tss = TranscriptionStorageService()
# mqs = MQService(host="rabbitmq", exchange=config["mqservice"]["exchange"])
# mqs.connect()

# Delete files upon exit
def signal_handler(sig, frame):
  print("\rCleaning up...")
  monitor.stop()
  for filename in os.listdir("recordings"):
    os.remove("recordings/" + filename)
  print("Done!")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Define a new function to handle transcription
def handle_transcription(path, channel_number):
  messages = ts.transcribe(path)
  entries = map(lambda message: {
    'timestamp': datetime.now(),
    'transcription': message
  }, messages)
  # tss.add_entries(entries)
  # for message in entries: # send to RabbitMQ for SSE server
  #   mqs.publish_event(message)
  for entry in entries:
    timestamped_transcription = entry["timestamp"].strftime("%H:%M:%S: ") + entry["transcription"]
    print("\rCH " + str(channel_number) + " @ " + timestamped_transcription)
  os.remove(path)

def handle_new_recording(path, channel_number):
  print("\rNew recording on CH " + str(channel_number) + "\t" + path)
  handle_transcription(path, channel_number)

def main():
  url = sys.argv[1:]
  monitor.start(url, handle_new_recording)

if __name__ == "__main__":
  main()
