import { ObjectId } from 'mongodb';
import { writable } from 'svelte/store';
import { Stream } from "../types";

// make this a readable and expose methods to make API calls which will update it

export const streams = writable<Stream[]>([]);

export const loadStreams = async () => {
  const response = await fetch('/api/streams');
  const data = await response.json();
  streams.set(data);
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
