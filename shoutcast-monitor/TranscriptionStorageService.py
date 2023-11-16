from pymongo import MongoClient

class TranscriptionStorageService:
  def __init__(self):
    self.__client = MongoClient('mongo', 27017)
    self.__db = self.__client['transcription_db']
    self.__collection = self.__db['transcribed_audio']
  
  def add_entry(self, entry):
    self.__collection.insert_one(entry)
