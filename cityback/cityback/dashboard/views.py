"""Dashboard views."""
from django.shortcuts import render
import os


def rtDemo(request):
    """Serve the index."""

    return render(request, "rtDemo.html", {'hostname':
                                           os.environ.get("HOSTNAME", "None")})
