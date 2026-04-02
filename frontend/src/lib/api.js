import { PUBLIC_API_URL } from '$env/static/public';

const apiBase = (PUBLIC_API_URL || 'http://localhost:8000').replace(/\/+$/, '');
// Django routes are defined with a trailing slash: /api/notes/
const notesBase = `${apiBase}/api/notes/`;

async function ensureJson(res) {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function fetchNotes() {
  const res = await fetch(notesBase, { method: 'GET' });
  if (!res.ok) throw new Error(`Failed to load notes (${res.status})`);
  return await res.json();
}

function noteDetailUrl(id) {
  // notesBase already ends with `/`, so avoid double slashes.
  return `${notesBase}${id}/`;
}

export async function createNote({ title, body }) {
  const res = await fetch(notesBase, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ title, body })
  });
  if (!res.ok) throw new Error(`Failed to create note (${res.status})`);
  return await res.json();
}

export async function updateNote({ id, title, body }) {
  const res = await fetch(noteDetailUrl(id), {
    method: 'PUT',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ title, body })
  });
  if (!res.ok) throw new Error(`Failed to update note (${res.status})`);
  return await res.json();
}

export async function deleteNote(id) {
  const res = await fetch(noteDetailUrl(id), { method: 'DELETE' });
  if (res.status !== 204) {
    const detail = await ensureJson(res);
    throw new Error(`Failed to delete note (${res.status}): ${JSON.stringify(detail)}`);
  }
}

