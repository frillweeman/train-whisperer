from MQService import MQService

mq = MQService(queue="test")

mq.connect()
mq.publish_event({
  "nigger": "yeah, why not"
})
mq.close()
