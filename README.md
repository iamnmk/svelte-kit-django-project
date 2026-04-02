# Chill Notes (SvelteKit + Django REST)

Small no-auth demo app for testing deployment. Create/edit/delete notes in the browser; data persists to a JSON file on the backend.

## End-to-end manual test

### 1. Start with Docker Compose (recommended)

1. From the project root:
   - `docker compose up --build`
2. Open:
   - `http://localhost:3000`
3. Create a note:
   - Enter a `Title` and `Body`
   - Click `Create`
   - Confirm the new note appears in the list

### 2. Verify the Django API directly

In another browser tab, open:
- `http://localhost:8000/api/notes/`

You should see the notes you created above.

### 3. Edit and delete

1. Click `Edit` on a note, change the text, click `Save`
2. Click `Delete` on a note and confirm it disappears
3. Confirm persistence:
   - `./data/notes.json` should update on the host machine

## What endpoints exist (no auth)

- `GET /api/notes/`
- `POST /api/notes/`
- `GET /api/notes/{id}/`
- `PUT /api/notes/{id}/`
- `DELETE /api/notes/{id}/`

## Where data is stored

- Docker Compose mounts `./data` into the backend at `/data`
- Backend uses `NOTES_DATA_FILE=/data/notes.json`

