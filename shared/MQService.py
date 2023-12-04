import pika

class MQService:

  def __init__(self, host="localhost", port=5672, exchange="events"):
    """
    Initialize the RabbitMQ client.

    Args:
      host (str): RabbitMQ host. Defaults to "localhost".
      port (int): RabbitMQ port. Defaults to 5672.
      exchange (str): Name of the exchange to publish/subscribe to events. Defaults to "events".
    """
    self.host = host
    self.port = port
    self.exchange = exchange
    self._connection = None
    self._channel = None
    self._callbacks = {}

  def connect(self):
    """
    Establish a connection to the RabbitMQ server.
    """
    self._connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.host, port=self.port)
    )
    self._channel = self._connection.channel()
    self._channel.exchange_declare(exchange=self.exchange, exchange_type="fanout")

  def publish_event(self, payload):
    """
    Publish an event to the RabbitMQ exchange.

    Args:
      payload (dict): Event payload to publish.
    """
    if not self._connection or not self._connection.is_open:
      raise ConnectionError("Not connected to RabbitMQ")
    self._channel.basic_publish(
      exchange=self.exchange, routing_key="", body=json.dumps(payload).encode()
    )

  def subscribe_event(self, routing_key, callback):
    """
    Subscribe to events with a specific routing key.

    Args:
      routing_key (str): Routing key to subscribe to.
      callback (callable): Function to be called when an event is received.
    """
    self._callbacks[routing_key] = callback
    queue = self._channel.queue_declare().method.queue
    self._channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=routing_key)
    self._channel.basic_consume(queue=queue, on_message_callback=self._on_message)

  def _on_message(self, channel, method, properties, body):
    """
    Internal callback for handling received messages.

    Args:
      channel (pika.channel.Channel): Channel the message was received on.
      method (pika.spec.basic.Deliver): Message delivery method.
      properties (pika.spec.basic_properties.BasicProperties): Message properties.
      body (bytes): Message body.
    """
    try:
      payload = json.loads(body.decode())
      routing_key = method.routing_key
      if routing_key in self._callbacks:
        self._callbacks[routing_key](payload)
    except Exception as e:
      print(f"Error processing message: {e}")

  def close(self):
    """
    Close the connection to the RabbitMQ server.
    """
    if self._connection:
      self._connection.close()

