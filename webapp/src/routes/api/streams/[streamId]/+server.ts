import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../../lib/server/mongo"; // TODO: figure out why $lib/ isn't working
import { ObjectId } from "mongodb";

export const DELETE: RequestHandler = async (event) => {
  const { streamId: streamIdString } = event.params;

  if (!streamIdString) {
    throw new Error("No streamId provided");
  }

  const streamId = ObjectId.createFromHexString(streamIdString);
  console.log("received stream id", streamIdString, streamId);

  const db = await mongo;
  db.collection("streams").deleteOne({ _id: streamId });

  return json({ message: `[simulation] deleted ${streamId}` });
}
