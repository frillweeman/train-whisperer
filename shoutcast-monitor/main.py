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
from MQService import MQService

rabbitmq_host = "rabbitmq" if os.getenv('DOCKER_ENV') else "localhost"

config = configparser.ConfigParser()
config.read("config.ini")
load_dotenv()
logging.basicConfig(level=logging.ERROR)

monitor = ShoutcastMonitor("recordings/")

ts = TranscriptionService(os.getenv("OPENAI_API_KEY"))
tss = TranscriptionStorageService()
mqs = MQService(host=rabbitmq_host, queue="transcribed")

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

  for message in messages:
    now = datetime.now()
    entry = {
      'timestamp': now.strftime("%Y-%m-%d %H:%M:%S"),
      'channel': channel_number,
      'transcription': message
    }
    mqs.publish_event(entry)
    print("\r" + entry['timestamp'] + " CH " + str(channel_number) + "\t" + message)

  # tss.add_entries(entries)
  # for message in entries: # send to RabbitMQ for SSE server
  #   mqs.publish_event(message)

  os.remove(path)

def handle_new_recording(path, channel_number):
  print("\rNew recording on CH " + str(channel_number) + "\t" + path)
  handle_transcription(path, channel_number)

def main():
  url = sys.argv[1:]
  mqs.connect()
  monitor.start(url, handle_new_recording)

if __name__ == "__main__":
  main()
