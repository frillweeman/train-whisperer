import { RequestHandler, json } from "@sveltejs/kit";
import { mongo } from "../../../lib/server/mongo"; // TODO: figure out why $lib/ isn't working
import { InsertOneResult, ObjectId } from "mongodb";
import { Stream } from "../../../types";

const tmpData = {
  applicationState: [
    {
      key: 'activeStreamId',
      value: 1
    }
  ],
  streams: [
    {
      _id: 1,
      channelNames: [], // default
      url: 'https://broadcastify.cdnstream1.com/8083',
      title: 'BNSF/UP Seattle Sub - North End',
    },
    {
      _id: 2,
      channelNames: ["NS", "CSX"], // custom
      url: 'https://broadcastify.cdnstream1.com/6752',
      title: 'Decatur Area CSX and Norfolk Southern Rail',
    }
  ],
}

export const GET: RequestHandler = async (event) => {
  const db = await mongo;
  const streams = await db.collection("streams").find({}).toArray();
  return json(streams);
}

export const POST: RequestHandler = async (event) => {
  const { url } = await event.request.json();
  console.log('POST /api/streams/+server.ts:', url)

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
