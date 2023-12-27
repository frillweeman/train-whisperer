import { RequestHandler, json } from '@sveltejs/kit';
import { mongo } from '../../../../lib/server/mongo';

export const GET: RequestHandler = async ({ params }) => {
  const { key } = params;
  const db = await mongo;
  const requestedKV = await db.collection("app_state").find({ key }).toArray();
  return json(requestedKV[0] ?? { key, value: null });
}
