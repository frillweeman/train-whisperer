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
from bson.objectid import ObjectId
from queue import Queue, Empty

rabbitmq_host = "rabbitmq" if os.getenv('DOCKER_ENV') else "localhost"
mongo_host = "mongo" if os.getenv('DOCKER_ENV') else "localhost"

monitoring_sse = False
outbound_sse_queue = Queue()

config = configparser.ConfigParser()
config.read("config.ini")
load_dotenv()
logging.basicConfig(level=logging.ERROR)

monitor = ShoutcastMonitor("recordings/")

ts = TranscriptionService(os.getenv("OPENAI_API_KEY"))
tss = TranscriptionStorageService(host=mongo_host)

current_stream_id = None

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
  if not current_stream_id:
    raise Exception("Stream ID not set")
  
  messages = ts.transcribe(path)
  db_entries = []

  for message in messages:
    now = datetime.utcnow()
    entry = {
      'streamId': current_stream_id,
      'channelIndex': channel_number,
      'text': message,
      'timestamp': now.isoformat()
    }
    db_entry = entry.copy()
    db_entry.update({
      'streamId': ObjectId(entry['streamId']),
      'timestamp': now
    })
    db_entries.append(db_entry)
    if monitoring_sse:
      outbound_sse_queue.put(entry)
    print("\r" + entry['timestamp'] + " CH " + str(channel_number) + "\t" + message)

  if len(db_entries) > 0:
    tss.add_entries(db_entries)

  os.remove(path)

def handle_new_recording(path, channel_number):
  print("\rNew recording on CH " + str(channel_number) + "\t" + path)
  handle_transcription(path, channel_number)

def start_monitoring_with_stream_id(stream_id_string):
  stream_id = ObjectId(stream_id_string)
  stream = tss.get_stream_info(stream_id)

  if not stream:
    raise Exception("Stream not found")
  
  tss.set_active_stream(stream_id)

  global current_stream_id
  current_stream_id = stream_id_string

  # wipe the queue, maintain reference to the queue object
  while not outbound_sse_queue.empty():
    try:
      outbound_sse_queue.get_nowait()
    except Empty:
      break

  if monitor.is_monitoring:
    monitor.stop()
  monitor.start(stream["url"], handle_new_recording)

def start_monitoring_active_stream():
  stream_id = tss.get_active_stream_id()

  if stream_id:
    stream_id_string = str(stream_id)
    print("Found active stream: " + stream_id_string)
    start_monitoring_with_stream_id(stream_id_string)
  else:
    print("No active stream found, waiting for activation...")

def stop_monitoring():
  global monitoring_sse
  monitoring_sse = False
  global current_stream_id
  current_stream_id = None
  tss.set_active_stream(None)
  monitor.stop()

def start_sse():
  global monitoring_sse
  monitoring_sse = True

def stop_sse():
  global monitoring_sse
  monitoring_sse = False
