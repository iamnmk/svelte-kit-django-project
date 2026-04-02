from __future__ import annotations

import json
import os
import tempfile
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from django.conf import settings


@dataclass(frozen=True)
class NoteRecord:
    id: int
    title: str
    body: str
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601


class JSONNoteStore:
    """
    Minimal JSON-file persistence for demo usage.

    Storage format:
      [
        {"id": 1, "title": "...", "body": "...", "created_at": "...", "updated_at": "..."},
        ...
      ]
    """

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._ensure_parent_dir()
        # Ensure file exists so first GET works.
        if not os.path.exists(self.path):
            self._write_all([])

    def _ensure_parent_dir(self) -> None:
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _read_all(self) -> List[Dict[str, Any]]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # For a demo, treat corruption as empty rather than 500ing.
            return []

        if isinstance(raw, dict):
            # Allow {"notes": [...]} shape if ever used.
            raw = raw.get("notes", [])

        if not isinstance(raw, list):
            return []

        return raw

    def _write_all(self, notes: List[Dict[str, Any]]) -> None:
        self._ensure_parent_dir()

        # Atomic replace for reliability.
        fd, tmp_path = tempfile.mkstemp(prefix="notes_", suffix=".json", dir=os.path.dirname(self.path) or ".")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass

    def list_notes(self) -> List[Dict[str, Any]]:
        with self._lock:
            return self._read_all()

    def get_note(self, note_id: int) -> Optional[Dict[str, Any]]:
        with self._lock:
            for n in self._read_all():
                try:
                    if int(n.get("id")) == note_id:
                        return n
                except (TypeError, ValueError):
                    continue
            return None

    def create_note(self, title: str, body: str) -> Dict[str, Any]:
        with self._lock:
            notes = self._read_all()
            max_id = 0
            for n in notes:
                try:
                    max_id = max(max_id, int(n.get("id")))
                except (TypeError, ValueError):
                    continue

            now = self._now_iso()
            new_note = {
                "id": max_id + 1,
                "title": title,
                "body": body,
                "created_at": now,
                "updated_at": now,
            }
            notes.append(new_note)
            self._write_all(notes)
            return new_note

    def update_note(self, note_id: int, title: str, body: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            notes = self._read_all()
            updated: Optional[Dict[str, Any]] = None
            for n in notes:
                try:
                    if int(n.get("id")) == note_id:
                        n["title"] = title
                        n["body"] = body
                        n["updated_at"] = self._now_iso()
                        updated = n
                        break
                except (TypeError, ValueError):
                    continue

            if updated is None:
                return None

            self._write_all(notes)
            return updated

    def delete_note(self, note_id: int) -> bool:
        with self._lock:
            notes = self._read_all()
            before_len = len(notes)
            notes = [n for n in notes if str(n.get("id")) != str(note_id)]
            deleted = len(notes) != before_len
            if deleted:
                self._write_all(notes)
            return deleted


_store_instance: Optional[JSONNoteStore] = None
_store_lock = threading.Lock()


def get_store() -> JSONNoteStore:
    global _store_instance
    with _store_lock:
        if _store_instance is None:
            _store_instance = JSONNoteStore(settings.NOTES_DATA_FILE)
        return _store_instance

