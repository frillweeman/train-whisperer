import { RequestHandler } from "@sveltejs/kit";

const hostAndPort = process.env.DOCKER_ENV ? 'shoutcast_monitor:8000' : '127.0.0.1:8000';

export const POST: RequestHandler = async (event) => {
  const response = await fetch(`http://${hostAndPort}/stop`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  return response;
}
