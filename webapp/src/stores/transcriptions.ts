import { writable } from 'svelte/store';
import { Transcription } from '../types';

// on connection, it starts the RabbitMQ consumer
// on message, it adds the new transcription to the store
// on last unsubscribe, it closes the connection
export const transcriptions = writable<Transcription[]>([], (_, update) => {
  const eventSource = new EventSource('/api/transcriptions');

  eventSource.onmessage = (event) => {
    const newTranscription: Transcription = JSON.parse(event.data);
    update((transcriptions) => [...transcriptions, newTranscription]);
  }

  // on last unsubscribe, close the event source
  return eventSource.close;
});
