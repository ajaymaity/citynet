"""Dashboard views."""
from django.shortcuts import render


def rtDemo(request):
    """Serve the index."""
    return render(request, "rtDemo.html", {})
