import { RequestHandler } from '@sveltejs/kit';
import amqp from "amqplib/callback_api";
import { Transcription } from '../../../../types';

// TODO: make this less hacky
let mqConnection: any = null;

function streamSSEFromRabbitMQ(controller: ReadableStreamDefaultController) {
  amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
      throw error0;
    }
    connection.createChannel(function(error1, channel) {
      if (error1) {
        throw error1;
      }
      const queue = 'transcribed'; // TODO: make this a configured value
      channel.assertQueue(queue, {
        durable: false
      });
      // need to encode transcription as a JSON string
      channel.consume(queue, function(msg: string) {
        const transcription: Transcription = JSON.parse(msg);
        controller.enqueue(transcription);
      }, {
        noAck: true
      });
    });
  });
}

function cleanUpRabbitMQ() {
  if (mqConnection) {
    mqConnection.close();
    mqConnection = null;
  }
}

export const GET: RequestHandler = async ({ url }) => {
  const stream = new ReadableStream({
    start: streamSSEFromRabbitMQ,
    cancel: cleanUpRabbitMQ
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream', 
      'Cache-Control': 'no-cache', 
    }
  })
}
