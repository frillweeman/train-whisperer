import { RequestHandler } from '@sveltejs/kit';

// TODO: rabbitmq consumer needs to provide data to the SSE stream

export const GET: RequestHandler = async ({ url }) => {
  const stream = new ReadableStream({
    start(controller) {
      // You can enqueue multiple data asynchronously here.
      const myData = ["abc", "def"]
      myData.forEach(data => {
          controller.enqueue(`data: ${data}\n\n`)
      })
      controller.close() 
    },
    cancel() {
      // cancel your resources here
    }
  });

  return new Response(stream, {
    headers: {
      // Denotes the response as SSE
      'Content-Type': 'text/event-stream', 
      // Optional. Request the GET request not to be cached.
      'Cache-Control': 'no-cache', 
    }
  })
}
