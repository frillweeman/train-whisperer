from MQService import MQService

mq = MQService(queue="test")

mq.connect()
mq.publish_event({
  "biggest": "yeah, why not"
})
mq.close()
