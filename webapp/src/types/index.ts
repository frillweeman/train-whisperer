import { ObjectId } from "mongodb";

export interface Stream {
  _id: ObjectId | undefined;
  channelNames: string[];
  url: string;
  title: string;
}

export interface Transcription {
  _id: ObjectId | undefined;
  streamId: ObjectId;
  channelIndex: number;
  text: string;
  timestamp: Date;
}
