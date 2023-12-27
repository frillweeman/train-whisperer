import type { ObjectId } from 'mongodb';
import { Writable, writable, derived } from 'svelte/store';
import { BrowserStream } from "$lib/types";

export const streams = writable<BrowserStream[]>([]);
export const activeStreamId = writable<string | undefined>(undefined);
export const activeStream = derived<[Writable<BrowserStream[]>, Writable<string | undefined>], BrowserStream>([streams, activeStreamId], ([$streams, $activeStreamId], set) => {
  set($streams.find(stream => stream._id == $activeStreamId));
});

export const loadStreams: () => Promise<void> = () => {
  return Promise.all([
    fetch('/api/streams'),
    fetch('/api/appState/activeStreamId')
  ]).then(async ([streamsResponse, activeStreamIdResponse]) => {
    const streamsJson = await streamsResponse.json();
    const { value: activeStreamIdValue } = await activeStreamIdResponse.json();

    streams.set(streamsJson);
    activeStreamId.set(activeStreamIdValue);
  });
}

export const deleteStream = async (streamId: ObjectId) => {
  await fetch(`/api/streams/${streamId.toString("hex")}`, { method: 'DELETE' });
  loadStreams();
}

export const addStream = async (url: string) => {
  await fetch(`/api/streams`, {
    method: 'POST',
    body: JSON.stringify({ url }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  loadStreams();
}

export const setActiveStream = async (streamId: string) => {
  console.log("setting active stream");
  await fetch(`/api/appState`, {
    method: 'PUT',
    body: JSON.stringify({ key: 'activeStreamId', value: streamId, isObjectId: true }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  await startMonitoring(streamId);
  loadStreams();
}

export const deactivateStream = async () => {
  console.log("deactivating stream");
  await fetch(`/api/appState`, {
    method: 'PUT',
    body: JSON.stringify({ key: 'activeStreamId', value: undefined }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  await stopMonitoring();
  loadStreams();
}

async function stopMonitoring(): Promise<Response> {
  return await fetch('/api/streams/stop', {
    method: 'POST',
    body: JSON.stringify({}),
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

async function startMonitoring(streamId: string): Promise<Response> {
  return await fetch('/api/streams/start', {
    method: 'POST',
    body: JSON.stringify({ streamId }),
    headers: {
      'Content-Type': 'application/json'
    }
  });
}
