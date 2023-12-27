import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../lib/server/mongo"; // TODO: figure out why $lib/ isn't working
import { InsertOneResult, ObjectId } from "mongodb";
import { Stream } from "$lib/types";

export const GET: RequestHandler = async (event) => {
  const db = await mongo;
  const streams = await db.collection("streams").find({}).toArray();
  return json(streams);
}

export const POST: RequestHandler = async (event) => {
  const { url } = await event.request.json();

  // get stream title from <title> tag in head
  const response = await fetch(url);
  const html = await response.text();
  const maybeTitle = html.match(/<title>(.*)<\/title>/)?.[1];
  const newStream: Stream = {
    _id: undefined,
    channelNames: [],
    url,
    title: maybeTitle || "Unnamed Stream",
  }
  const insertedDoc = await addStreamToDb(newStream);

  return json({
    ...newStream,
    _id: insertedDoc.insertedId
  });
}

async function addStreamToDb(stream: Stream): Promise<InsertOneResult<Document>> {
  const db = await mongo;
  return await db.collection("streams").insertOne(stream);
  
}
