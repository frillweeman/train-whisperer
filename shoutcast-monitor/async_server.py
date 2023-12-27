from aiohttp import web
from main import start_monitoring_active_stream, stop_monitoring, start_monitoring_with_stream_id, start_sse, stop_sse, outbound_sse_queue
import json
from threading import Event
from queue import Empty
import asyncio

stop_event = Event()

async def handle_start(request):
  data = await request.json()
  stream_id = data.get('streamId')
  start_monitoring_with_stream_id(stream_id)
  return web.Response(text='Start request received')

async def handle_stop(request):
  stop_event.set()
  stop_monitoring()
  return web.Response(text='Stop request received')

async def handle_sse(request):
  stop_event.clear()
  start_sse()
  print("new SSE connection...")
  response = web.StreamResponse()
  response.headers['Content-Type'] = 'text/event-stream'
  response.headers['Cache-Control'] = 'no-cache'
  response.headers['Connection'] = 'keep-alive'
  response.headers['Access-Control-Allow-Origin'] = '*'
  await response.prepare(request)

  try:
    while not stop_event.is_set():
      try: # TODO: quickly loop over queue when it receives stuff, not 0.5s delay
        outbound_msg = outbound_sse_queue.get_nowait()
        message = f"data: {json.dumps(outbound_msg)}\n\n"
        await response.write(message.encode())
      except Empty:
        await asyncio.sleep(0.5)
        continue
    
    # cleanup SSE
    print("Stopping SSE due to stop event")
    stop_sse()
  except ConnectionResetError:
    print("Client disconnected")
    stop_sse()
  finally:
    try:
      await response.write_eof()
    except ConnectionResetError:
      print("Client disconnected before the response could be sent.")
      stop_sse()

  return response

if __name__ == '__main__':
  print("Starting server...")
  start_monitoring_active_stream()

  print("started monitoring active stream")
  
  app = web.Application()

  app.router.add_post('/start', handle_start)
  app.router.add_post('/stop', handle_stop)
  app.router.add_get('/transcriptions/live', handle_sse)

  web.run_app(app, port=8000, handle_signals=False, keepalive_timeout=0)
