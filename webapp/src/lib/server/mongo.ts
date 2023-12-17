import { MongoClient } from "mongodb";

const MONGO_URL = "mongodb://localhost:27017";
const MONGO_DB_NAME = "transcription_db";

const client = new MongoClient(MONGO_URL);

let counter = 0;

export const mongo = client.connect().then((client) => {
  console.log(`Connected to MongoDB: ${++counter}`);
  return client.db(MONGO_DB_NAME)
});
