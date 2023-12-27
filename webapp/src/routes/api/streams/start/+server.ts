import { RequestHandler } from "@sveltejs/kit";

const hostAndPort = process.env.DOCKER_ENV ? 'shoutcast_monitor:8000' : '127.0.0.1:8000';

export const POST: RequestHandler = async (event) => {
  const { streamId } = await event.request.json();
  const response = await fetch(`http://${hostAndPort}/start`, {
    method: 'POST',
    body: JSON.stringify({ streamId }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  return response;
}
