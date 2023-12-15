import sys, os
from MQService import MQService

def on_message(payload):
  print("received message:\n{}".format(payload))

def main():
  mq = MQService(queue="transcribed")
  mq.connect()

  print("listening for messages...")

  mq.subscribe_event("transcribed", on_message)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
