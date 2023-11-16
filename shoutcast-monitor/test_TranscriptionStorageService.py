from TranscriptionStorageService import TranscriptionStorageService
from datetime import datetime

def test_add_entry():
  tss = TranscriptionStorageService()
  entry = {
    'timestamp': datetime.now(),
    'transcription': 'This is a test transcription'
  }
  tss.add_entry(entry)

if __name__ == "__main__":
  test_add_entry()
  print("Test passed!")
