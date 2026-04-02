from __future__ import annotations

from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(allow_blank=True)
    # JSON-file store persists timestamps as ISO8601 strings.
    # Treat them as strings to avoid DRF DateTimeField expecting datetime objects.
    created_at = serializers.CharField()
    updated_at = serializers.CharField()


class NoteCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(allow_blank=True, required=False, default="")


class NoteUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(allow_blank=True, required=False, default="")

