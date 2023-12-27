import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../lib/server/mongo"; // TODO: figure out why $lib/ isn't working
import { ObjectId } from "mongodb";

export const PUT: RequestHandler = async ({ request }) => {
  const { key, value, isObjectId = false } = await request.json();

  const db = await mongo;
  db.collection("app_state").updateOne({ key }, { $set: {
    value: isObjectId ? ObjectId.createFromHexString(value) : value
  } }, { upsert: true });

  return json({ key, value });
}

export const GET: RequestHandler = async () => {
  const db = await mongo;
  const appState = await db.collection("app_state").find({}).toArray();
  return json(appState);
}
