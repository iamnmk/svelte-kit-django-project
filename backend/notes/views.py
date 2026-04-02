from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import NoteCreateSerializer, NoteSerializer, NoteUpdateSerializer
from .store import get_store


class NotesListCreateView(APIView):
    """
    Public CRUD endpoints for notes (no auth).
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        store = get_store()
        notes = store.list_notes()

        # Keep response shape consistent.
        notes_sorted = sorted(notes, key=lambda n: int(n.get("id", 0)), reverse=True)
        serializer = NoteSerializer(notes_sorted, many=True)
        return Response(serializer.data)

    def post(self, request):
        store = get_store()
        serializer = NoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = store.create_note(
            title=serializer.validated_data["title"],
            body=serializer.validated_data.get("body", ""),
        )
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


class NotesDetailView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, pk: int):
        store = get_store()
        note = store.get_note(pk)
        if note is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(NoteSerializer(note).data)

    def put(self, request, pk: int):
        store = get_store()
        serializer = NoteUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated = store.update_note(
            note_id=pk,
            title=serializer.validated_data["title"],
            body=serializer.validated_data.get("body", ""),
        )
        if updated is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(NoteSerializer(updated).data)

    def delete(self, request, pk: int):
        store = get_store()
        deleted = store.delete_note(pk)
        if not deleted:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
