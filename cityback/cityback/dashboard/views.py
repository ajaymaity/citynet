"""Dashboard views."""
from django.shortcuts import render


def index_view(request):
    """Serve the index."""
    return render(request, "index.html", {})
