import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../../lib/server/mongo"; // TODO: figure out why $lib/ isn't working
import { ObjectId } from "mongodb";

export const DELETE: RequestHandler = async (event) => {
  const { streamId: streamIdString } = event.params;

  if (!streamIdString) {
    throw new Error("No streamId provided");
  }

  const streamId = ObjectId.createFromHexString(streamIdString);

  const db = await mongo;
  await db.collection("streams").deleteOne({ _id: streamId });
  await db.collection("transcribed_audio").deleteMany({ streamId });

  return json({ message: `deleted ${streamId}` });
}

export const PATCH: RequestHandler = async (event) => {
  const { streamId: streamIdString } = event.params;

  if (!streamIdString) {
    throw new Error("No streamId provided");
  }

  const changes = await event.request.json()
  const streamId = ObjectId.createFromHexString(streamIdString);

  const db = await mongo;
  await db.collection("streams").findOneAndUpdate(
    { _id: streamId },
    { $set: changes },
  );

  return json({
    message: `updated ${streamId}`,
    changes,
  });
}
