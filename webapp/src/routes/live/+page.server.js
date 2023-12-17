import { redirect } from '@sveltejs/kit';

export function load() {
  const activeStream = null; // TODO: grab from DB
  if (activeStream)
    throw redirect(307, `/live/${activeStream}`);
}
