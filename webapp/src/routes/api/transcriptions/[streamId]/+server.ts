import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../../lib/server/mongo";
import { Transcription } from "$lib/types";
import { ObjectId } from "mongodb";

export const GET: RequestHandler = async ({ params }) => {
  const db = await mongo;

  if (!params.streamId) {
    throw new Error("No streamId provided");
  }
  const streamId: ObjectId = ObjectId.createFromHexString(params.streamId);
  const transcriptions = (await db.collection("transcribed_audio").find({ streamId }).toArray())
    .map(transcription => transcription as Transcription);

  return json(transcriptions);
}

export const DELETE: RequestHandler = async ({ params }) => {
  const db = await mongo;

  if (!params.streamId) {
    throw new Error("No streamId provided");
  }
  const streamId: ObjectId = ObjectId.createFromHexString(params.streamId);
  await db.collection("transcribed_audio").deleteMany({ streamId });

  return json({ message: "ok" });
}
