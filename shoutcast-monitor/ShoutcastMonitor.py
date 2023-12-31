import requests
from io import BytesIO
from threading import Thread, Event
import sys
import logging
from datetime import datetime
from pydub import AudioSegment

class ShoutcastMonitor:

  def __init__(self, recording_directory):
    self.recording_directory = recording_directory
    self.stop_event = Event()
    self.start_threshold = -40 # dBFS
    self.stop_threshold = -40 # dBFS
    self.new_recording_callback = None
    self.record_buffer = {
      1: BytesIO(),
      2: BytesIO()
    }
    self.is_monitoring = False

  def start_recording_channel(self, channel_data, channel_number):
    not_recording = self.record_buffer[channel_number].tell() == 0
    
    if not_recording:
      print("Recording...", end="")
      sys.stdout.flush()

    # convert channel_data to bytes-like object
    bytes = BytesIO()
    channel_data = channel_data.export(bytes, format='mp3')
    bytes.seek(0)
    self.record_buffer[channel_number].write(bytes.read())
  
  def stop_recording_channel(self, channel_number):
    recording = self.record_buffer[channel_number].tell() > 0

    if recording:
      print("Saving recording...")
      filename = datetime.now().strftime("%H-%M-%S_" + str(channel_number) + ".mp3")
      path = self.recording_directory + filename

      # Stop recording
      self.record_buffer[channel_number].seek(0)
      record = AudioSegment.from_file(self.record_buffer[channel_number], format='mp3')

      record.export(path, format='mp3')

      # Clear buffer
      self.record_buffer[channel_number] = BytesIO()

      # Call callback
      if self.new_recording_callback:
        self.new_recording_callback(path, channel_number)


  def monitor_stream(self, url):
    response = requests.get(url, stream=True)
    buffer = BytesIO()

    # Continuously read data from the stream
    for block in response.iter_content(1024): # TODO: add timeout
      # stop monitoring if stop() is called
      if self.stop_event.is_set():
        # clean up
        self.new_recording_callback = None
        self.record_buffer = {
          1: BytesIO(),
          2: BytesIO()
        }
        self.stop_event.clear()
        self.is_monitoring = False
        break

      buffer.write(block)
      
      # Check audio level every few seconds
      # TODO: check if stereo or mono to get number of bytes per second
      if buffer.tell() > 3500 * 4:
        logging.debug("Checking audio level...")
        buffer.seek(0)

        segment = AudioSegment.from_file(buffer, format='mp3')
        stereo_components = segment.split_to_mono()

        for i, component in enumerate(stereo_components):
          if (component.dBFS > self.start_threshold):
            self.start_recording_channel(component, i + 1)
          elif (component.dBFS < self.stop_threshold):
            self.stop_recording_channel(i + 1)
        
        # Clear buffer
        buffer = BytesIO()
            

  def start(self, url, new_recording_callback):
    if self.is_monitoring:
      return
    print("Starting monitoring: " + url + "...")
    self.is_monitoring = True
    self.new_recording_callback = new_recording_callback
    Thread(target=self.monitor_stream, args=(url,)).start()

  def stop(self):
    if not self.is_monitoring:
      return
    self.stop_event.set()
    while self.is_monitoring:
      pass
    print("Stopped monitoring")
