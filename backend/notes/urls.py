from django.urls import path

from .views import NotesDetailView, NotesListCreateView

urlpatterns = [
    # Accept both `/api/notes` and `/api/notes/` to avoid Django APPEND_SLASH POST redirects.
    path("notes", NotesListCreateView.as_view(), name="notes-list-create-non-slash"),
    path("notes/", NotesListCreateView.as_view(), name="notes-list-create"),
    path("notes/<int:pk>", NotesDetailView.as_view(), name="notes-detail-non-slash"),
    path("notes/<int:pk>/", NotesDetailView.as_view(), name="notes-detail"),
]

