<script>
  import { onMount } from 'svelte';
  import { deleteNote, fetchNotes, createNote, updateNote } from '$lib/api';

  let notes = [];
  let loading = true;
  let error = '';

  let title = '';
  let body = '';
  let editingId = null;

  async function reloadNotes() {
    loading = true;
    error = '';
    try {
      notes = await fetchNotes();
    } catch (e) {
      error = e?.message ?? String(e);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    reloadNotes();
  });

  function startCreate() {
    editingId = null;
    title = '';
    body = '';
  }

  function startEdit(note) {
    editingId = note.id;
    title = note.title ?? '';
    body = note.body ?? '';
  }

  async function submitForm() {
    error = '';
    try {
      if (editingId === null) {
        await createNote({ title, body });
      } else {
        await updateNote({ id: editingId, title, body });
      }
      startCreate();
      await reloadNotes();
    } catch (e) {
      error = e?.message ?? String(e);
    }
  }

  async function remove(noteId) {
    const ok = confirm('Delete this note?');
    if (!ok) return;
    error = '';
    try {
      await deleteNote(noteId);
      if (editingId === noteId) startCreate();
      await reloadNotes();
    } catch (e) {
      error = e?.message ?? String(e);
    }
  }
</script>

<h2 style="margin: 0 0 12px 0;">
  {editingId === null ? 'Create a note' : `Edit note #${editingId}`}
</h2>

<form on:submit|preventDefault={submitForm} style="display: grid; gap: 10px; margin-bottom: 18px;">
  <label style="display: grid; gap: 6px;">
    <span style="font-size: 13px; color: #555;">Title</span>
    <input
      bind:value={title}
      required
      maxlength="200"
      placeholder="e.g. Sprint planning"
      style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;"
    />
  </label>

  <label style="display: grid; gap: 6px;">
    <span style="font-size: 13px; color: #555;">Body</span>
    <textarea
      bind:value={body}
      rows="4"
      placeholder="Write something chill..."
      style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; resize: vertical;"
    />
  </label>

  <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
    <button
      type="submit"
      style="padding: 10px 14px; border: 0; border-radius: 8px; background: #111; color: white; cursor: pointer;"
    >
      {editingId === null ? 'Create' : 'Save'}
    </button>

    {#if editingId !== null}
      <button
        type="button"
        on:click={startCreate}
        style="padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; background: white; cursor: pointer;"
      >
        Cancel
      </button>
    {/if}
  </div>
</form>

{#if error}
  <div style="margin-bottom: 14px; padding: 12px; border-radius: 8px; border: 1px solid #f2c0c0; background: #fff3f3; color: #7a1d1d;">
    {error}
  </div>
{/if}

<h2 style="margin: 0 0 12px 0;">Your notes</h2>

{#if loading}
  <p style="color: #666;">Loading...</p>
{:else if notes.length === 0}
  <p style="color: #666;">No notes yet. Create one above.</p>
{:else}
  <ul style="list-style: none; padding: 0; margin: 0; display: grid; gap: 10px;">
    {#each notes as n (n.id)}
      <li style="border: 1px solid #eee; background: #fafafa; border-radius: 10px; padding: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 10px;">
          <div>
            <strong>#{n.id}</strong> {n.title}
          </div>
          <div style="font-size: 12px; color: #777;">Updated {n.updated_at ? new Date(n.updated_at).toLocaleString() : ''}</div>
        </div>
        <div style="margin-top: 8px; color: #333; white-space: pre-wrap;">{n.body}</div>
        <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
          <button
            type="button"
            on:click={() => startEdit(n)}
            style="padding: 8px 12px; border-radius: 8px; border: 1px solid #ddd; background: white; cursor: pointer;"
          >
            Edit
          </button>
          <button
            type="button"
            on:click={() => remove(n.id)}
            style="padding: 8px 12px; border-radius: 8px; border: 1px solid #f2c0c0; background: #fff3f3; color: #7a1d1d; cursor: pointer;"
          >
            Delete
          </button>
        </div>
      </li>
    {/each}
  </ul>
{/if}

