import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../lib/server/mongo";
import { Transcription } from "../../../types";
import { ObjectId } from "mongodb";

export const GET: RequestHandler = async (event) => {
  const db = await mongo;
  const activeStreamId: ObjectId = (await db.collection("app_state").findOne({ key: "activeStreamId" }))?.value;
  const transcriptions = (await db.collection("transcribed_audio").find({ streamId: activeStreamId }).toArray())
    .map(transcription => transcription as Transcription);

  return json(transcriptions);
}
