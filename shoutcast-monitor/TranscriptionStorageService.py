from pymongo import MongoClient

class TranscriptionStorageService:
  def __init__(self, host='localhost'):
    self.__client = MongoClient(host, 27017)
    self.__db = self.__client['transcription_db']
    self.__collection = self.__db['transcribed_audio']
  
  def add_entry(self, entry):
    self.__collection.insert_one(entry)

  def add_entries(self, entries):
    self.__collection.insert_many(entries)

  # TODO: make this class more generic, not transcription-oriented
  def get_stream_info(self, stream_id):
    return self.__db['streams'].find_one({'_id': stream_id})
  
  def set_active_stream(self, stream_id):
    self.__db['app_state'].update_one({'key': 'activeStreamId'}, {'$set': {'value': stream_id}})

  def get_active_stream_id(self):
    maybe_doc = self.__db['app_state'].find_one({'key': 'activeStreamId'})
    if not maybe_doc:
      return None
    return maybe_doc['value']
