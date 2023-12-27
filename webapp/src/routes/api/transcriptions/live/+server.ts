import { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async (req) => {
  try {
    const hostAndPort = process.env.DOCKER_ENV ? 'shoutcast_monitor:8000' : '127.0.0.1:8000';
    const res = await fetch(`http://${hostAndPort}/transcriptions/live`);
    const stream = res.body;

    // Directly use the fetched stream as the response stream
    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
      },
      status: res.status,
      statusText: res.statusText,
    });
  } catch (err) {
    console.error('Error fetching SSE from backend:', err);
    return new Response('Error fetching SSE', { status: 500 });
  }
};
